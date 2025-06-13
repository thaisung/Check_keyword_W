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

from django.core.mail import send_mail
from django.forms.models import model_to_dict
from django.core.mail import send_mail,EmailMessage

from django.urls import resolve



    
def price_list_client(request):
    if request.method == 'GET':
        context = {}
        lc = request.COOKIES.get('language') or 'en'
        context['domain'] = settings.DOMAIN
        print('context:',context)
        try:
            obj = Price_list.objects.get(Order=1)
            context['Price_one'] = obj.Price_one
            context['Price_month'] = obj.Price_month
            context['Keyword_day'] = obj.Keyword_day
        except:
            pass
        return render(request, 'sleekweb/client/price_list_client.html', context, status=200)
    if request.method == 'POST':
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, 'Chưa được cấp quyền.')
            return redirect('login_client')
        Price_one = request.POST.get('Price_one')
        Price_month = request.POST.get('Price_month')
        Keyword_day = request.POST.get('Keyword_day')
        try:
            obj = Price_list.objects.get(Order=1)
            if Price_one:
                obj.Price_one = Price_one
            if Price_month:
                obj.Price_month = Price_month
            if Keyword_day:
                obj.Keyword_day = Keyword_day
            obj.save()
        except:
            if Price_one:
                obj = Price_list.objects.create(Price_one=Price_one,Order=1)
            if Price_month:
                obj = Price_list.objects.create(Price_month=Price_month,Order=1)
            if Keyword_day:
                obj = Price_list.objects.create(Keyword_day=Keyword_day,Order=1)
        if Keyword_day:
            return redirect('home_client')
        else:
            return redirect('price_list_client')
        
def user_change_time_user_30(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            context = {}
            context['domain'] = settings.DOMAIN
            try:
                obj = Price_list.objects.get(Order=1)
                context['Price_one'] = obj.Price_one
                context['Price_month'] = obj.Price_month
                context['Keyword_day'] = obj.Keyword_day
            except:
                pass
            if  int(request.user.Money) < int(obj.Price_month):
                messages.error(request, 'Không thể đăng ký do số tiền không đủ')
                return redirect('price_list_client')
                # return JsonResponse({'success': False, 'message': 'Không thể đăng ký do số tiền không đủ'},json_dumps_params={'ensure_ascii': False})
            try:
                day_number = 30
                user = request.user
                
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

                request.user.Money = int(request.user.Money)-int(obj.Price_month)
                request.user.save()

                Transaction_history.objects.create(
                    Code = random.randint(100_000_000, 999_999_999),
                    Content = 'Đăng ký 30 ngày',
                    Belong_User = request.user,
                    Status = 1,
                    Value = f'-{obj.Price_month}'
                    )

                context['success'] = True
                messages.success(request, f'Đã thêm 30 ngày thành công cho tài khoản {user.username}')
                return redirect('price_list_client')
                # return JsonResponse({'success': True,'message': f'Đã thêm {day_number} ngày thành công cho tài khoản {user.username}'},json_dumps_params={'ensure_ascii': False})
            except (User.DoesNotExist, ValueError):
                return JsonResponse({'error': 'Lỗi data'}, status=400)
        return JsonResponse({'success': False, 'message': 'Đăng nhập tài khoản trước khi đăng ký'},json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'error': 'Lỗi kết nối'}, status=400)
