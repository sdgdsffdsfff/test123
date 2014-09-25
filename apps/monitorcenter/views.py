#coding=utf-8

import sh
import time, json
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from django.views.generic.base import View
from apps.monitorcenter.models import *
from apps.monitorcenter.forms import *
from apps.monitorcenter.shortcut import MyCal, monitor_system, get_chinamap_ping_data, get_alert_sms, \
    get_fail_order_hours, get_fail_order_week, get_order_time_line, get_tclv_hours
import datetime


def index(request):
    username = request.user.username
    style = 'monitor'
    pic_pool = [1, 2, 3, 4]  # when there is no alarm,display these
    now_stm = int(time.strftime("%s")) - 300
    cacti_pool = monitor_system(now_stm)
    node_pool = get_chinamap_ping_data(now_stm)
    alert_sms = get_alert_sms(now_stm)
    order_type_list = []
    try:
        order_type_list = [OrdersFailType.objects.get(type_id=i) for i in (0, 151, 152, 153, 20, 21)]
    except Exception, e:
        pass
    order_fail_hours_list, orders_pay_fail_hours_detail_list = get_fail_order_hours(order_type_list)
    cancel_order_week_list, order_pay_fail_week_list = get_fail_order_week(order_type_list)
    x_date, sub_order_list, cancel_order_list = get_order_time_line()
    tclv = json.dumps(get_tclv_hours())
    print tclv
    return render_to_response("monitorcenter/index.html", {'username': username, 'index': style, 'cacti': cacti_pool,
                                                           "pic_pool": pic_pool, "node_pool": node_pool,
                                                           "orders": json.dumps(order_fail_hours_list),
                                                           'x_date': json.dumps(x_date), 'alert_sms': alert_sms,
                                                           'sub_order_list': json.dumps(sub_order_list),
                                                           'cancel_order_list': json.dumps(cancel_order_list),
                                                           'cancel_order_week_list': json.dumps(
                                                               cancel_order_week_list),
                                                           'orders_pay_fail_list': orders_pay_fail_hours_detail_list,
                                                           'order_pay_fail_week_list': order_pay_fail_week_list,
                                                           "tclv": tclv},
                              context_instance=RequestContext(request))


def system(request):
    username = request.user.username
    style = 'system'
    cacti = CactiHost.objects.get(name=u'系统监控').graphsgroup_set.all().order_by('-id')
    system = GraphsGroup.objects.get(name=u'系统响应监控')
    return render_to_response("monitorcenter/system.html", {'username': username, 'index': style, 'system': system,
                                                            'cacti': cacti},
                              context_instance=RequestContext(request))


def sub_system(request, id):
    username = request.user.username
    style = 'system'
    cacti = CactiHost.objects.get(name=u'系统监控').graphsgroup_set.all().order_by('-id')
    system = GraphsGroup.objects.get(id=id)
    return render_to_response("monitorcenter/system.html", {'username': username, 'index': style, 'system': system,
                                                            'cacti': cacti},
                              context_instance=RequestContext(request))


def network(request):
    username = request.user.username
    style = 'network'
    cacti = CactiHost.objects.get(name=u'网络监控').graphsgroup_set.all().order_by('-id')
    network = GraphsGroup.objects.get(name=u'网络监控')
    return render_to_response("monitorcenter/network.html", {'username': username, 'index': style, 'system': network,
                                                             'cacti': cacti},
                              context_instance=RequestContext(request))


def sub_network(request, id):
    username = request.user.username
    style = 'network'
    cacti = CactiHost.objects.get(name=u'网络监控').graphsgroup_set.all().order_by('-id')
    network = GraphsGroup.objects.get(id=id)
    return render_to_response("monitorcenter/network.html", {'username': username, 'index': style, 'system': network,
                                                             'cacti': cacti},
                              context_instance=RequestContext(request))


def db(request):
    username = request.user.username
    style = 'db'
    cacti = CactiHost.objects.get(name=u'数据库监控').graphsgroup_set.all().order_by('-id')
    db = GraphsGroup.objects.get(name=u'oracle监控')
    return render_to_response("monitorcenter/db.html", {'username': username, 'index': style, 'system': db,
                                                        'cacti': cacti},
                              context_instance=RequestContext(request))


def sub_db(request, id):
    username = request.user.username
    style = 'db'
    cacti = CactiHost.objects.get(name=u'数据库监控').graphsgroup_set.all().order_by('-id')
    db = GraphsGroup.objects.get(id=id)
    return render_to_response("monitorcenter/db.html", {'username': username, 'index': style, 'system': db,
                                                        'cacti': cacti},
                              context_instance=RequestContext(request))


def zhiban(request):
    style = 'zhiban'
    mid = datetime.datetime.now().month
    #mid = 10
    did = datetime.datetime.now().day
    if int(mid) > 3:
        try:
            ShiftTable.objects.get_or_create(years='2014', month='4', shift_id=0)
            myshift = ShiftTable.objects.get(month=str(mid))
        except:
            pass
        if myshift:
            myshift_id = myshift.shift_id
            mycal = MyCal(did, i=myshift_id)
            zhibanbiao = mycal.formatmonth(2014, int(mid))
            next_shift_id = mycal.get()
            try:
                ShiftTable.objects.get_or_create(years='2014', month=str(mid + 1), shift_id=next_shift_id - 1)
            except:
                pass
            return render_to_response("monitorcenter/zhibanbiao.html", {'username': request.user.username, 'mid': mid,
                                                                        'index': style, 'zhiban': zhibanbiao},
                                      context_instance=RequestContext(request))
        else:
            errors = u'本月还没有值班表～～'
            return render_to_response("monitorcenter/zhibanbiao.html", {'username': request.user.username, 'mid': mid,
                                                                        'index': style, 'zhiban': errors},
                                      context_instance=RequestContext(request))
    else:
        errors = u'本月还没有值班表～～'
        return render_to_response("monitorcenter/zhibanbiao.html", {'username': request.user.username, 'mid': mid,
                                                                    'index': style, 'zhiban': errors},
                                  context_instance=RequestContext(request))
