#!/usr/bin/env python
#coding=utf8
import json
import datetime
import os
import time
from netaddr import IPNetwork
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.db.models import Q
from django.utils.html import escape
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import get_users_with_perms, get_groups_with_perms, get_perms_for_model
from guardian.forms import UserObjectPermissionsForm, GroupObjectPermissionsForm
from apps.networkcenter.shortcut import page, save_history, ip2host, importexcel, exportexcel, display_tree
from apps.networkcenter.models import *
from apps.networkcenter.forms import *
from apps.systemcenter.models import ServerPool


month_first_day = datetime.date(datetime.date.today().year, datetime.date.today().month, 1).isoformat()
today_now = datetime.date.today().isoformat()


def networkindex(request):
    """
    #网络中心index页面
    """
    index = 'assets'
    if request.method == 'POST':
        if False:
            return HttpResponse(json.dumps({"code": 1, "message": 2}))
        else:
            return HttpResponse(json.dumps({"code": 0}))
    else:
        return render_to_response("networkcenter/networkindex.html", locals(), context_instance=RequestContext(request))


#------------机房View--------------------------------------------------------
def idcindex(request):
    index = 'idclist'
    print os.getcwd()
    u = request.user
    if request.method == 'POST':
        form = IDCForm(request.POST)
        if form.is_valid():
            if u.has_perm("networkcenter.add_idc"):
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "address": form['address'].errors,
                                                                   "mail": form['mail'].errors, }}))
    else:
        idc_pool = IDC.objects.all()
        ip_net = IpSection.objects.all()
        idc_form = IDCForm()
        rack_form = RackForm
        ip_net_form = IpSectionForm()
        rack_all = Rack.objects.all()
        device_all = Device.objects.all()
        return render(request, 'networkcenter/idcindex.html', {'index': index, 'idc_pool': idc_pool, 'ip_net': ip_net,
                                                               'idc_form': idc_form, 'rack_form': rack_form,
                                                               'ip_net_form': ip_net_form, "rack_all": rack_all,
                                                               "device_all": device_all})


def idcedit(request, id):
    index = 'assets'
    u = request.user
    idc = get_object_or_404(IDC, pk=int(id))
    if request.method == 'POST':
        form = IdcForm(request.POST, instance=idc)
        if form.is_valid():
            if u.has_perm("networkcenter.change_idc"):
                #save_history(form, request)
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有编辑权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "address": form['address'].errors,
                                                                   "mail": form['mail'].errors}}))
    else:
        form = IdcForm(instance=idc)
        return render_to_response('networkcenter/idcedit.html', {'index': index, 'form': form},
                                  context_instance=RequestContext(request))


def idcdel(request, id):
    idc_del = get_object_or_404(IDC, pk=id)
    u = request.user
    if idc_del.device_set.count() == 0 and idc_del.ipadress_set.count() == 0:
        idc_del.changed_by = User.objects.get(username=request.user)
        if u.has_perm("networkcenter.delete_idc"):
            idc_del.delete()
            return HttpResponse(json.dumps({"code": 1}))
        else:
            auth = u'没有删除权限'
            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
    else:
        auth = u'使用中'
        return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))

#---------------机房View end----------------------------------------------


#---------------机柜View--------------------------------------------------
def racklist(request):
    index = 'idclist'
    u = request.user
    all_errors = ''
    if request.method == 'POST':
        form = RackForm(request.POST)
        if form.is_valid():
            if u.has_perm("networkcenter.add_rack"):
                rack = form.save()
                for nameid in range(1, 21):
                    try:
                        Position.objects.get_or_create(name=nameid, rack=rack)
                    except:
                        pass
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            if form.non_field_errors:
                all_errors = u'机柜和IDC不能同时重复'
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors, "all": all_errors,
                                                                   "idc": form['idc'].errors}}))
    else:
        id = request.GET.get('idc')
        idc_pool = IDC.objects.all()
        ip_net = IpSection.objects.all()
        idc = get_object_or_404(IDC, id=id)
        rack = Rack.objects.filter(idc=idc)
        idc_form = IDCForm()
        rack_form = RackForm(initial={'idc': idc.id})
        ip_net_form = IpSectionForm
        return render(request, 'networkcenter/racklist.html', {'index': index, 'idcs': rack, 'idc_form': idc_form,
                                                               'ip_net': ip_net, 'rack_form': rack_form, 'idc': idc,
                                                               'idc_pool': idc_pool, 'ip_net_form': ip_net_form})


