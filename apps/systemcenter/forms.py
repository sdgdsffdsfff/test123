#!/usr/bin/env python
#coding=utf8
__author__ = 's7eph4ni3'

from django import forms
from django.forms import ModelForm
from apps.networkcenter.models import IpAdress
from apps.systemcenter.models import ServerPool
from apps.networkcenter.shortcut import MyCheckboxSelectMultiple


class ServerForm(ModelForm):
    class Meta:
        model = ServerPool
        exclude = ['status', 'install', 'detect', 'collect']

    def __init__(self, *args, **kwargs):
        super(ServerForm, self).__init__(*args, **kwargs)
        self.fields['host'].label = u'宿主机'
        self.fields['sn'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['hostname'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['os_type'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['os_kernel'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['os_release'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['ip'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['oper'].widget = forms.Select(attrs={'class': 'form-control', },
                                                  choices=self.fields['oper'].choices)
        self.fields['fronter'].widget = forms.Select(attrs={'class': 'form-control', },
                                                     choices=self.fields['fronter'].choices)
        self.fields['dever'].widget = forms.Select(attrs={'class': 'form-control', },
                                                   choices=self.fields['dever'].choices)
        self.fields['host'].widget = forms.Select(attrs={'class': 'form-control', },
                                                  choices=self.fields['host'].choices)
        self.fields['is_vrt'].widget = forms.NullBooleanSelect(attrs={'class': 'form-control'})
        self.fields['tag'].widget = MyCheckboxSelectMultiple(choices=self.fields['tag'].choices)

    def clean_tag(self):
        self.__tags = []

        for tag in self.cleaned_data['tag']:
            if tag.level not in self.__tags:
                self.__tags.append(tag.level)
            else:
                raise forms.ValidationError(u"%s TAG重复" % tag.level.remask)
        return self.cleaned_data['tag']

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        try:
            IpAdress.objects.get(name=ip)
            return self.cleaned_data['ip']
        except IpAdress.DoesNotExist:
            raise forms.ValidationError(u"ip不存在")
