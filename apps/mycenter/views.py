#coding=utf-8
import json
import requests
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from apps.mycenter.forms import LoginForm, UserForm, GroupForm


def _login(request, username, password):
    ret = False
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            auth_login(request, user)
            ret = True
        else:
            messages.add_message(request, messages.INFO, u'用户没有激活')
    else:
        messages.add_message(request, messages.INFO, u'用户名或密码错误')
    return ret


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST.copy())
        if form.is_valid():
            _login(request, form.cleaned_data["username"], form.cleaned_data["password"])
            return HttpResponseRedirect(reverse('profile'))
    return render_to_response("myprofile/login.html", {'form': form}, context_instance=RequestContext(request))


def index(request):
    if request.user.is_authenticated():
        username = request.user.username
        style = 'home'
        return render_to_response("myprofile/index.html", {'username': username, 'index': style},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('login'))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))


def profile(request):
    style = 'home'
    username = request.user.first_name
    return render(request, "myprofile/profile.html", {'index': style, 'username': username})


def profileedit(request):
    style = 'home'
    username = request.user.first_name
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({"code": 1}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"username": form['username'].errors,
                                                                   "first_name": form['first_name'].errors,
                                                                   "password": form['password'].errors,
                                                                   "email": form['email'].errors,
                                                                   "last_name": form['last_name'].errors}}))
    else:
        form = UserForm(instance=user,)
        return render(request, "myprofile/profileedit.html", {'form': form, 'index': style, 'username': username})


def userlist(request):
    style = 'home'
    username = request.user.first_name
    if request.method == 'GET':
        if request.user.has_perm("auth.add_user"):
            user_list = User.objects.all()[1:]
        else:
            user_list = []
        return render(request, "myprofile/userlist.html", {'users': user_list, 'index': style, 'username': username})
    else:
        raise Http404


def useradd(request):
    style = 'home'
    username = request.user.first_name
    u = request.user
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            if u.has_perm("auth.add_user", "auth.user"):
                form.save()
                form.save_m2m()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加用户权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"username": form['username'].errors,
                                                                   "first_name": form['first_name'].errors,
                                                                   "password": form['password'].errors,
                                                                   "email": form['email'].errors,
                                                                   "last_name": form['last_name'].errors}}))
    else:
        form = UserForm()
        return render(request, "myprofile/useradd.html", {'form': form, 'index': style, 'username': username})


def useredit(request, id):
    style = 'home'
    username = request.user.first_name
    user = User.objects.get(id=id)
    u = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            if u.has_perm("auth.change_user", "auth.user"):
                form.save()
                form.save_m2m()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有修改用户权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"username": form['username'].errors,
                                                                   "first_name": form['first_name'].errors,
                                                                   "password": form['password'].errors,
                                                                   "email": form['email'].errors,
                                                                   "last_name": form['last_name'].errors}}))
    else:
        form = UserForm(instance=user)
        return render(request, "myprofile/useredit.html", {'form': form, 'index': style, 'username': username})


def grouplist(request):
    style = 'home'
    username = request.user.first_name
    if request.method == 'GET':
        grouplist = Group.objects.all()
        return render(request, "myprofile/grouplist.html", {'groups': grouplist, 'index': style, 'username': username})
    else:
        raise Http404


def groupedit(request, id):
    style = 'home'
    username = request.user.first_name
    group = Group.objects.get(id=id)
    u = request.user
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            if u.has_perm("auth.change_group", "auth.group"):
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有修改用户组权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "permissions": form['permissions'].errors}}))
    else:
        form = GroupForm(instance=group)
        return render(request, "myprofile/groupedit.html", {'form': form, 'index': style, 'username': username})


def groupadd(request):
    style = 'home'
    username = request.user.first_name
    u = request.user
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            if u.has_perm("auth.add_group", "auth.group"):
                form.save()
                return HttpResponse(json.dumps({"code": 1}))
            else:
                auth = u'没有添加用户组权限'
                return HttpResponse(json.dumps({"code": 0, "message": {"auth": auth}}))
        else:
            return HttpResponse(json.dumps({"code": 0, "message": {"name": form['name'].errors,
                                                                   "permissions": form['permissions'].errors}}))
    else:
        form = GroupForm()
        return render(request, "myprofile/groupadd.html", {'form': form, 'index': style, 'username': username})


def oaquery(request):
    no = request.GET.get("no")
    st = request.GET.get("st")
    et = request.GET.get("et")
    url = "http://oa.lefeng.com/seeyon/common/ivendor/ClockInfo.jsp?no=%s&st=%s&et=%s" % (no, st, et)
    try:
        r = requests.get(url)
        return HttpResponse(json.dumps(r.json()))
    except Exception, e:
        return HttpResponse(json.dumps({u'result': u"200&{}"}))