def rackdetail(request, id):
    index = 'assets'
    rack = get_object_or_404(Rack, pk=int(id))
    return render(request, 'networkcenter/rackdetail.html', {"index": index, "rack": rack})


def rackedit(request, id):
    index = 'assets'
    all_errors = ''
    u = request.user
    rack = get_object_or_404(Rack, pk=int(id))
    host_list = rack.device_set.all().order_by('position')
    if request.method == 'POST':
        form = RackForm(request.POST, instance=rack)
        if form.is_valid():
            if u.has_perm("networkcenter.change_rack"):
                #save_history(form, request)
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有编辑权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            if form.non_field_errors:
                all_errors = u'机柜和IDC不能同时重复'
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "all": all_errors,
                                                                   "idc": form['idc'].errors}}))
    else:
        form = RackForm(instance=rack)
        return render_to_response('networkcenter/rackedit.html', {'index': index, 'form': form, "host_list": host_list,
                                                                  'idcs': rack},
                                  context_instance=RequestContext(request))


def rackdel(request, id):
    rack = get_object_or_404(Rack, pk=int(id))
    u = request.user
    rack_inuse = rack.device_set.all().count()
    if rack_inuse == 0:
        rack.changed_by = User.objects.get(username=request.user)
        if u.has_perm("networkcenter.delete_rack"):
            rack.delete()
            return HttpResponse(json.dumps({"code": 1}))
        else:
            auth = u'没有删除权限'
            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
    else:
        auth = u'机柜使用中!'
        return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))

#---------------------机柜View end------------------------------------------


#---------------------IP View----------------------------------------------
def ipsection(request):
    index = 'assets'
    u = request.user
    if request.method == 'POST':
        form = IpSectionForm(request.POST)
        if form.is_valid():
            if u.has_perm("networkcenter.add_ipsection"):
                #save_history(form, request)
                ipsec = form.save()
                ip_pool = IPNetwork(ipsec.name)
                category = request.POST.get('category')
                for ip in ip_pool:
                    try:
                        IpAdress.objects.get_or_create(name=ip, section=ipsec, idc=ipsec.idc, category=category)
                    except Exception, e:
                        pass
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            all_error = form.non_field_errors() and u"子网重复" or ''
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors, "all_error": all_error,
                                                                   "idc": form['idc'].errors,
                                                                   "remark": form['remark'].errors}}))
    else:
        form = IpSectionForm()
        ip_use_status = {}
        for ip in ipsec:
            ip_use_status[ip.id] = (ip.ipadress_set.filter(status=True).count(),
                                    ip.ipadress_set.filter(status=False).count())
        return render_to_response('networkcenter/ipsection.html',
                                  {'index': index, 'form': form, 'ip_use_status': ip_use_status},
                                  context_instance=RequestContext(request))


def ipsectionedit(request, id):
    index = 'assets'
    u = request.user
    ipsec = IpSection.objects.get(id=id)
    if request.method == 'POST':
        form = IpSectionForm(request.POST, instance=ipsec)
        if form.is_valid():
            if u.has_perm("networkcenter.change_ipsection"):
                #save_history(form, request)
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有编辑权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "idc": form['idc'].errors,
                                                                   "remark": form['remark'].errors}}))
    else:
        form = IpSectionForm(instance=ipsec)
        return render_to_response('networkcenter/ipsectionedit.html', {'index': index, 'idcs': ipsec, 'form': form},
                                  context_instance=RequestContext(request))


def ipsectiondel(request, id):
    ipsec = get_object_or_404(IpSection, pk=int(id))
    u = request.user
    ip_inuse_sum = ipsec.ipadress_set.filter(status=True).count()
    if ip_inuse_sum == 0:
        ipsec.changed_by = User.objects.get(username=request.user)
        if u.has_perm("networkcenter.delete_ipsection"):
            ipsec.delete()
            return HttpResponse(json.dumps({"code": 1}))
        else:
            auth = u'没有删除权限'
            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
    else:
        auth = u'IP段使用中!'
        return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))


