#coding=utf8
__author__ = 's7eph4ni3'

import json
import copy
import datetime
import xlrd
import xlwt
from itertools import chain
from gearman import GearmanClient
from django.db.models import Q
from django import forms
from django.forms import CheckboxInput
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.html import conditional_escape, format_html, format_html_join
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.safestring import mark_safe
import sys

reload(sys)
sys.setdefaultencoding('utf8')


#------------分页函数封装----------------------------------
def page(request, result):
    p = Paginator(result, 10)
    try:
        page_num = int(request.GET.get('page', '1'))
    except ValueError:
        page_num = 1
    try:
        result = p.page(page_num)
    except(EmptyPage, InvalidPage):
        result = p.page(p.num_pages)
    return result

#---------------------------------------------------------


#--------------------------分布式装机服务-------------------
def os_install(server, install_param):
    gearman_client = GearmanClient(['%s:7070'] % server)
    gearman_client.submit_job('install', json.dumps(install_param), background=True)
    return True


def os_install_action(install_param):
    gearman_client = GearmanClient(['10.1.102.50:7070'])
    gearman_client.submit_job('rsync', json.dumps(install_param), background=True)
    return True

#---------------------------------------------------------


#----------------功能函数----------------------------------
def update_ip_status(ip_id, status):
    from apps.networkcenter.models import IpAdress

    IpAdress.objects.filter(id=ip_id).update(status=status)


def update_devint_status(link_id, status):
    from apps.networkcenter.models import DeviceInerface

    DeviceInerface.objects.filter(id=link_id).update(status=status)


def update_position_status(position_id, status):
    from apps.networkcenter.models import Position

    Position.objects.filter(id=position_id).update(status=status)

#------------------------------------------------------------


#------------设备sava()重写-----------------------------------
def device_save(self, *args, **kwargs):
    from apps.networkcenter.models import Device

    if self.pk:
        device = Device.objects.get(pk=self.pk)
        if device.position and device.position != self.position:
            position_id = device.position.id
            update_position_status(position_id, False)
            if self.position:
                update_position_status(self.position.id, True)
        else:
            if self.position:
                update_position_status(self.position.id, True)

    else:
        if self.position:
            position_id = self.position.id
            update_position_status(position_id, True)

    super(Device, self).save(*args, **kwargs)


def deviceint_save(self, *args, **kwargs):
    from apps.networkcenter.models import DeviceNIC

    if self.pk:
        deviceint = DeviceNIC.objects.get(pk=self.pk)
        if deviceint.ip and self.ip:
            if deviceint.ip != self.ip:
                update_ip_status(deviceint.ip_id, False)
                update_ip_status(self.ip_id, True)
            else:
                update_ip_status(self.ip_id, True)
        else:
            if self.ip:
                update_ip_status(self.ip_id, True)
            if deviceint.ip:
                update_ip_status(deviceint.ip_id, False)
        if deviceint.link and self.link:
            if deviceint.link != self.link:
                update_devint_status(deviceint.link_id, False)
                update_devint_status(self.link_id, True)
            else:
                update_devint_status(self.link_id, True)
        else:
            if self.link:
                update_devint_status(self.link_id, True)
            if deviceint.link:
                update_devint_status(deviceint.link_id, False)
    else:
        if self.ip:
            update_ip_status(self.ip_id, True)
        if self.link:
            update_devint_status(self.link_id, True)

    super(DeviceNIC, self).save(*args, **kwargs)


