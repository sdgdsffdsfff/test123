#!/usr/bin/env python
#coding=utf8
__author__ = 's7eph4ni3'
from django import forms
from django.forms import ModelForm
from apps.monitorcenter.models import *


class CactiHostForm(ModelForm):
    class Meta:
        model = CactiHost

    def __init__(self, *args, **kwargs):
        super(CactiHostForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['host'].widget = forms.TextInput(attrs={'class': 'form-control'})


class GraphsGroupForm(ModelForm):
    class Meta:
        model = GraphsGroup

    def __init__(self, *args, **kwargs):
        super(GraphsGroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['graph_id'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['cacti_host'].widget = forms.Select(attrs={'class': 'form-control', },
                                                        choices=self.fields['cacti_host'].choices)


class OrdersFailTypeForm(ModelForm):
    class Meta:
        model = OrdersFailType

    def __init__(self, *args, **kwargs):
        super(OrdersFailTypeForm, self).__init__(*args, **kwargs)
        self.fields['type_id'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['remask'].widget = forms.TextInput(attrs={'class': 'form-control'})


class OrdersFailNumHourForm(ModelForm):
    class Meta:
        model = OrdersFailNumHour

    def __init__(self, *args, **kwargs):
        super(OrdersFailNumHourForm, self).__init__(*args, **kwargs)
        self.fields['record_time'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['fail_type'].widget = forms.Select(attrs={'class': 'form-control', },
                                                       choices=self.fields['fail_type'].choices)
        self.fields['order_num'].widget = forms.TextInput(attrs={'class': 'form-control'})