def iplist(request):
    index = 'idclist'
    iprang = '.'
    u = request.user
    if request.method == 'POST':
        form = IpForm(request.POST)
        if form.is_valid():
            if u.has_perm("networkcenter.add_ipadress"):
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"ip": form['name'].errors, 'iprang': iprang,
                                                                   "idc": form['idc'].errors,
                                                                   "section": form['section'].errors}}))
    else:
        idc_form = IDCForm()
        rack_form = RackForm()
        idc_pool = IDC.objects.all()
        ip_net = IpSection.objects.all()
        id = request.GET.get('ipnet')
        ip_net_form = IpSectionForm()
        if id:
            ipsec = IpSection.objects.get(id=id)
            ip_pool = IpAdress.objects.filter(section=ipsec)
        else:
            ipsec = u'所有IP'
            ip_pool = IpAdress.objects.all()
        return render(request, 'networkcenter/iplist.html', {'index': index, 'ip_pool': ip_pool, 'ipsec': ipsec,
                                                             'idc_form': idc_form, 'idc_pool': idc_pool,
                                                             'rack_form': rack_form, 'ip_net_form': ip_net_form,
                                                             'ip_net': ip_net, })


#----------------------------设备管理View----------------------------------
def deviceindex(request):
    index = 'device'
    form = DeviceForm(initial={})
    try:
        tag = DeviceTag.objects.get(tag="sw")
    except Exception, e:
        tag = None
    device = Device.objects.filter(tag=tag)
    device_type = get_object_or_404(DeviceLevel, level='dtype').devicetag_set.all()
    return render(request, "networkcenter/deviceindex.html", {'index': index, 'device_type': device_type, 'form': form,
                                                              'idcs': device, "tag": tag})


def devicetree(request):
    node_list = []
    default_tree = ['idc', 'dtype', 'vendor']
    node = display_tree(default_tree, node_list)
    #tree_list.append({'id': 'root', 'text': 'root', 'children': []})
    return HttpResponse(json.dumps(node))


def devicedetail(request, id):
    index = 'device'
    instance = Device.objects.get(id=id)
    dtp_list = [tag[0] for tag in DeviceLevel.objects.get(level="dtype").devicetag_set.all().values_list('tag')]
    vendor_list = [tag[0] for tag in DeviceLevel.objects.get(level="vendor").devicetag_set.all().values_list('tag')]
    prd_list = [tag[0] for tag in DeviceLevel.objects.get(level="prd").devicetag_set.all().values_list('tag')]
    sp_list = [tag[0] for tag in DeviceLevel.objects.get(level="sp").devicetag_set.all().values_list('tag')]
    if request.method == 'GET':
        return render(request, 'networkcenter/devicedetails.html',
                      {'idcs': instance, 'index': index, "sp_list": sp_list,
                       "prd_list": prd_list, "dtp_list": dtp_list,
                       "vendor_list": vendor_list})


def devicelist(request):
    index = 'device'
    u = request.user
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            if u.has_perm("networkcenter.add_device"):
                #save_history(form, request)
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"sn": form['sn'].errors,
                                                                   'idc': form['idc'].errors,
                                                                   "rack": form['rack'].errors,
                                                                   "position": form['position'].errors,
                                                                   "asset_id": form['position'].errors,
                                                                   "purchase_id": form['position'].errors,
                                                                   "buy_price": form['buy_price'].errors,
                                                                   "buy_time": form['buy_time'].errors,
                                                                   'expired_time': form['expired_time'].errors,
                                                                   "remark": form['position'].errors,
                                                                   "tag": form['tag'].errors}}))
    else:
        node = request.GET.get('node')
        device_type = get_object_or_404(DeviceLevel, level='dtype').devicetag_set.all()
        if node:
            level = DeviceLevel.objects.get(level=node.split('.')[0])
            tag = DeviceTag.objects.get(tag=node.split('.')[1], level=level)
            device = tag.device_set.all()
        else:
            device = Device.objects.all()
            tag = None
        form = DeviceForm(initial={})
        return render(request, 'networkcenter/devicelist.html', {'index': index, 'idcs': device, 'form': form,
                                                                 'device_type': device_type, 'tag': tag})