#----------------设备接口IP和连接过滤--------------
def device_ip_link_filter(self, *args, **kwargs):
    from apps.networkcenter.models import IpAdress, DeviceNIC

    if self.instance.id:
        # for ip
        if self.instance.ip_id:
            ip_list = IpAdress.objects.filter(
                Q(id=self.instance.ip_id) |
                Q(status=False)
            )
            ip_field = self.fields['ip'].widget
            ip_choices = list()
            ip_choices.append(('', '---------'))
            if ip_list:
                for ip in ip_list:
                    ip_choices.append((ip.id, ip))
                    ip_field.choices = ip_choices
            else:
                ip_field.choices = ip_choices
        else:
            ip_list = IpAdress.objects.filter(Q(status=False))
            ip_field = self.fields['ip'].widget
            ip_choices = list()
            ip_choices.append(('', '---------'))
            if ip_list:
                for ip in ip_list:
                    ip_choices.append((ip.id, ip))
                    ip_field.choices = ip_choices
            else:
                ip_field.choices = ip_choices
                # for link
        if self.instance.link_id:
            link_list = DeviceNIC.objects.filter(
                Q(id=self.instance.link_id) |
                Q(status=False)
            )
            link_field = self.fields['link'].widget
            link_choices = list()
            link_choices.append(('', '---------'))
            if link_list:
                for link in link_list:
                    link_choices.append((link.id, link))
                    link_field.choices = link_choices
            else:
                link_field.choices = link_choices
        else:
            link_list = DeviceNIC.objects.filter(Q(status=False))
            link_field = self.fields['link'].widget
            link_choices = list()
            link_choices.append(('', '---------'))
            if link_list:
                for link in link_list:
                    link_choices.append((link.id, link))
                    link_field.choices = link_choices
            else:
                link_field.choices = link_choices
    else:
        #for ip
        ip_list = IpAdress.objects.filter(Q(status=False))
        ip_field = self.fields['ip'].widget
        ip_choices = list()
        ip_choices.append(('', '---------'))
        if ip_list:
            for ip in ip_list:
                ip_choices.append((ip.id, ip))
                ip_field.choices = ip_choices
        else:
            ip_field.choices = ip_choices
            #fro link
        link_list = DeviceNIC.objects.filter(Q(status=False))
        link_field = self.fields['link'].widget
        link_choices = list()
        link_choices.append(('', '---------'))
        if link_list:
            for link in link_list:
                link_choices.append((link.id, link))
                link_field.choices = link_choices
        else:
            link_field.choices = link_choices


#----------------设备U位过滤-----------------------
def device_position_filter(self, *args, **kwargs):
    from apps.networkcenter.models import Position, Rack

    if self.instance.id:
        # for position
        if self.instance.position_id:
            position_list = Position.objects.filter(Q(id=self.instance.position_id) | Q(status=False)).filter(
                rack=self.instance.rack)
            position_field = self.fields['position'].widget
            position_choices = list()
            position_choices.append(('', '---------'))
            if position_list:
                for position in position_list:
                    position_choices.append((position.id, position.__unicode__()))
                    position_field.choices = position_choices
            else:
                position_field.choices = position_choices
        else:
            if self.instance.rack_id:
                position_list = Position.objects.filter(Q(status=False)).filter(rack=self.instance.rack)
            else:
                position_list = Position.objects.filter(Q(status=False))
            position_field = self.fields['position'].widget
            position_choices = list()
            position_choices.append(('', '---------'))
            if position_list:
                for position in position_list:
                    position_choices.append((position.id, position.__unicode__()))
                    position_field.choices = position_choices
            else:
                position_field.choices = position_choices

        # for rack
        if self.instance.rack_id:
            rack_list = Rack.objects.filter(Q(id=self.instance.rack_id) | Q(idc=self.instance.idc))
            rack_field = self.fields['rack'].widget
            rack_choices = list()
            rack_choices.append(('', '---------'))
            if rack_list:
                for rack in rack_list:
                    rack_choices.append((rack.id, rack.__unicode__()))
                rack_field.choices = rack_choices
            else:
                rack_field.choices = rack_choices
        else:
            if self.instance.idc_id:
                rack_list = Rack.objects.filter(Q(idc=self.instance.idc))
            else:
                rack_list = None
            rack_field = self.fields['rack'].widget
            rack_choices = list()
            rack_choices.append(('', '---------'))
            if rack_list:
                for rack in rack_list:
                    rack_choices.append((rack.id, rack.__unicode__()))
                rack_field.choices = rack_choices
            else:
                rack_field.choices = rack_choices

    else:
        position_list = Position.objects.filter(Q(status=False))
        position_field = self.fields['position'].widget
        position_choices = list()
        position_choices.append(('', '---------'))
        if position_list:
            for position in position_list:
                position_choices.append((position.id, position.__unicode__()))
                position_field.choices = position_choices
        else:
            position_field.choices = position_choices


