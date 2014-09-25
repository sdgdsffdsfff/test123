#!/usr/bin/env python
#coding=utf8
# Create your views here.
import json
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from apps.networkcenter.shortcut import page
from apps.systemcenter.models import *
from apps.systemcenter.forms import *
from copy import deepcopy


def index(request):
    """
    #系统管理中心 index页面
    """
    index = "system"
    return render(request, "systemcenter/index.html", {'index': index})


def display_tree(trees, node_list):
    tree_list = []
    if trees:
        tree = trees.pop()
        childrens = SystemLevel.objects.get(level=tree).systemtag_set.all()
        if childrens:
            for ch in childrens:
                if not node_list:
                    tree_list.append({'id': "%s.%s" % (ch.level, ch.tag), 'text': ch.remask, 'children': node_list})
                elif trees:
                    tree_list.append({'id': "%s.%s" % (ch.level, ch.tag), "state": "closed", 'text': ch.remask,
                                      'children': node_list})
                else:
                    tree_list.append({'id': "%s.%s" % (ch.level, ch.tag), 'text': ch.remask, 'children': node_list})
        node_list = deepcopy(tree_list)
        return display_tree(trees, node_list)
    else:
        return node_list


def serverindex(request):
    """
    #主机管理 index页面
    """
    index = "server"
    pool = ServerPool.objects.filter(status="00")
    #tree_list.append({'id': 'root', 'text': 'root', 'children': []})
    return render(request, "systemcenter/serverindex.html", {'index': index, 'server_pool': pool})


def servertree(request):
    node_list = []
    default_tree = ['cop', 'pdl', 'sbs', 'grp']
    node = display_tree(default_tree, node_list)
    return HttpResponse(json.dumps(node))


def physerver(request):
    index = 'server'
    srv_type = u"物理机"
    if request.method == 'GET':
        phyhost_pool = ServerPool.objects.filter(~Q(status="00") & Q(is_vrt=False))
        return render(request, "systemcenter/serverlist.html", {'index': index, 'host_pool': phyhost_pool,
                                                                "srv_type": srv_type})


def vrtserver(request):
    index = 'server'
    srv_type = u"虚拟机"
    if request.method == 'GET':
        vrthost_pool = ServerPool.objects.filter(~Q(status="00") & Q(is_vrt=True))
        return render(request, "systemcenter/serverlist.html", {'index': index, 'host_pool': vrthost_pool,
                                                                "srv_type": srv_type})


def servertreelist(request):
    device_list = []
    if request.is_ajax() and request.method == "GET":
        node = request.GET.get('node')
        if node:
            node_list = node.split('_')
            set_list = []
            for n in node_list:
                try:
                    level = SystemLevel.objects.get(level=n.split('.')[0])
                    tag = SystemTag.objects.get(tag=n.split('.')[1], level=level)
                    set_list.append(set(tag.serverpool_set.filter(~Q(status="00"))))
                except Exception, e:
                    pass
            try:
                device = list(set.intersection(*set_list))
            except Exception, e:
                device = []
        else:
            device = Device.objects.all()
        for dev in device:
            device_list.append([dev.sn, dev.hostname, dev.ip, dev.detect, dev.collect, dev.status, dev.id])
        return HttpResponse(json.dumps(device_list))
    else:
        index = "srvtree"
        return render(request, "systemcenter/servertreelist.html", {'index': index})


def serverdetail(request, id):
    from apps.networkcenter.models import Device, DeviceLevel
    try:
        srv = ServerPool.objects.get(id=id)
    except Exception, e:
        raise Http404
    if srv.is_vrt:
        device = Device.objects.get(sn=srv.host.sn)
    else:
        device = Device.objects.get(sn=srv.sn)
    try:
        d_tp = device.tag.filter(level=DeviceLevel.objects.get(level="dtype"))[0]
        #设备类型
    except Exception, e:
        d_tp = None
    try:
        d_vd = device.tag.filter(level=DeviceLevel.objects.get(level="vendor"))[0]
        #设备品牌
    except Exception, e:
        d_vd = None
    try:
        d_prd = device.tag.filter(level=DeviceLevel.objects.get(level="prd"))[0]
        #设备型号
    except Exception, e:
        d_prd = None
    try:
        s_pdl = srv.tag.filter(level=SystemLevel.objects.get(level="pdl"))[0]
    except Exception, e:
        s_pdl = None
    try:
        s_sbs = srv.tag.filter(level=SystemLevel.objects.get(level="sbs"))[0]
    except Exception, e:
        s_sbs = None
    try:
        s_grp = srv.tag.filter(level=SystemLevel.objects.get(level="grp"))[0]
    except Exception, e:
        s_grp = None

    return render(request, "systemcenter/serverdetail.html", {"idcs": device, "srv": srv, "d_tp": d_tp, "d_vd": d_vd,
                                                              "d_prd": d_prd, "s_pdl": s_pdl, "s_sbs": s_sbs,
                                                              "s_grp": s_grp})