def devicetreelist(request):
    device_list = []
    node = request.GET.get('node')
    if node:
        node_list = node.split('_')
        set_list = []
        for n in node_list:
            try:
                level = DeviceLevel.objects.get(level=n.split('.')[0])
                tag = DeviceTag.objects.get(tag=n.split('.')[1], level=level)
                set_list.append(set(tag.device_set.all()))
            except Exception, e:
                pass
        try:
            device = list(set.intersection(*set_list))
        except Exception, e:
            device = []
    else:
        device = Device.objects.all()
    for dev in device:
        idc = dev.idc.name if dev.idc else ''
        rack = dev.rack.name if dev.rack else ''
        pos = dev.position.name if dev.position else ''
        device_list.append([dev.sn, idc, rack, pos, dev.status, dev.id])
    return HttpResponse(json.dumps(device_list))
    #form = DeviceForm(initial={})
    #return render(request, 'networkcenter/devicelist.html', {'index': index, 'idcs': device, 'form': form,
    #                                                         'device_type': device_type, 'tag': ''})


def deviceedit(request, id):
    index = 'device'
    u = request.user
    device = Device.objects.get(id=id)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            if u.has_perm("networkcenter.change_device"):
                #save_history(form, request)
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有编辑权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"sn": form['sn'].errors,
                                                                   'idc': form['idc'].errors,
                                                                   "rack": form['rack'].errors,
                                                                   "position": form['position'].errors,
                                                                   "asset_id": form['position'].errors,
                                                                   "purchase_id": form['position'].errors,
                                                                   "buy_price": form['buy_price'].errors,
                                                                   "buy_time": form['buy_time'].errors,
                                                                   'expired_time': form['expired_time'].errors,
                                                                   "remark": form['position'].errors,
                                                                   "tag": form['tag'].errors}}))
    else:
        form = DeviceForm(instance=device)
        return render_to_response('networkcenter/deviceedit.html', {'index': index, 'idcs': device, 'form': form},
                                  context_instance=RequestContext(request))


def importdevice(request):
    u = request.user
    if request.method == 'POST':
        if u.has_perm("networkcenter.add_device"):
            file_excel = request.FILES.get('file')
            if file_excel:
                xls = 'upload/myexcel/%s.xlsx' % (request.user.username,)
                myexcel = file(xls, 'wb+')
                for excel in file_excel:
                    myexcel.write(excel)
                myexcel.close()
                importexcel(request)
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'导入错误,请选择文件！'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            auth = u'没有导入权限'
            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))


def exportdevice(request):
    u = request.user
    if request.method == 'GET':
        if u.has_perm("networkcenter.add_device"):
            exportexcel(request)
            return HttpResponse(json.dumps({"code": 1}))
        else:
            auth = u'没有导出权限'
            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))


def deviceint(request, id):
    index = 'assets'
    u = request.user
    devobj = Device.objects.get(id=id)
    devint = DeviceNIC.objects.filter(device=devobj)
    if request.method == 'POST':
        form = DeviceIntForm(request.POST)
        if form.is_valid():
            if u.has_perm("networkcenter.add_devicenic"):
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            if form.non_field_errors:
                all_errors = u'设备接口已经存在'
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "device": form['device'].errors,
                                                                   "product": form['product'].errors,
                                                                   "vendor": form['vendor'].errors,
                                                                   "speed": form['speed'].errors,
                                                                   "mac": form['mac'].errors,
                                                                   "ip": form['ip'].errors,
                                                                   "vlan": form['vlan'].errors,
                                                                   "link": form['link'].errors,
                                                                   "remark": form['remark'].errors,
                                                                   "all": all_errors}}))
    else:
        form = DeviceIntForm({'device': devobj.id})
        return render(request, "networkcenter/deviceintlist.html", {'index': index, 'form': form, 'idcs': devint,
                                                                    'idc': devobj})


def deviceintedit(request, id):
    index = 'assets'
    u = request.user
    devint = DeviceNIC.objects.get(id=id)
    if request.method == 'POST':
        form = DeviceIntForm(request.POST, instance=devint)
        if form.is_valid():
            if u.has_perm("networkcenter.add_devicenic"):
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            if form.non_field_errors:
                all_errors = u'设备接口已经存在'
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "device": form['device'].errors,
                                                                   "product": form['product'].errors,
                                                                   "vendor": form['vendor'].errors,
                                                                   "speed": form['speed'].errors,
                                                                   "mac": form['mac'].errors,
                                                                   "ip": form['ip'].errors,
                                                                   "vlan": form['vlan'].errors,
                                                                   "link": form['link'].errors,
                                                                   "remark": form['remark'].errors,
                                                                   "all": all_errors}}))
    else:
        form = DeviceIntForm(instance=devint)
        return render(request, "networkcenter/deviceintedit.html", {'index': index, 'form': form, 'idcs': devint})