#----------------------------------------------------------


def host_save(self, *args, **kwargs):
    from apps.networkcenter.models import Host, Ip

    if self.pk:
        host = Host.objects.get(pk=self.pk)

        if host.ip_ilo and host.ip_ilo != self.ip_ilo:
            ip = host.ip_ilo.ip
            update_ip_status(ip, False)
            update_ip_status(self.ip_ilo.ip, True)

        if host.position and host.position != self.position:
            position_id = host.position.id
            update_position_status(position_id, False)
            update_position_status(self.position.id, True)

    else:
        if self.ip_ilo:
            ip = self.ip_ilo.ip
            Ip.objects.filter(ip=ip).update(status=True)

        if self.position:
            position_id = self.position.id
            update_position_status(position_id, True)

    super(Host, self).save(*args, **kwargs)


def hostvirtual_ip_filter(self, *args, **kwargs):
    from apps.networkcenter.models import Ip

    if self.instance.id:
        #
        # for ip_one
        #
        if self.instance.ip_one_id:
            ip_one_list = Ip.objects.filter(
                Q(id=self.instance.ip_one_id) |
                Q(category='ip', status=False)
            )
            ip_one_field = self.fields['ip_one'].widget
            ip_one_choices = list()
            ip_one_choices.append(('', '---------'))
            if ip_one_list:
                for ip_one in ip_one_list:
                    ip_one_choices.append((ip_one.id, ip_one.ip))
                    ip_one_field.choices = ip_one_choices
            else:
                ip_one_field.choices = ip_one_choices
        else:
            ip_one_list = Ip.objects.filter(
                Q(category='ip', status=False)
            )
            ip_one_field = self.fields['ip_one'].widget
            ip_one_choices = list()
            ip_one_choices.append(('', '---------'))
            if ip_one_list:
                for ip_one in ip_one_list:
                    ip_one_choices.append((ip_one.id, ip_one.ip))
                    ip_one_field.choices = ip_one_choices
            else:
                ip_one_field.choices = ip_one_choices

        #
        # for ip_two
        #
        if self.instance.ip_two_id:
            ip_two_list = Ip.objects.filter(
                Q(id=self.instance.ip_two_id) |
                Q(category='ip', status=False)
            )
            ip_two_field = self.fields['ip_two'].widget
            ip_two_choices = list()
            ip_two_choices.append(('', '---------'))
            if ip_two_list:
                for ip_two in ip_two_list:
                    ip_two_choices.append((ip_two.id, ip_two.ip))
                    ip_two_field.choices = ip_two_choices
            else:
                ip_two_field.choices = ip_two_choices
        else:
            ip_two_list = Ip.objects.filter(
                Q(category='ip', status=False)
            )
            ip_two_field = self.fields['ip_two'].widget
            ip_two_choices = list()
            ip_two_choices.append(('', '---------'))
            if ip_two_list:
                for ip_two in ip_two_list:
                    ip_two_choices.append((ip_two.id, ip_two.ip))
                    ip_two_field.choices = ip_two_choices
            else:
                ip_two_field.choices = ip_two_choices

    else:
        #
        # for ip_one
        #
        ip_one_list = Ip.objects.filter(
            Q(category='ip', status=False)
        )
        ip_one_field = self.fields['ip_one'].widget
        ip_one_choices = list()
        ip_one_choices.append(('', '---------'))
        if ip_one_list:
            for ip_one in ip_one_list:
                ip_one_choices.append((ip_one.id, ip_one.ip))
                ip_one_field.choices = ip_one_choices
        else:
            ip_one_field.choices = ip_one_choices

        #
        # for ip_two
        #
        ip_two_list = Ip.objects.filter(
            Q(category='ip', status=False)
        )
        ip_two_field = self.fields['ip_two'].widget
        ip_two_choices = list()
        ip_two_choices.append(('', '---------'))
        if ip_two_list:
            for ip_two in ip_two_list:
                ip_two_choices.append((ip_two.id, ip_two.ip))
                ip_two_field.choices = ip_two_choices
        else:
            ip_two_field.choices = ip_two_choices