def serveredit(request, id):
    try:
        srv = ServerPool.objects.get(id=id)
    except ServerPool.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = ServerForm(request.POST, instance=srv)
        if form.is_valid():
            if request.user.has_perm("systemcenter.change_serverpool"):
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有编辑权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"sn": form['sn'].errors,
                                                                   "hostname": form['hostname'].errors,
                                                                   "os_type": form['os_type'].errors,
                                                                   "os_kernel": form['os_kernel'].errors,
                                                                   "os_release": form['os_release'].errors,
                                                                   "ip": form['ip'].errors,
                                                                   "oper": form['oper'].errors,
                                                                   "fronter": form['fronter'].errors,
                                                                   "dever": form['dever'].errors,
                                                                   "host": form['host'].errors,
                                                                   "tag": form['tag'].errors}}))
    else:
        form = ServerForm(instance=srv)
        return render(request, "systemcenter/serveredit.html", {"form": form})


def crtvrt(request, id):
    try:
        srv = ServerPool.objects.get(id=id)
    except ServerPool.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = ServerForm(request.POST)
        if form.is_valid():
            if request.user.has_perm("systemcenter.change_serverpool"):
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有编辑权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"sn": form['sn'].errors,
                                                                   "hostname": form['hostname'].errors,
                                                                   "os_type": form['os_type'].errors,
                                                                   "os_kernel": form['os_kernel'].errors,
                                                                   "os_release": form['os_release'].errors,
                                                                   "ip": form['ip'].errors,
                                                                   "oper": form['oper'].errors,
                                                                   "fronter": form['fronter'].errors,
                                                                   "dever": form['dever'].errors,
                                                                   "host": form['host'].errors,
                                                                   "tag": form['tag'].errors}}))
    else:
        form = ServerForm(initial={"host": srv, "is_vrt": True})
        #form.fields['host'].widget = forms.HiddenInput()
        #form['host'].field.queryset = ServerPool.objects.filter(id=id)
        #form.fields['host'].queryset = ServerPool.objects.filter(id=id)
        return render(request, "systemcenter/serveredit.html", {"form": form})


def servermonitor(request, id):
    from apps.monitorcenter.models import CactiHost
    if request.method == "GET":
        try:
            cacti = CactiHost.objects.get(name=u"系统监控")
            srv = ServerPool.objects.get(id=id)
            graph_id_list = srv.servermonitor_set.all()
            return render(request, "systemcenter/servermonitor.html", {"srv": srv, "graph_id_list": graph_id_list,
                                                                       "cacti": cacti})
        except ServerPool.DoesNotExist:
            raise Http404
    else:
        return Http404


def serverup(request, id):
    try:
        srv = ServerPool.objects.get(id=id)
    except ServerPool.DoesNotExist:
        raise Http404
    if request.is_ajax() and request.method == "GET":
        if srv.hostname and srv.ip:
            srv.status = "11"
            #更新主机状态为运行中
            srv.install = False
            #更新主机为不可重新装机
            srv.save()
            return HttpResponse(json.dumps({"code": 1}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"error": u"%s 缺少主机名或IP" % srv.sn}}))
    else:
        return HttpResponseBadRequest("<p>请求错误</p>")


def srvmaintain(request, id):
    try:
        srv = ServerPool.objects.get(id=id)
    except ServerPool.DoesNotExist:
        raise Http404

    if request.is_ajax() and request.method == "GET":
        if srv.status == "11":
            srv.status = "01"
            #更新主机状态为维护中
            srv.save()
            #do something
            return HttpResponse(json.dumps({"code": 1}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"error": u"%s 状态错误" % srv.sn}}))
    else:
        return HttpResponseBadRequest("<p>请求错误</p>")
