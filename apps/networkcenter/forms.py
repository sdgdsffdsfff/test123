#coding=utf-8
__author__ = 's7eph4ni3'
from netaddr import IPNetwork
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from guardian.shortcuts import get_perms_for_model, get_perms
from apps.networkcenter.shortcut import MyCheckboxSelectMultiple
from apps.networkcenter.models import *
from apps.networkcenter.shortcut import device_ip_link_filter, device_position_filter


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        exclude = ['two_dim_code', 'status', 'create_time']

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['sn'].label = u'序列号'
        self.fields['sn'].error_messages = {'required': u'请填序列号'}
        self.fields['idc'].label = u'机房'
        self.fields['rack'].label = u'机柜'
        self.fields['position'].label = u'U 位'
        self.fields['asset_id'].label = u'资产编号'
        self.fields['purchase_id'].label = u'采购单号'
        self.fields['buy_price'].label = u'购买单价'
        self.fields['buy_time'].label = u'购买时间'
        self.fields['expired_time'].label = u'过保时间'
        self.fields['remark'].label = u'备注'
        self.fields['buy_price'].error_messages = {'invalid': u'请输入一个整数'}
        self.fields['buy_time'].error_messages = {'invalid': u'时间格式: 2013-11-27'}
        self.fields['expired_time'].error_messages = {'invalid': u'时间格式: 2013-11-27'}
        #for filed add CSS class
        self.fields['sn'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['idc'].widget = forms.Select(attrs={'class': 'form-control', },
                                                 choices=self.fields['idc'].choices)
        self.fields['rack'].widget = forms.Select(attrs={'class': 'form-control', },
                                                  choices=self.fields['rack'].choices)
        self.fields['position'].widget = forms.Select(attrs={'class': 'form-control', },
                                                      choices=self.fields['position'].choices)
        self.fields['tag'].widget = MyCheckboxSelectMultiple(choices=self.fields['tag'].choices)
        self.fields['asset_id'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['purchase_id'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['buy_price'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['buy_time'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['expired_time'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['remark'].widget = forms.TextInput(attrs={'class': 'form-control'})
        device_position_filter(self)

    def clean_tag(self):
        self.__tags = []

        for tag in self.cleaned_data['tag']:
            if tag.level not in self.__tags:
                self.__tags.append(tag.level)
            else:
                raise forms.ValidationError(u"%s TAG重复" % tag.level.remask)
        return self.cleaned_data['tag']


class OSInstallQueueForm(ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = OSInstallQueue
        fields = ('sn', 'tp_type', "needs_user")

    def __init__(self, *args, **kwargs):
        super(OSInstallQueueForm, self).__init__(*args, **kwargs)
        self.fields['sn'].widget = forms.Textarea(attrs={'class': 'form-control'})
        self.fields['needs_user'].widget = forms.Select(attrs={'class': 'form-control', },
                                                        choices=self.fields['needs_user'].choices)
        self.fields['tp_type'].widget = forms.RadioSelect(attrs={'class': 'radio'},
                                                          choices=self.fields['tp_type'].choices)
        self.fields['needs_user'].error_messages = {'required': u'不能为空'}
        self.fields['sn'].error_messages = {'required': u'请填写'}

    def clean_description(self):
        self.description = self.cleaned_data["description"]
        if not self.description:
            raise forms.ValidationError(u"不能为空")
        else:
            return self.cleaned_data["description"]

    def clean_sn(self):
        self.sn = self.cleaned_data["sn"]
        for sn in [sn for sn in self.sn.split("\r\n") if sn != ""]:
            try:
                #判断提交的服务器SN是否录入CMDB
                d = Device.objects.get(sn=sn)
            except Exception, e:
                raise forms.ValidationError(u"%s 不存在" % sn)
            if d.status:
                    raise forms.ValidationError(u"%s 已分配" % sn)
        return self.cleaned_data["sn"]

    def save(self, commit=True):
        instance = super(OSInstallQueueForm, self).save(commit=False)
        return instance


class DeviceIntForm(ModelForm):
    class Meta:
        model = DeviceNIC
        exclude = ['status']

    def __init__(self, *args, **kwargs):
        super(DeviceIntForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'接口名'
        self.fields['name'].error_messages = {'required': u'填写接口名'}
        self.fields['device'].label = u'设备'
        self.fields['device'].error_messages = {'required': u'选择设备'}
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['device'].widget = forms.Select(attrs={'class': 'form-control', },
                                                    choices=self.fields['device'].choices)
        self.fields['product'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['vendor'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['speed'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['ip'].widget = forms.Select(attrs={'class': 'form-control', },
                                                choices=self.fields['ip'].choices)
        self.fields['mac'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['vlan'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['link'].widget = forms.Select(attrs={'class': 'form-control', },
                                                  choices=self.fields['link'].choices)
        self.fields['remark'].widget = forms.TextInput(attrs={'class': 'form-control'})
        device_ip_link_filter(self)


#class DeviceParaForm(forms.Form):
#    def __init__(self, devobj=None, *args, **kwargs):
#        super(DeviceParaForm, self).__init__(*args, **kwargs)
#        self.devobj = devobj
#        if self.devobj:
#            self.my_field = self.devobj.device_type.deviceparameter_set.all()
#            for para in self.my_field:
#                instance = DeviceParameterValue.objects.filter(device=self.devobj, device_para=para).count()
#                if instance:
#                    dev_val = DeviceParameterValue.objects.get(device=self.devobj, device_para=para)
#                    self.fields[para.name] = forms.CharField(max_length=50, label=getattr(para, 'desc', para.name),
#                                                             widget=forms.TextInput(attrs={'class': 'form-control'}),
#                                                             initial=dev_val.value)
#                else:
#                    self.fields[para.name] = forms.CharField(max_length=50, label=getattr(para, 'desc', para.name),
#                                                             widget=forms.TextInput(attrs={'class': 'form-control'}))
#
#    def save(self):
#        dev_val = None
#        if self.devobj:
#            for para in self.devobj.device_type.deviceparameter_set.all():
#                instance = DeviceParameterValue.objects.filter(device=self.devobj, device_para=para).count()
#                if instance:
#                    dev_val = DeviceParameterValue.objects.get(device=self.devobj, device_para=para)
#                    dev_val.value = self.data.get(para.name)
#                    dev_val.save()
#                else:
#                    dev_val = DeviceParameterValue(device=self.devobj, device_para=para,
#                                                   value=self.data.get(para.name))
#                    dev_val.save()
#        return dev_val
#
#


class IDCForm(ModelForm):
    class Meta:
        model = IDC
        fields = ('name', 'address', 'phone', 'mail', 'tag', 'remark',)

    def __init__(self, *args, **kwargs):
        super(IDCForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {'required': u'请填写机房名'}
        self.fields['mail'].error_messages = {'invalid': u'邮箱格式错误'}
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['phone'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['mail'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['tag'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['remark'].widget = forms.TextInput(attrs={'class': 'form-control'})
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            if instance.rack_set.count() > 0:
                self.fields['name'].widget.attrs['readonly'] = 'readonly'


class RackForm(ModelForm):
    class Meta:
        model = Rack
        fields = ('name', 'idc', 'tag', 'remark',)

    def __init__(self, *args, **kwargs):
        super(RackForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'机柜'
        self.fields['name'].error_messages = {'required': u'请填写机柜名'}
        self.fields['idc'].label = u'所属机房'
        self.fields['idc'].error_messages = {'required': u'请填选择机房'}
        self.fields['tag'].label = u'标签'
        self.fields['remark'].label = u'备注'
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control', })
        self.fields['idc'].widget = forms.Select(attrs={'class': 'form-control', },
                                                 choices=self.fields['idc'].choices)
        self.fields['tag'].widget = forms.TextInput(attrs={'class': 'form-control', })
        self.fields['remark'].widget = forms.TextInput(attrs={'class': 'form-control', })
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            if instance.device_set.count() > 0:
                self.fields['name'].widget.attrs['readonly'] = 'readonly'
                self.fields['idc'].widget = forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'},
                                                         choices=((instance.idc.id, instance.idc.name),))


class IpSectionForm(ModelForm):
    ip_cat = (('ip', 'os ip'), ('iLo', 'ilo ip'),)
    category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=ip_cat)

    class Meta:
        model = IpSection

    def __init__(self, *args, **kwargs):
        super(IpSectionForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'IP段'
        self.fields['name'].error_messages = {'required': u'请填写子网段'}
        self.fields['idc'].error_messages = {'required': u'请选择机房'}
        self.fields['remark'].label = u'备注'
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control', })
        self.fields['idc'].widget = forms.Select(attrs={'class': 'form-control', },
                                                 choices=self.fields['idc'].choices)
        self.fields['remark'].widget = forms.TextInput(attrs={'class': 'form-control', })

    def clean_name(self):
        self.ipnet = self.cleaned_data['name']
        try:
            IPNetwork(self.ipnet)
        except Exception, e:
            raise forms.ValidationError(u"子网格式错误")
        return self.cleaned_data['name']
        #class DomainForm(ModelForm):
        #    class Meta:
        #        model = Domain
        #
        #    def __init__(self, *args, **kwargs):
        #        super(DomainForm, self).__init__(*args, **kwargs)
        #        self.fields['name'].label = u'域名'
        #        self.fields['name'].error_messages = {'required': u'请填写域名'}
        #        self.fields['cop'].error_messages = {'required': u'请填写公司'}
        #        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        #        self.fields['cop'].widget = forms.Select(attrs={'class': 'form-control', },
        #                                                 choices=self.fields['cop'].choices)
        #        self.fields['registrar'].widget = forms.TextInput(attrs={'class': 'form-control'})
        #        self.fields['remark'].widget = forms.TextInput(attrs={'class': 'form-control'})
        #
        #
        #class DomainRecordForm(ModelForm):
        #    class Meta:
        #        model = DomainRecord
        #
        #    def __init__(self, *args, **kwargs):
        #        super(DomainRecordForm, self).__init__(*args, **kwargs)
        #        self.fields['name'].label = u'主机记录'
        #        self.fields['name'].error_messages = {'required': u'请填主机记录'}
        #        self.fields['domain'].error_messages = {'required': u'请填写域名'}
        #        self.fields['record_type'].error_messages = {'required': u'请填记录类型'}
        #        self.fields['record_value'].error_messages = {'required': u'请填记录值'}
        #        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        #        self.fields['domain'].widget = forms.Select(attrs={'class': 'form-control', },
        #                                                    choices=self.fields['domain'].choices)
        #        self.fields['record_type'].widget = forms.Select(attrs={'class': 'form-control', },
        #                                                         choices=self.fields['record_type'].choices)
        #        self.fields['record_value'].widget = forms.TextInput(attrs={'class': 'form-control'})
        #        self.fields['record_ttl'].widget = forms.TextInput(attrs={'class': 'form-control'})
        #        self.fields['remark'].widget = forms.TextInput(attrs={'class': 'form-control'})
        #
        #
        #class ObjUserPermForm(forms.Form):
        #    def __init__(self, obj, user_obj=None, *args, **kwargs):
        #        self.obj = obj
        #        self.user_obj = user_obj
        #        super(ObjUserPermForm, self).__init__(*args, **kwargs)
        #        self.fields['user'] = forms.CharField(max_length=3, widget=forms.Select(attrs={'class': 'form-control', },
        #                                                                                choices=self.get_user_choices()))
        #        self.fields['permissions'] = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={
        #            'class': 'form-control'}), choices=self.get_obj_perms_field_choices())
        #
        #    def get_obj_perms_field_choices(self):
        #        #返回模型实例相应具备的权限
        #        choices = [(p.codename, p.name) for p in get_perms_for_model(self.obj)]
        #        return choices
        #
        #    def get_user_choices(self):
        #        users = User.objects.all()[1:]
        #        user_choices = []
        #        if self.user_obj:
        #            #编辑实例用户对模型实例的权限,此处返回对应实例用户
        #            user_choices.append((self.user_obj.id, self.user_obj.first_name))
        #        else:
        #            #添加模型实例权限管理,获取所有用户列表
        #            for u in users:
        #                u_p_l = get_perms(u, self.obj)
        #                if not u_p_l:
        #                    user_choices.append((u.id, u.first_name))
        #        return user_choices
        #
        #
        #class ObjGroupsPermForm(forms.Form):
        #    def __init__(self, obj, group_obj=None, *args, **kwargs):
        #        self.obj = obj
        #        self.group_obj = group_obj
        #        super(ObjGroupsPermForm, self).__init__(*args, **kwargs)
        #        self.fields['groups'] = forms.CharField(max_length=3, widget=forms.Select(attrs={'class': 'form-control', },
        #                                                                                  choices=self.get_groups_choices()))
        #        self.fields['permissions'] = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={
        #            'class': 'form-control'}), choices=self.get_obj_perms_field_choices())
        #
        #    def get_obj_perms_field_choices(self):
        #        choices = [(p.codename, p.name) for p in get_perms_for_model(self.obj)]
        #        return choices
        #
        #    def get_groups_choices(self):
        #        groups = Group.objects.all()
        #        groups_choices = []
        #        if self.group_obj:
        #            groups_choices.append((self.group_obj.id, self.group_obj.name))
        #        else:
        #            for u in groups:
        #                g_p_l = get_perms(u, self.obj)
        #                if not g_p_l:
        #                    groups_choices.append((u.id, u.name))
        #        return groups_choices