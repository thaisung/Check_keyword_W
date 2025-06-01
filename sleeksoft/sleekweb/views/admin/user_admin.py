from ...models import *

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator


from django.http import HttpResponse
import requests
import time

from django.db import models
from django.utils import timezone

import os

from datetime import datetime

from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from datetime import datetime
from django.contrib import messages
import random
import string
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

# from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

import random
import string

import base64

import time
from django.http import JsonResponse

import re
import json

from django.conf import settings
from django.db.models import Q

import datetime

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


import base64
import uuid




    
def user_admin(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
            context = {}
            lc = request.COOKIES.get('language') or 'en'
            context['domain'] = settings.DOMAIN
            if request.user.is_authenticated and request.user.is_superuser:
                context['list_User'] = User.objects.all()
                # s = request.GET.get('s')
                # f = request.GET.get('f')
                # f1 = request.GET.get('f1')
                # if s:
                #     context['list_Product'] = context['list_Product'].filter(Q(Name__icontains=s)).order_by('-id')
                #     context['s'] = s
                # if f:
                #     context['list_Product'] = context['list_Product'].filter(Belong_Large_area_id=f).order_by('-id')
                #     context['f'] = int(f)
                # if f1:
                #     context['list_Product'] = context['list_Product'].filter(Belong_Small_area_id=f1).order_by('-id')
                #     context['f1'] = int(f1)
                # print('context:',context)
                return render(request, 'sleekweb/admin/user_admin.html', context, status=200)
            else:
                return redirect('login_admin')
        return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})


def user_add_admin(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
            context = {}
            context['domain'] = settings.DOMAIN
            print('context:',context)
            if request.user.is_authenticated and request.user.is_superuser:
                return render(request, 'sleekweb/admin/user_add_admin.html', context, status=200)
            else:
                return redirect('login_admin')
        return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})

    elif request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            username =  request.POST.get('username')
            password =  request.POST.get('password')
            email = username
            if username is None or password is None or email is None:
                return JsonResponse({'success': False, 'message': 'Your login action is not accepted. Please go to the official WEBSITE page to register..'},json_dumps_params={'ensure_ascii': False})
            elif not username or not password  or not email:
                return JsonResponse({'success': False, 'message': 'Fill in all required information before registering.'},json_dumps_params={'ensure_ascii': False})
            else:
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'success': False, 'message': 'Username already exists'},json_dumps_params={'ensure_ascii': False})
                elif User.objects.filter(email=email).exists():
                    return JsonResponse({'success': False, 'message': 'Email already exists'},json_dumps_params={'ensure_ascii': False})
                else:
                    obj_user = User.objects.create_user(username=username,email=email,password=password,is_staff=True)
                    Time_user.objects.create(Belong_User=obj_user)
                return JsonResponse({'success': True,'message': 'Account registration successful. Log in now !', 'redirect_url': reverse('user_admin')},json_dumps_params={'ensure_ascii': False})
        return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})
    else:
        return redirect('user_add_admin')
    
def user_edit_admin(request,pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            context = {}
            context['domain'] = settings.DOMAIN
            try:
                context['obj_user'] = User.objects.get(pk=pk)
            except:
                context['obj_user'] = {}
            print('context:',context)
            if request.user.is_authenticated:
                return render(request, 'sleekweb/admin/user_edit_admin.html', context, status=200)
            else:
                return redirect('login_admin')
        return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})
    else:
        return redirect('user_edit_admin',pk=pk)
    
def user_remove_admin(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            context = {}
            context['domain'] = settings.DOMAIN
            id = request.POST.get('id')
            try:
                context['obj_user'] = User.objects.get(pk=id)
                context['obj_user'].delete()
                return JsonResponse({'success': True,'message': 'Account deleted successfully !', 'redirect_url': reverse('user_admin')},json_dumps_params={'ensure_ascii': False})
            except:
                context['obj_user'] = {}
                return JsonResponse({'success': True,'message': 'User does not exist !'},json_dumps_params={'ensure_ascii': False})
        return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})

def user_change_password_admin(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            context = {}
            context['domain'] = settings.DOMAIN
            id = request.POST.get('id')
            new_password = request.POST.get('new_password')
            print('new_password:',new_password)
            try:
                if request.user.is_superuser:
                    obj = User.objects.get(pk=id)
                    obj.set_password(new_password)
                    obj.save()
                    update_session_auth_hash(request, obj)
                else:
                    obj = request.user
                    obj.set_password(new_password)
                return JsonResponse({'success': True,'message': f'Password changed successfully for account {obj.username} !'},json_dumps_params={'ensure_ascii': False})
            except:
                obj = {}
                return JsonResponse({'success': True,'message': 'User does not exist !'},json_dumps_params={'ensure_ascii': False})
        return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})

def user_change_time_user_admin(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            context = {}
            context['domain'] = settings.DOMAIN
            user_id = request.POST.get('id')
            day_number = request.POST.get('day_number')

            try:
                day_number = int(day_number)
                user = User.objects.get(pk=user_id)
                
                # Lấy hoặc tạo Time_user nếu chưa có
                time_user, created = Time_user.objects.get_or_create(Belong_User=user)

                print('time_user.days_left:',time_user.days_left())

                if time_user.days_left() == 0:
                    day_number = day_number + 1

                print('day_number:',day_number)
                
                # Nếu End_time < now (quá hạn) thì bắt đầu từ hiện tại
                now = timezone.now()
                current_end = time_user.End_time if time_user.End_time > now else now
                
                # Cộng thêm ngày mới
                time_user.End_time = current_end + timedelta(days=day_number)
                time_user.save()

                context['success'] = True
                return JsonResponse({'success': True,'message': f'Add {day_number} days of success to {user.username}'},json_dumps_params={'ensure_ascii': False})
            except (User.DoesNotExist, ValueError):
                return JsonResponse({'error': 'Invalid data'}, status=400)
        return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def user_reset_time_user_admin(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            user_id = request.POST.get('id')
            try:
                user = User.objects.get(pk=user_id)
                time_user, created = Time_user.objects.get_or_create(Belong_User=user)

                # Reset thời gian hết hạn về thời điểm hiện tại
                now = timezone.now()
                time_user.End_time = now
                time_user.save()

                return JsonResponse({
                    'success': True,
                    'message': f'Time reset successful for user {user.username}',
                    'days_left': time_user.days_left()
                })

            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
        return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