#
##---------------------------------创建装机任务View-----------------------------------
#@login_required(login_url='/login')
#def osinstall(request):
#    u = request.user
#    if request.method == 'POST':
#        name = None
#        sn = None
#        ip = None
#        ostemplate = None
#        os_ip = ''
#        os_name = ''
#        os_template = ''
#        os_softs = ''
#        os_sn = ''
#        if request.POST['name']:
#            name = request.POST['name']
#        else:
#            os_name = u'请填写主机名'
#        try:
#            sn = get_object_or_404(Host, sn=request.POST['host_sn'])
#        except:
#            os_sn = u'获取SN错误'
#        if request.POST['ip']:
#            ip = request.POST['ip']
#        else:
#            os_ip = u'请选择IP'
#        try:
#            ostemplate = get_object_or_404(OsTemplate, id=request.POST['os_template'])
#        except:
#            os_template = u'获取模板错误'
#
#        if sn.status:
#            osinstall = u'请不要重复提交'
#            return HttpResponse(json.dumps({"code": 0, "message": {"name": os_name, "ip": os_ip, 'sn': os_sn,
#                                                                   "ostemplate": os_template,
#                                                                   "soft": os_softs, "osinstall": osinstall}}))
#        else:
#            if u.has_perm("networkcenter.add_osinstall", 'networkcenter.osinstall'):
#                try:
#                    osinstall = OsInstall(name=name, host=sn, ip=ip, os_template=ostemplate,
#                                          changed_by=User.objects.get(username=request.user))
#                    osinstall.save()
#                    Ip.objects.filter(ip=ip).update(status=True)
#                    if request.POST.getlist('soft'):
#                        softs = request.POST.getlist('soft')
#                        for soft in softs:
#                            osinstall.soft.add(OsSoft.objects.get(id=soft))
#                    sn.status = True
#                    sn.save()
#                    install_param = {'system_name': sn.sn, 'profile': ostemplate.name, 'ip': ip, 'mac': sn.mac,
#                                     'hostname': os_name}
#                    #os_install(install_param)
#                    return HttpResponse(json.dumps({"code": 1}))
#                except:
#                    return HttpResponse(json.dumps({"code": 0, "message": {"name": os_name, "ip": os_ip, 'sn': os_sn,
#                                                                           "ostemplate": os_template, "soft": os_softs,
#                                                                           }}))
#            else:
#                auth = u'没有安装权限'
#                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
#    else:
#        return HttpResponse("<script> alert('" + u'请求方式不对，亲～～' + "');window.location.href='/networkcenter/hostlist'</script>")
#
##----------------------------------创建装机任务View end--------------------------
#
#
##----------------------------------执行装机View---------------------------------
#@login_required(login_url='/login')
#def osinstallaction(request):
#    u = request.user
#    osinstall_list = OsInstall.objects.filter(status_id='00')
#    install_param = {}
#    if osinstall_list.count() != 0:
#        if u.has_perm("networkcenter.change_osinstall", 'networkcenter.osinstall'):
#            try:
#                for os in osinstall_list:
#                    install_param[os.id] = {'system_name': os.host.sn, 'profile': os.os_template.name,
#                                            'ilo': os.host.ip_ilo.ip}
#                    os.status_id = '01'
#                    os.save()
#                    os_install_action(install_param)
#                    return HttpResponse(json.dumps({"code": 1, }))
#            except:
#                return HttpResponse(json.dumps({"code": 0, }))
#        else:
#            auth = u'没有安装权限'
#            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
#    else:
#        return HttpResponse(json.dumps({"code": 2, }))
#
##---------------------------------执行装机View end------------------------------
#
#
##---------------------------------装机任务撤销View-------------------------------
#@login_required(login_url='/login')
#def osinstallcancel(request, id):
#    u = request.user
#    if u.has_perm("networkcenter.change_osinstall", 'networkcenter.osinstall'):
#        osinstall = OsInstall.objects.get(id=id)
#        Ip.objects.filter(ip=osinstall.ip).update(status=False)
#        Host.objects.filter(sn=osinstall.host.sn).update(status=False)
#        osinstall.status = True
#        osinstall.status_id = '10'
#        osinstall.save()
#        return HttpResponse(json.dumps({"code": 1, }))
#    else:
#        auth = u'没有删除权限'
#        return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
#    #except:
#    #    return HttpResponse(json.dumps({"code": 0, }))
#
##---------------------------------装机任务撤销View end-------------------------------
#
#
##----------------------------------获取装机进度View----------------------------------
#@login_required(login_url='/login')
#def installprogress(request, id):
#    try:
#        hostinstall = get_object_or_404(OsInstall, id=id)
#        job_list = []
#        job_dic = {'job_percent': hostinstall.progress}
#        job_list.append(job_dic)
#        result = json.dumps(job_list)
#        return HttpResponse(result)
#    except:
#        return HttpResponse('error')
#
##----------------------------------装机进度View end---------------------------------
#
#
##----------------------------------主机上线View-------------------------------------
#@login_required(login_url='/login')
#def hostonline(request):
#    global host_group_list, owner_list, business_list
#    u = request.user
#    if request.method == 'POST':
#        host = None
#        eth0 = None
#        host_group = None
#        business = None
#        users = None
#        host_id = ''
#        online_host_group = ''
#        online_business = ''
#        online_users = ''
#        online = ''
#        host_name_error = ''
#        hostapp_error = ''
#        try:
#            host = get_object_or_404(OsInstall, id=request.POST['host_id'])
#            eth0 = get_object_or_404(Ip, ip=host.ip)
#        except:
#            host_id = u'未找到主机'
#        host_name = request.POST['name']
#        try:
#            host_group_list = get_object_or_404(HostGroup, id=request.POST['host_group'])
#        except:
#            online_host_group = u'请选择主机组'
#        if request.POST.getlist('business'):
#            business_list = request.POST.getlist('business')
#        else:
#            online_business = u'请选择业务线'
#        if request.POST.getlist('owner'):
#            owner_list = request.POST.getlist('owner')
#        else:
#            online_users = u'请选择负责人'
#        find_name = HostApp.objects.filter(name=host_name)
#        find_hostapp = HostApp.objects.filter(host=host.host)
#        if find_name.count() != 0:
#            host_name_error = u'主机名重复'
#            return HttpResponse(json.dumps({"code": 0, "message": {"name_error": host_name_error, }}))
#        if find_hostapp.count() != 0:
#            hostapp_error = u'主机已存在'
#            return HttpResponse(json.dumps({"code": 0, "message": {"hostapp_error": hostapp_error, }}))
#        if u.has_perm("networkcenter.add_hostapp", 'networkcenter.hostapp'):
#            try:
#                hostapp = HostApp(name=host_name, host=host.host, ip_eth0=eth0, host_group=host_group_list,
#                                  changed_by=User.objects.get(username=request.user))
#                hostapp.save()
#                host.status = True
#                host.changed_by = User.objects.get(username=request.user)
#                host.save()
#                #for business add
#                for business in business_list:
#                    hostapp.business.add(Business.objects.get(id=business))
#                    #for owner add
#                for user in owner_list:
#                    hostapp.owner.add(User.objects.get(id=user))
#            except:
#                online = u'上线失败'
#                return HttpResponse(json.dumps({"code": 0, "message": {"host_id": host_id, "hostgroup": online_host_group,
#                                                                       'business': online_business, "users": online_users,
#                                                                       "online": online, }}))
#            return HttpResponse(json.dumps({"code": 1, }))
#        else:
#            auth = u'没有删除权限'
#            return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
#    else:
#        return HttpResponse(
#            "<script> alert('" + u'请求方式不对，亲～～' + "');window.location.href='/networkcenter/osinstalllist'</script>")
#
##----------------------------主机上线View end--------------------------------------
#
#
##----------------------------For Search Api---------------------------------------
#def searchip(request):
#    index = 'networkcenter'
#    order_type = request.GET.get('order_type', 'id')
#    search_var = request.GET.get('search_var')
#    username = request.user.first_name
#    form = IpForm()
#    iprangform = IpRangForm()
#    ip_list = None
#    if request.method == 'GET':
#        try:
#            ip_list = page(request, Ip.objects.filter(ip__istartswith=search_var).order_by(order_type))
#            return render_to_response('networkcenter/iplist.html',
#                                      {'index': index, 'idcs': ip_list, 'form': form, 'ip_form': iprangform,
#                                       'username': username, "order_type": order_type, "search_var": search_var},
#                                      context_instance=RequestContext(request))
#        except:
#            pass
#            return render_to_response('networkcenter/iplist.html',
#                                      {'index': index, 'idcs': ip_list, 'form': form, 'ip_form': iprangform,
#                                       'username': username, "order_type": order_type},
#                                      context_instance=RequestContext(request))
#
#
#def searchhost(request):
#    index = 'networkcenter'
#    order_type = request.GET.get('order_type', 'id')
#    if request.method == 'GET':
#        search_var = request.GET.get('search_var')
#        username = request.user.first_name
#        form = HostForm(initial={})
#        form_installos = OsInstallForm(initial={})
#        host = None
#        try:
#            ip = Ip.objects.get(ip=search_var)
#        except:
#            pass
#            ip = None
#        try:
#            host = Host.objects.filter(Q(sn=search_var) | Q(ip_ilo=ip)).order_by(order_type)
#            return render_to_response('networkcenter/serverpool.html',
#                                      {'index': index, 'idcs': host, 'form': form, 'form_os': form_installos,
#                                       'username': username, "order_type": order_type},
#                                      context_instance=RequestContext(request))
#        except:
#            pass
#            return render_to_response('networkcenter/serverpool.html',
#                                      {'index': index, 'idcs': host, 'form': form, 'form_os': form_installos,
#                                       'username': username, "order_type": order_type},
#                                      context_instance=RequestContext(request))
#
#
#def searchhostapp(request):
#    index = 'networkcenter'
#    order_type = request.GET.get('order_type', 'id')
#    if request.method == 'GET':
#        search_var = request.GET.get('search_var')
#        username = request.user.first_name
#        add_hostapp_form = HostAppForm()
#        virtual_form = HostVirtualForm()
#        hostapp = None
#        try:
#            ip = Ip.objects.get(ip=search_var)
#        except:
#            pass
#            ip = None
#        try:
#            hostapp = HostApp.objects.filter(Q(name=search_var) | Q(ip_eth0=ip))
#            return render_to_response('networkcenter/hostapplist.html', {'index': index, 'idcs': hostapp,
#                                                                  'form': add_hostapp_form,
#                                                                  'virtual_form': virtual_form,
#                                                                  'username': username,
#                                                                  'order_type': order_type},
#                                      context_instance=RequestContext(request))
#        except:
#            pass
#            return render_to_response('networkcenter/hostapplist.html', {'index': index, 'idcs': hostapp,
#                                                                  'form': add_hostapp_form,
#                                                                  'virtual_form': virtual_form,
#                                                                  'username': username,
#                                                                  'order_type': order_type},
#                                      context_instance=RequestContext(request))
#
#
#def searchhostvirtual(request):
#    index = 'networkcenter'
#    order_type = request.GET.get('order_type', 'id')
#    if request.method == 'GET':
#        search_var = request.GET.get('search_var')
#        username = request.user.first_name
#        form = HostVirtualForm()
#        hostvirtual = None
#        try:
#            ip = Ip.objects.get(ip=search_var)
#        except:
#            pass
#            ip = None
#        try:
#            hostvirtual = HostVirtual.objects.filter(Q(name=search_var) | Q(ip_one=ip))
#            return render_to_response('networkcenter/hostvirtuallist.html', {'index': index, 'idcs': hostvirtual,
#                                                                      'form': form, 'username': username,
#                                                                      'order_type': order_type},
#                                      context_instance=RequestContext(request))
#        except:
#            pass
#            return render_to_response('networkcenter/hostvirtuallist.html', {'index': index, 'idcs': hostvirtual,
#                                                                      'form': form, 'username': username,
#                                                                      'order_type': order_type},
#                                      context_instance=RequestContext(request))
#
#
#def searchrack(request):
#    index = 'networkcenter'
#    order_type = request.GET.get('order_type', 'id')
#    search_var = request.GET.get('search_var')
#    username = request.user.first_name
#    form = RackForm()
#    rack_list = None
#    if request.method == 'GET':
#        try:
#            rack_list = page(request, Rack.objects.filter(name__istartswith=search_var).order_by(order_type))
#            return render_to_response('networkcenter/racklist.html.bak', {'index': index, 'idcs': rack_list, 'form': form,
#                                                               'username': username, "order_type": order_type,
#                                                               "search_var": search_var},
#                                      context_instance=RequestContext(request))
#        except:
#            pass
#            return render_to_response('networkcenter/racklist.html.bak', {'index': index, 'idcs': rack_list, 'form': form,
#                                                               'username': username, "order_type": order_type},
#                                      context_instance=RequestContext(request))
#
#