def devicetoowt(request, devid, owtid):
    u = request.user
    if request.method == 'GET':
        if u.has_perm("systemcenter.add_host"):
            device = Device.objects.get(id=int(devid))
            if device.device_type.name == u'服务器':
                host, status = Host.objects.get_or_create(device=device)
                owt = OwnerTeam.objects.get(id=int(owtid))
                device.owt = owt
                device.status = True
                device.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'交换机不能分配'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            auth = u'没有添加权限'
            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))


##----------------------------公司View------------------------------------
def domain(request):
    index = 'assets'
    u = request.user
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            if u.has_perm("networkcenter.add_domain"):
                #save_history(form, request)
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "cop": form['cop'].errors,
                                                                   "registrar": form['registrar'].errors,
                                                                   "remark": form['remark'].errors, }}))
    else:
        form = DomainForm(initial={})
        domain = page(request, Domain.objects.all())
        return render_to_response('networkcenter/domain.html', {'index': index, 'idcs': domain, 'form': form},
                                  context_instance=RequestContext(request))


def domaindel(request, id):
    domain_del = get_object_or_404(Domain, pk=id)
    u = request.user
    domain_inuse_sum = domain_del.domainrecord_set.all().count()
    if domain_inuse_sum == 0:
        domain_del.changed_by = User.objects.get(username=request.user)
        if u.has_perm("networkcenter.delete_domain"):
            domain_del.delete()
            return HttpResponse(json.dumps({"code": 1}))
        else:
            auth = u'没有删除权限'
            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
    else:
        auth = u'域名还有解析'
        return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))


def domainedit(request, id):
    index = 'assets'
    domain = Domain.objects.get(id=id)
    u = request.user
    if request.method == 'POST':
        form = DomainForm(request.POST, instance=domain)
        if form.is_valid():
            if u.has_perm("networkcenter.change_domain"):
                #save_history(form, request)
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有编辑权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "cop": form['cop'].errors,
                                                                   "registrar": form['registrar'].errors,
                                                                   "remark": form['remark'].errors, }}))
    else:
        form = DomainForm(instance=domain)
        return render_to_response('networkcenter/domainedit.html', {'index': index, 'idcs': domain, 'form': form},
                                  context_instance=RequestContext(request))


def domainre(request, id):
    index = 'assets'
    u = request.user
    if request.method == 'POST':
        form = DomainRecordForm(request.POST)
        if form.is_valid():
            if u.has_perm("networkcenter.add_domain"):
                #save_history(form, request)
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "domain": form['domain'].errors,
                                                                   "record_type": form['record_type'].errors,
                                                                   "record_value": form['record_value'].errors,
                                                                   "record_ttl": form['record_ttl'].errors,
                                                                   "remark": form['remark'].errors, }}))
    else:
        form = DomainRecordForm(initial={'domain': id})
        domain = Domain.objects.get(id=id)
        domain_re = DomainRecord.objects.filter(domain_id=id)
        return render_to_response('networkcenter/domainre.html', {'index': index, 'idcs': domain_re, 'domain': domain,
                                                                  'form': form},
                                  context_instance=RequestContext(request))


def domainredel(request, id):
    domainre_del = get_object_or_404(DomainRecord, pk=id)
    u = request.user
    domainre_del.changed_by = User.objects.get(username=request.user)
    if u.has_perm("networkcenter.delete_domainrecord"):
        domainre_del.delete()
        return HttpResponse(json.dumps({"code": 1}))
    else:
        auth = u'没有删除权限'
        return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))


def domainreedit(request, id):
    index = 'assets'
    u = request.user
    domain_re = DomainRecord.objects.get(id=id)
    if request.method == 'POST':
        form = DomainRecordForm(request.POST, instance=domain_re)
        if form.is_valid():
            if u.has_perm("networkcenter.change_domainrecord"):
                #save_history(form, request)
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有编辑权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "domain": form['domain'].errors,
                                                                   "record_type": form['record_type'].errors,
                                                                   "record_value": form['record_value'].errors,
                                                                   "record_ttl": form['record_ttl'].errors,
                                                                   "remark": form['remark'].errors}}))
    else:
        form = DomainRecordForm(instance=domain_re)
        return render_to_response('networkcenter/domainreedit.html', {'index': index, 'idcs': domain_re, 'form': form},
                                  context_instance=RequestContext(request))