def save_history(form, request):
    changed = form.save(commit=False)
    changed.changed_by = User.objects.get(username=request.user)
    changed = changed.save()
    return changed


def ip2host(ip):
    if ip.status:
        device = ip.deviceinerface.device
    else:
        device = None
    return device


def importexcel(request):
    from apps.networkcenter.models import DeviceLevel, DeviceTag, Device, DeviceNIC, IDC, Rack, Position, IpSection, \
        IpAdress

    xls = 'upload/myexcel/%s.xlsx' % (request.user.username,)
    data = xlrd.open_workbook(xls)
    table = data.sheet_by_name(u'device')
    rows_num = table.nrows
    # print type(table.row_values(8)[14])
    # print datetime.date.fromordinal(datetime.date(1899,12,31).toordinal()-1+int(40712.0)).strftime("%Y-%m-%d")
    for i in range(1, rows_num):
        tag_list = []
        d = table.row_values(i)
        try:
            devicetype = DeviceTag.objects.get(remask=d[0])
            tag_list.append(devicetype)
        except DeviceTag.DoesNotExist:
            pass
        try:
            devicebrands = DeviceTag.objects.get(tag__icontains=d[2])
            tag_list.append(devicebrands)
        except DeviceTag.DoesNotExist:
            pass
        try:
            devicemodel = DeviceTag.objects.get(tag__icontains=d[3])
            tag_list.append(devicemodel)
        except DeviceTag.DoesNotExist:
            pass
        try:
            idc = IDC.objects.get_or_create(name=d[4])[0]
        except DeviceTag.DoesNotExist:
            idc = None
        try:
            idc_tag = DeviceTag.objects.get(remask=d[4])
            tag_list.append(idc_tag)
        except DeviceTag.DoesNotExist:
            pass
        if idc and d[5]:
            rack = Rack.objects.get_or_create(name=str(d[5]), idc=idc)[0]
            if d[6]:
                if type(d[6]) is float:
                    p_s = int(d[6])
                else:
                    p_s = str(d[6])
                pos = Position.objects.get_or_create(name=p_s, rack=rack)[0]
            else:
                pos = None
        else:
            rack = None
            pos = None
        if idc and d[7]:
            try:
                ip_sec = '%s.%s.%s.1/24' % (d[7].split('.')[0], d[7].split('.')[1], d[7].split('.')[2])
            except:
                ip_sec = None
            if ip_sec:
                try:
                    ipsec = IpSection.objects.get_or_create(name=ip_sec, idc=idc)[0]
                    ip = IpAdress.objects.get_or_create(name=d[7], section=ipsec, idc=ipsec.idc, category='ip')[0]
                except Exception, e:
                    pass
            else:
                ip = None
        else:
            ip = None
        if idc and d[8]:
            try:
                iloip_sec = '%s.%s.%s.1/24' % (d[8].split('.')[0], d[8].split('.')[1], d[8].split('.')[2])
            except:
                iloip_sec = None
            if iloip_sec:
                try:
                    iloipsec = IpSection.objects.get_or_create(name=iloip_sec, idc=idc)[0]
                    iloip = IpAdress.objects.get_or_create(name=d[8], idc=idc, section=iloipsec, category='iLo')[0]
                except:
                    pass
            else:
                iloip = None
        else:
            iloip = None
        if d[9]:
            remark = d[9]
        else:
            remark = ''
        try:
            sp = DeviceTag.objects.get(remask=d[10])
            tag_list.append(sp)
        except DeviceTag.DoesNotExist:
            pass
        if d[11]:
            asset_id = d[11]
        else:
            asset_id = ''
        if d[12]:
            purchase_id = d[12]
        else:
            purchase_id = ''
        if d[13]:
            buy_price = int(d[13])
        else:
            buy_price = 1
        if d[14]:
            buy_time = datetime.date.fromordinal(datetime.date(1899, 12, 31).toordinal() - 1 + int(d[14])).strftime("%Y-%m-%d")
        else:
            buy_time = '2014-1-1'
        if d[15]:
            expired_time = datetime.date.fromordinal(datetime.date(1899, 12, 31).toordinal() - 1 + int(d[15])).strftime("%Y-%m-%d")
        else:
            expired_time = '2015-1-1'
            #if d[16] == 'Yes':
        #    d[16] = True
        #else:
        #    d[16] = False
        if d[1]:
            try:
                device = Device.objects.get(sn__icontains=d[1])
            except Exception, e:
                device = Device(sn=d[1])
            if idc:
                device.idc = idc
            if rack:
                device.rack = rack
            if pos:
                device.position = pos
            device.remark = remark
            device.asset_id = asset_id
            device.purchase_id = purchase_id
            device.buy_price = buy_price
            device.buy_time = buy_time
            device.expired_time = expired_time
            device.save()
            try:
                add_tag = list(set(tag_list) - set(device.tag.all()))
                minus_tag = list(set(device.tag.all()) - set(tag_list))
                device.tag.remove(*minus_tag)
                device.tag.add(*add_tag)
            except Exception, e:
                device.tag.add(*tag_list)
            if d[0] == u'服务器':
                try:
                    if ip and not ip.status:
                        devint = DeviceNIC.objects.get_or_create(name='bond0', device=device)[0]
                        devint.save()
                        devint.ip = ip
                        devint.save()
                except Exception, e:
                    pass
                try:
                    if iloip and not iloip.status:
                        deviloint = DeviceNIC.objects.get_or_create(name='ilo', device=device)[0]
                        deviloint.save()
                        deviloint.ip = iloip
                        deviloint.save()
                except Exception, e:
                    pass
            elif d[0] == u'交换机':
                try:
                    if ip and not ip.status:
                        devint = DeviceNIC.objects.get_or_create(name='vlan1', device=device)[0]
                        devint.save()
                        devint.ip = ip
                        devint.save()
                except Exception, e:
                    pass
                try:
                    if iloip and not iloip.status:
                        deviloint = DeviceNIC.objects.get_or_create(name='vlan1', device=device)[0]
                        deviloint.save()
                        deviloint.ip = iloip
                        deviloint.save()
                except Exception, e:
                    pass
            else:
                try:
                    if ip and not ip.status:
                        devint = DeviceNIC.objects.get_or_create(name='eth0', device=device)[0]
                        devint.save()
                        devint.ip = ip
                        devint.save()
                except Exception, e:
                    pass
    if device:
        return True
    else:
        return False


