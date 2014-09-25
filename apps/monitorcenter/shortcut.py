#coding=utf-8
__author__ = 's7eph4ni3'

import sh
import json
import calendar
import datetime
from django.db.models import Q
from django.db.models import Sum
from apps.monitorcenter.models import OrdersFailNumHour, OrdersFailType, City, Tclv


class MyCal(calendar.HTMLCalendar):
    """值班表生成"""

    def __init__(self, did, i=0, *args, **kwargs):
        super(MyCal, self).__init__(*args, **kwargs)
        self.i = i
        self.did = did
        self.xx = ['张勇', '高明', '刘海清','王学兵','郭灵通']

    def formatname(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        else:
            if self.i > 4:
                self.i = 0
            if day == self.did:
                self.i += 1
                return '<td class="%d" style="background-color: #ed9c28;">%s</td>' % (day, self.xx[self.i-1])
            else:
                self.i += 1
                return '<td class="%d">%s</td>' % (day, self.xx[self.i-1])

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            if day == self.did:
                return '<td class="%d" style="background-color: #ed9c28;">%d</td>' % (day, day)
            else:
                return '<td class="%d">%d</td>' % (day, day)

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        n = ''.join(self.formatname(d, wd, ) for (d, wd) in theweek)
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<tr>%s</tr><tr>%s</tr>' % (s, n)

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="table table-bordered table-striped">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def get(self):
        return self.i


def monitor_system(now_stm):
    system_pool = []
    system_log = []
    system_name = {'active': 30887, 'wservice': 30780, 'order': 31499, 'passport': 30592, 'pay': 31545,
                   'product': 30342, 'shopping': 29138, 'slist': 33027, 'track': 30779, 'tuan': 30778, 'wap_v5': 33008}
    try:
        system_log = list(sh.tail("-n5", "/var/log/shuffling.log"))
    except Exception, e:
        pass

    for log in system_log:
        if int(log.split()[0]) > now_stm:
            try:
                system_pool.append(system_name[log.split()[1]])
            except:
                pass

    return system_pool


def get_chinamap_ping_data(now_stm):
    ping_dic = {}
    ping_data = list(sh.tail("-n5", "/var/log/map_ping.log"))
    for ptm in ping_data:
        if int(ptm.split()[0]) > now_stm:
            try:
                ping_dic[ptm.split()[2].split('_')[3]] = {'type': ptm.split()[1], 'loss': ptm.split()[4],
                                                          'rtt': ptm.split()[6]}
            except:
                pass
    return json.dumps(ping_dic)


def get_alert_sms(now_stm):
    alert_sms = []
    sms_data = []
    try:
        sms_data = list(sh.tail("-n5", "/var/log/sms.log"))
    except Exception, e:
        pass
    for sms in sms_data:
        if int(sms.split()[0]) > now_stm:
            try:
                alert_sms.append(' '.join(sms.split()[1:]))
            except Exception, e:
                pass
    if not alert_sms:
        alert_sms.append(u'现在木有报警信息')
    return alert_sms


def get_fail_order_hours(order_type_list):
    """每小时订单失败分布"""
    ago_one_hour = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:00:00')
    ago_two_hour = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:00:00')
    order_fail_hours_list = []
    orders_pay_fail_hours_detail_list = []
    orders_pay_fail_hours_detail = []
    orders_pay_fail_sum = None
    orders = []
    try:
        orders = OrdersFailNumHour.objects.filter(~Q(fail_type__in=order_type_list) & Q(record_time=ago_one_hour))
        orders_pay_fail_sum = OrdersFailNumHour.objects.filter(
            Q(fail_type__in=order_type_list[1:]) & Q(record_time=ago_one_hour)).aggregate(Sum('order_num'))
        orders_pay_fail_hours_detail = OrdersFailNumHour.objects.filter(
            Q(fail_type__in=order_type_list[1:]) & Q(record_time=ago_one_hour))
    except Exception, e:
        pass
    if not orders:
        try:
            orders = OrdersFailNumHour.objects.filter(~Q(fail_type__in=order_type_list) & Q(record_time=ago_two_hour))
            orders_pay_fail_sum = OrdersFailNumHour.objects.filter(
                Q(fail_type__in=order_type_list[1:]) & Q(record_time=ago_two_hour)).aggregate(Sum('order_num'))
            orders_pay_fail_hours_detail = OrdersFailNumHour.objects.filter(
                Q(fail_type__in=order_type_list[1:]) & Q(record_time=ago_two_hour))
        except Exception, e:
            pass
    for order in orders:
        order_fail_hours_list.append(['%s' % order.fail_type.remask, order.order_num])
    if orders_pay_fail_sum:
        order_fail_hours_list.append([u'支付失败', orders_pay_fail_sum['order_num__sum']])
    for order_pay_fail in orders_pay_fail_hours_detail:
        orders_pay_fail_hours_detail_list.append([order_pay_fail.fail_type.remask, order_pay_fail.order_num])
    return order_fail_hours_list, orders_pay_fail_hours_detail_list


def get_fail_order_week(order_type_list):
    """最近一周失败订单分布"""
    cancel_order_week_list = []
    order_pay_fail_week_list = []
    st_week = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:00:00')
    cancel_order_week = OrdersFailNumHour.objects.filter(
        ~Q(fail_type__in=order_type_list) & Q(record_time__gte=st_week)).values('fail_type_id').annotate(
        order_all=Sum('order_num')).order_by('-order_all')
    order_pay_fail_week = OrdersFailNumHour.objects.filter(
        Q(fail_type__in=order_type_list[1:]) & Q(record_time__gte=st_week)).values('fail_type_id').annotate(
        order_all=Sum('order_num')).order_by('-order_all')
    order_pay_fail_week_sum = OrdersFailNumHour.objects.filter(
        Q(fail_type__in=order_type_list[1:]) & Q(record_time__gte=st_week)).aggregate(Sum('order_num'))
    cancel_order_week_list.append([u'支付失败', order_pay_fail_week_sum['order_num__sum']])

    for order_pay in order_pay_fail_week:
        #print cel_order
        try:
            order_type = OrdersFailType.objects.get(id=order_pay['fail_type_id'])
        except:
            pass
        if order_type:
            order_pay_fail_week_list.append(['%s' % order_type.remask, order_pay['order_all']])

    for cel_order in cancel_order_week:
        #print cel_order
        try:
            order_type = OrdersFailType.objects.get(id=cel_order['fail_type_id'])
        except:
            pass
        if order_type:
            cancel_order_week_list.append(['%s' % order_type.remask, cel_order['order_all']])

    return cancel_order_week_list, order_pay_fail_week_list


def get_order_time_line():
    """订单趋势图，x轴生成"""
    sub_order_list = []
    cancel_order_list = []
    sub_order_type = OrdersFailType.objects.get(type_id=0)
    x_date = [(datetime.datetime.now() - datetime.timedelta(hours=i)).hour for i in
              [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]]
    xx_date = [(datetime.datetime.now() - datetime.timedelta(hours=i)).strftime('%Y-%m-%d %H:00:00') for i in
               [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]]
    for d in xx_date:
        try:
            submit_order = OrdersFailNumHour.objects.filter(Q(fail_type=sub_order_type) & Q(record_time=d))
            if submit_order:
                sub_order_list.append(submit_order[0].order_num)
            else:
                sub_order_list.append(None)
        except Exception, e:
            pass
        try:
            cancel_order = OrdersFailNumHour.objects.filter(~Q(fail_type=sub_order_type) & Q(record_time=d)).aggregate(
                Sum('order_num')).get('order_num__sum')
            cancel_order_list.append(cancel_order)
        except Exception, e:
            pass
    return x_date, sub_order_list, cancel_order_list


def get_tclv_hours():
    """地区跳出率"""
    xx_date = [(datetime.datetime.now() - datetime.timedelta(hours=i)).strftime('%Y-%m-%d %H:00:00') for i in
               [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]]
    city_list = [u"北京市", u"上海市", u"广东省", u"辽宁省", u"江苏省", u"浙江省"]
    area_tclv = []
    for city in city_list:
        tclv_list = []
        try:
            city_obj = City.objects.get(name=city)
        except Exception, e:
            city_obj = None
        if city_obj:
            for d in xx_date:
                try:
                    tclv = Tclv.objects.get(Q(city=city_obj) & Q(record_time=d)).tclv
                    tclv_list.append(tclv)
                except Exception, e:
                    tclv_list.append(None)
            area_tclv.append({"name": city, "data": tclv_list})

    return area_tclv