# for api get Rack and Position
def getrack(request):
    if request.is_ajax():
        if request.method == "POST":
            rack_list = []
            idc_id = request.POST.get('idc', 1)
            if idc_id:
                idc = IDC.objects.get(id=idc_id)
                rack_query = Rack.objects.filter(idc=idc)
                for rack in rack_query:
                    rack_list.append({"id": rack.id, "name": rack.name})
                return HttpResponse(json.dumps({"code": 1, "message": rack_list}))
            else:
                return HttpResponse(json.dumps({"code": 0, "message": {"request_error": u'请求不合法'}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"request_error": u'请求不合法'}}))
    else:
        return HttpResponse(json.dumps({"code": 0, "message": {"request_error": u'请求不合法'}}))


def getposition(request):
    if request.is_ajax():
        if request.method == "POST":
            position_list = []
            rack_id = request.POST.get('rack', 1)
            if rack_id:
                rack = Rack.objects.get(id=rack_id)
                position_query = Position.objects.filter(rack=rack, status=False)
                for position in position_query:
                    position_list.append({"id": position.id, "name": position.__unicode__()})
                return HttpResponse(json.dumps({"code": 1, "message": position_list}))
            else:
                return HttpResponse(json.dumps({"code": 0, "message": {"request_error": u'请求不合法'}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"request_error": u'请求不合法'}}))
    else:
        return HttpResponse(json.dumps({"code": 0, "message": {"request_error": u'请求不合法'}}))


def srvpool(request):
    index = 'cobbler'
    uname = request.user.username
    if request.method == "POST":
        x = 1
    else:
        try:
            srvpools = DeviceTag.objects.get(
                Q(tag="srv") & Q(level=DeviceLevel.objects.get(level="dtype"))).device_set.filter(status=False)
        except Exception, e:
            srvpools = []
        form = OSInstallQueueForm()
        return render(request, "networkcenter/ossrvpool.html", {"index": index, "idcs": srvpools, "form": form})


def osinstall(request):
    index = 'cobbler'
    uname = request.user.username
    if request.method == "POST":
        form = OSInstallQueueForm(request.POST)
        if form.is_valid():
            instance = form.save()
            desc = request.POST.get("description")
            unavailable_device = []
            from apps.networkcenter.shortcut import get_device_ip, get_osinstall, get_device_mac
            batch = "%s%s%s" % (time.strftime("%Y%m%d%H%M%S"), uname.upper(), instance.needs_user.username.upper())
            batch_instance = OSInstallTask.objects.get_or_create(batch_name=batch, description=desc)[0]
            for sn in [sn for sn in instance.sn.split("\r\n") if sn != ""]:
                try:
                    d = Device.objects.get(sn=sn)
                except Device.DoesNotExist:
                    d = None
                try:
                    #判断装机任务是否已经存在 and 是否有人已经提交
                    os = OSInstallQueue.objects.get(Q(sn=d.sn) & ~Q(status="11"))
                except Exception, e:
                    os = None
                if not d.status and not os:
                    os = OSInstallQueue(sn=d.sn, tp_type=instance.tp_type, install=get_osinstall(d.sn),
                                        create_user=uname, ilo_ip=get_device_ip(d, "ilo"),
                                        os_ip=get_device_ip(d, "bond0"), eth0_mac=get_device_mac(d),
                                        needs_user=instance.needs_user, batch=batch_instance)
                    os.save()
                    d.status = True
                    d.save()
                else:
                    unavailable_device.append(sn)
            return HttpResponse(json.dumps({"code": 1, "message": {"unavailable_device": unavailable_device}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"sn": form['sn'].errors,
                                                                   "needs_user": form["needs_user"].errors,
                                                                   "description": form["description"].errors}}))
    else:
        form = OSInstallQueueForm()
        os_list = OSInstallQueue.objects.filter(Q(create_user=uname) & ~Q(status="11"))
        return render(request, "networkcenter/osinstall.html", {"index": index, "form": form, "os_list": os_list})


def osinstallrefresh(request, id):
    from apps.networkcenter.shortcut import get_device_ip, get_osinstall, get_device_mac

    os = OSInstallQueue.objects.get(id=id)
    d = Device.objects.get(sn=os.sn)
    (os.install, os.ilo_ip, os.os_ip, os.eth0_mac) = (get_osinstall(d.sn), get_device_ip(d, "ilo"),
                                                      get_device_ip(d, "bond0"), get_device_mac(d))
    if os.install and os.ilo_ip and os.os_ip and os.eth0_mac:
        os.save()
        return HttpResponse(json.dumps({"code": 1, "message": 1}))
    else:
        return HttpResponse(json.dumps({"code": 0, "message": 1}))


