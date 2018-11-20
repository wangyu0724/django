# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models.aggregates import Count
from logging import logging
_logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
	return render(request,"index.html")

# 登录操作
def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			request.session['user'] = username
			response = HttpResponseRedirect('/event_manage/')
			return response
		# if username == 'admin' and password == '123':
		# 	response = HttpResponseRedirect('/event_manage/')
		# 	# response.set_cookie('user',username,3600) #添加浏览器cookie,不安全，故将cookie换成session
		# 	request.session['user'] = username #将session信息记录到浏览器
		# 	return response
		else:
			return render(request,'index.html',{'error':'username or password error!'})

# 发布会管理
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '')  # 读取浏览器session
    line = Guest.objects.filter(sign=True)
    guest_list = Event.objects.filter(guest__sign=True).annotate(num_events=Count('guest'))
    _logger.info('*****%s'%guest_list)
    all_info = zip(event_list,[x.num_events for x in guest_list])
    return render(request, "event_manage.html", {"user": username, "events": all_info})



# 根据名称搜索发布会
@login_required
def search_name(request):
	username = request.session.get('user','')
	search_name = request.GET.get('name','')
	event_list = Event.objects.filter(name__contains=search_name)
	return render(request,'event_manage.html',{'user':username,'events':event_list})

# 分页显示嘉宾
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(guest_list, 20)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})

# 分页搜索嘉宾
@login_required
def search_guest(request):
    username = request.session.get('user','')
    search_phone = request.GET.get('phone','')
    guest_list = Guest.objects.filter(phone__contains=search_phone)
    paginator = Paginator(guest_list,20)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,'guests':contacts,'phone':search_phone})

# 签到页面
@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)
    line = Guest.objects.filter(sign=True,event_id=eid)
    guest = Guest.objects.filter(event_id=eid)
    return render(request,'sign_index.html',{'event':event,'sign':len(line),'guest_sign':len(guest)})

# 前端签到页面
def sign_index2(request,event_id):
    event_name = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index2.html',{'eventId': event_id,'eventNanme': event_name})

# 签到动作
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id=eid)
    guest_list = Guest.objects.filter(event_id=eid)
    guest_data = str(len(guest_list))
    sign_data = 0   #计算发布会“已签到”的数量
    for guest in guest_list:
        if guest.sign == True:
            sign_data += 1
    phone = request.POST.get('phone','')
    print phone
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error.','guest_sign':guest_data,'sign':sign_data})
    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.','guest_sign':guest_data,'sign':sign_data})
    result = Guest.objects.get(phone=phone,event_id=eid)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'user has sign in.','guest_sign':guest_data,'sign':sign_data})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success.','guest':result,'guest_sign':guest_data,'sign':str(int(sign_data)+1)})

# 登出
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response