def get_tag(d, lv):
    from apps.networkcenter.models import DeviceLevel
    try:
        l = DeviceLevel.objects.get(level=lv)
    except Exception, e:
        l = None
    if l:
        try:
            t = d.tag.get(level=l).remask
        except Exception, e:
            t = None
    else:
        t = None
    return t


def exportexcel(request):
    from apps.networkcenter.models import Device, DeviceLevel

    col_num = 0
    xls = 'static/bootstrap/img/device.xls'
    file = xlwt.Workbook()
    table = file.add_sheet('device', cell_overwrite_ok=True)
    ip_col, iloip_col = table.col(10), table.col(11)
    buy_time_col, ex_time_col = table.col(17), table.col(18)
    ip_col.width = 256 * 16
    iloip_col.width = 256 * 16
    buy_time_col.width = 256 * 10
    ex_time_col.width = 256 * 10
    col_list = [u'设备类别', u'序列号', u'品牌', u'型号', u'机房', u'机柜', u'U位', u'IP', u'ilo', u'备注', u'供货商', u'资产编号', u'采购单号',
                u'购买单价', u'购买时间', u'过保时间']
    style = xlwt.XFStyle()
    # borders
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    borders.bottom_colour = 0x3A
    style.borders = borders
    # title
    titlestyle = copy.deepcopy(style)
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 5
    titlestyle.pattern = pattern
    # datetime
    datestyle = copy.deepcopy(style)
    datestyle.num_format_str = 'M/D/YY'

    for i in range(len(col_list)):
        table.write(0, i, col_list[i], style=titlestyle)
    device = Device.objects.all()
    for dev in device:
        col_num += 1
        table.write(col_num, 0, get_tag(dev, "dtype"), style=style)
        table.write(col_num, 1, dev.sn, style=style)
        table.write(col_num, 2, get_tag(dev, "vendor"), style=style)
        table.write(col_num, 3, get_tag(dev, "prd"), style=style)
        if dev.idc:
            table.write(col_num, 4, dev.idc.name, style=style)
        if dev.rack:
            table.write(col_num, 5, dev.rack.name, style=style)
        if dev.position:
            table.write(col_num, 6, dev.position.name, style=style)
        try:
            ip = dev.devicenic_set.get(name__in=["bond0", "eth0", "vlan"]).ip.name
        except Exception, e:
            ip = None
        try:
            ilo = dev.devicenic_set.get(name="ilo").ip.name
        except Exception, e:
            ilo = None
        table.write(col_num, 7, ip, style=style)
        table.write(col_num, 8, ilo, style=style)
        if dev.remark:
            table.write(col_num, 9, dev.remark, style=style)
        table.write(col_num, 10, get_tag(dev, "sp"), style=style)
        if dev.asset_id:
            table.write(col_num, 11, dev.asset_id, style=style)
        if dev.purchase_id:
            table.write(col_num, 12, dev.purchase_id, style=style)
        if dev.buy_price:
            table.write(col_num, 13, dev.buy_price, style=style)
        if dev.buy_time:
            table.write(col_num, 14, dev.buy_time, style=datestyle)
        if dev.expired_time:
            table.write(col_num, 15, dev.expired_time, style=datestyle)
    file.save(xls)


class MyCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['<div>']
        # Normalize to strings
        str_values = set([force_text(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = format_html(' for="{0}" class="checkbox-inline"', final_attrs['id'])
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_text(option_label)
            output.append(format_html('<label{0}>{1} <span>{2}</span></label>',
                                      label_for, rendered_cb, str(option_label)))
        output.append('</div>')
        return mark_safe('\n'.join(output))


def display_tree(trees, node_list):
    from apps.networkcenter.models import DeviceLevel

    tree_list = []
    if trees:
        tree = trees.pop()
        childrens = DeviceLevel.objects.get(level=tree).devicetag_set.all()
        if childrens:
            for ch in childrens:
                if not node_list:
                    tree_list.append({'id': "%s.%s" % (ch.level, ch.tag), 'text': ch.remask, 'children': node_list})
                elif trees:
                    tree_list.append({'id': "%s.%s" % (ch.level, ch.tag), "state": "closed", 'text': ch.remask,
                                      'children': node_list})
                else:
                    tree_list.append({'id': "%s.%s" % (ch.level, ch.tag), 'text': ch.remask, 'children': node_list})
        node_list = tree_list
        return display_tree(trees, node_list)
    else:
        return node_list


def get_device_ip(d, name):
    try:
        ip = d.devicenic_set.all().get(name=name).ip.name
    except Exception, e:
        ip = ""
    return ip


def get_device_mac(d):
    try:
        mac = d.devicenic_set.all().get(name='eth0').ip.name
    except Exception, e:
        mac = ""
    print mac
    return mac


def get_osinstall(sn):
    from apps.systemcenter.models import ServerPool
    try:
        install = ServerPool.objects.get(sn=sn).install
    except Exception, e:
        install = True
    return install