def osinstallsubmit(request, id):
    from apps.networkcenter.shortcut import os_install

    try:
        os = OSInstallQueue.objects.get(id=id)
        gearman_server = '%s.%s.%s.220' % (os.os_ip.split('.')[0], os.os_ip.split('.')[1], os.os_ip.split('.')[2])
        install_param = {'sn': os.sn, 'ip': os.os_ip, 'mac': os.eth0_mac, 'ilo': os.ilo_ip}
        os_install(gearman_server, json.dumps(install_param))
        return HttpResponse(json.dumps({"code": 1, "message": 1}))
    except Exception, e:
        return HttpResponse(json.dumps({"code": 0, "message": 1}))


def osinstallcomplete(request):
    """已完成装机队列"""
    index = 'cobbler'
    uname = request.user.username
    if request.method == "GET":
        form = OSInstallQueueForm()
        os_list = OSInstallQueue.objects.filter(Q(create_user=uname) & Q(status="11") & Q(deliver=False))
        return render(request, "networkcenter/osinstall.html", {"index": index, "form": form, "os_list": os_list})

    else:
        return HttpResponse("请求错误")


def osinstalldeliver(request, id):
    from apps.systemcenter.models import ServerPool
    try:
        os = OSInstallQueue.objects.get(id=id)
        d = Device.objects.get(sn=os.sn)
        os.deliver = True
        d.status = True
        s = ServerPool(sn=os.sn, ip=os.os_ip, oper=os.needs_user, description=os.batch.description)
        os.save()
        d.save()
        s.save()
        return HttpResponse(json.dumps({"code": 1, "message": 1}))
    except Exception, e:
        return HttpResponse(json.dumps({"code": 0, "message": 1}))

#权限管理
#def permissions(request, target, id):
#    index = 'assets'
#    u = request.user
#    username = request.user.first_name
#    model_list = {'idc': IDC, 'rack': Rack, 'ip': IpAdress, 'device': Device, 'company': Company, 'supplier': Supplier,
#                  'owt': OwnerTeam, 'loc': Location, 'brands': Brands, 'devicetype': DeviceType, 'domain': Domain,
#                  'devicemodel': DeviceModel, 'ipsection': IpSection, }
#    model_name = {'idc': u'机房', 'rack': u'机柜', 'ip': u'IP', 'device': u'设备', 'company': u'公司',
#                  'supplier': u'厂商', 'owt': u'部门', 'loc': u'地区', 'brands': u'品牌', 'devicetype': u'设备类型',
#                  'domain': u'域名', 'devicemodel': u'设备型号', 'ipsection': u'IP段'}
#    obj = model_list[target].objects.get(id=id)
#    obj_name = model_name[target]
#    if request.method == 'POST':
#        if u.has_perm("auth.add_permission"):
#            user_id = request.POST.get('user', None)
#            group_id = request.POST.get('groups', None)
#            if user_id:
#                user = get_object_or_404(User, pk=user_id)
#                form = UserObjectPermissionsForm(user, obj, request.POST or None)
#                if form.is_valid():
#                    form.save_obj_perms()
#                    return HttpResponse(json.dumps({"code": 1}))
#                else:
#                    return HttpResponse(json.dumps({"code": 0, "message": {"name": form['permissions'].errors}}))
#            if group_id:
#                groups = get_object_or_404(Group, pk=group_id)
#                form = GroupObjectPermissionsForm(groups, obj, request.POST or None)
#                if form.is_valid():
#                    form.save_obj_perms()
#                    return HttpResponse(json.dumps({"code": 1}))
#                else:
#                    return HttpResponse(json.dumps({"code": 0, "message": {"name": form['permissions'].errors}}))
#            else:
#                return HttpResponse(json.dumps({"code": 0, "message": {"name": u'请选择用户或用户组'}}))
#        else:
#            auth = u'没有添加权限'
#            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
#    else:
#        user_perm_item = [(p.codename, p.name) for p in get_perms_for_model(obj)]
#        obj_user_perm = get_users_with_perms(obj, attach_perms=True)
#        obj_groups_perm = get_groups_with_perms(obj, attach_perms=True)
#        usersform = ObjUserPermForm(obj)
#        groupsform = ObjGroupsPermForm(obj)
#        return render(request, "networkcenter/permissions.html", {'usersform': usersform, 'groupsform': groupsform,
#                                                                  'index': index, 'username': username, 'obj': obj,
#                                                                  'obj_name': obj_name,
#                                                                  'user_perm_item': user_perm_item,
#                                                                  'obj_user_perm': obj_user_perm,
#                                                                  'obj_groups_perm': obj_groups_perm, })


