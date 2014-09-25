__author__ = 's7eph4ni3'
#coding=utf-8
import re
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password


class LoginForm(forms.Form):
    username = forms.CharField(label=u"用户名", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', }))
    password = forms.CharField(label=u"密码", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', }))


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'groups']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['username'].error_messages = {'required': u'请填写登录帐号'}
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['email'].error_messages = {'invalid': u'邮箱格式错误'}
        self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
        self.fields['password'].error_messages = {'required': u'请填写密码'}
        self.fields['groups'].widget = forms.SelectMultiple(attrs={'class': 'form-control', },
                                                            choices=self.fields['groups'].choices)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].widget.attrs['readonly'] = 'readonly'

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if re.match(r'^(1(([35][0-9])|(47)|[8][01236789]))\d{8}$', data):
            return self.cleaned_data['last_name']
        else:
            raise forms.ValidationError(u'手机号不正确')

    def clean_first_name(self):
        if not self.cleaned_data['first_name']:
            raise forms.ValidationError(u'姓名不能为空')
        else:
            return self.cleaned_data['first_name']

    def clean_password(self):
        if self.instance and self.cleaned_data["password"] == self.instance.password:
            return self.cleaned_data['password']
        else:
            self.cleaned_data['password'] = make_password(self.cleaned_data['password'])
            return self.cleaned_data['password']

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class GroupForm(ModelForm):
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['permissions_old'] = forms.CharField(widget=forms.SelectMultiple(
            choices=self.get_groups_perm_old_choices(),  attrs={'class': 'form-control', 'id': 'id_permissions_from',
                                                                'style': 'height:300px;width:350px'}), required=False)
        #  custom field permissions_old and can set null
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['name'].error_messages = {'required': u'请填写权限组'}
        self.fields['permissions'].widget = forms.SelectMultiple(attrs={'class': 'form-control',
                                                                        'style': 'height:300px;width:350px',
                                                                        'id': 'id_permissions_to'},
                                                                 choices=self.get_groups_perm_choices())

    def get_groups_perm_old_choices(self):
        obj_list = ['idc', 'rack', 'ip adress', 'user', 'device', 'permission', 'group', 'ip section',
                    'os install queue', 'cacti host', 'server pool']
        perms_list = []
        perms = ContentType.objects.filter(name__in=obj_list)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            for perm in perms:
                perms_list += perm.permission_set.all()
            group_perms = instance.permissions.all()
            choices_set = list(set(perms_list).difference(set(group_perms)))
            choices = [(p.id, p) for p in choices_set]
        else:
            for perm in perms:
                perms_list += perm.permission_set.all()
            choices = [(p.id, p) for p in perms_list]
        return choices

    def get_groups_perm_choices(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            group_perms = instance.permissions.all()
            choices = [(p.id, p) for p in group_perms]
            #choices = self.fields['permissions'].choices
        else:
            choices = ''
        return choices