#def user_perm(request, target, id, userid):
#    index = 'assets'
#    u = request.user
#    username = request.user.first_name
#    model_list = {'idc': IDC, 'rack': Rack, 'ip': IpAdress, 'device': Device, 'company': Company, 'supplier': Supplier,
#                  'owt': OwnerTeam, 'loc': Location, 'brands': Brands, 'devicetype': DeviceType, 'domain': Domain,
#                  'devicemodel': DeviceModel, 'ipsection': IpSection, }
#    model_name = {'idc': u'机房', 'rack': u'机柜', 'ip': u'IP', 'device': u'设备', 'company': u'公司',
#                  'supplier': u'厂商', 'owt': u'部门', 'loc': u'地区', 'brands': u'品牌', 'devicetype': u'设备类型',
#                  'domain': u'域名', 'devicemodel': u'设备型号', 'ipsection': u'IP段'}
#    obj = model_list[target].objects.get(id=id)
#    obj_name = model_name[target]
#    user_obj = get_object_or_404(User, pk=userid)
#    if request.method == 'POST':
#        if u.has_perm("auth.change_permission"):
#            user_id = request.POST.get('user', None)
#            if user_id:
#                user = get_object_or_404(User, pk=user_id)
#                form = UserObjectPermissionsForm(user, obj, request.POST or None)
#                if form.is_valid():
#                    form.save_obj_perms()
#                    return HttpResponse(json.dumps({"code": 1}))
#                else:
#                    return HttpResponse(json.dumps({"code": 0, "message": {"name": form['permissions'].errors}}))
#        else:
#            auth = u'没有添加权限'
#            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
#    else:
#        form = ObjUserPermForm(obj, user_obj)
#        return render(request, "networkcenter/userperm.html",
#                      {'form': form, 'index': index, 'username': username, 'obj': obj,
#                       'obj_name': obj_name})
#
#
#def group_perm(request, target, id, groupid):
#    index = 'assets'
#    u = request.user
#    model_list = {'idc': IDC, 'rack': Rack, 'ip': IpAdress, 'device': Device, 'company': Company, 'supplier': Supplier,
#                  'owt': OwnerTeam, 'loc': Location, 'brands': Brands, 'devicetype': DeviceType, 'domain': Domain,
#                  'devicemodel': DeviceModel, 'ipsection': IpSection, 'domainrecord': DomainRecord}
#    model_name = {'idc': u'机房', 'rack': u'机柜', 'ip': u'IP', 'device': u'设备', 'company': u'公司',
#                  'supplier': u'厂商', 'owt': u'部门', 'loc': u'地区', 'brands': u'品牌', 'devicetype': u'设备类型',
#                  'domain': u'域名', 'devicemodel': u'设备型号', 'ipsection': u'IP段', 'domainrecord': u'域名记录'}
#    obj = model_list[target].objects.get(id=id)
#    obj_name = model_name[target]
#    group_obj = get_object_or_404(Group, pk=groupid)
#    if request.method == 'POST':
#        if u.has_perm("auth.change_permission"):
#            group_id = request.POST.get('groups', None)
#            if group_id:
#                groups = get_object_or_404(Group, pk=group_id)
#                form = GroupObjectPermissionsForm(groups, obj, request.POST or None)
#                if form.is_valid():
#                    form.save_obj_perms()
#                    return HttpResponse(json.dumps({"code": 1}))
#                else:
#                    return HttpResponse(json.dumps({"code": 0, "message": {"name": form['permissions'].errors}}))
#        else:
#            auth = u'没有添加权限'
#            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
#    else:
#        form = ObjGroupsPermForm(obj, group_obj)
#        return render(request, "networkcenter/groupperm.html",
#                      {'form': form, 'index': index, 'obj': obj, 'obj_name': obj_name})
