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



    
def list_user_client(request):
    if not request.user.is_authenticated:
        return redirect('login_client')
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Chưa được cấp quyền truy cập.'},json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET':
        context = {}
        lc = request.COOKIES.get('language') or 'en'
        context['domain'] = settings.DOMAIN
        context['list_User'] = User.objects.all().order_by('id')
        print('context:',context)
        return render(request, 'sleekweb/client/list_user_client.html', context, status=200)

def user_delete_client(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)

            # Chỉ cho phép đổi mật khẩu nếu người đang đăng nhập là chính họ
            if not request.user.is_superuser:
                messages.error(request, 'Chưa được cấp quyền.')
                return redirect('list_user_client')

            user.delete()

            messages.success(request, f'Xoá thành công tài khoản.')
            return redirect('list_user_client')
        except User.DoesNotExist:
            messages.error(request, 'Người dùng không tồn tại.')
            return redirect('list_user_client')

def user_change_password_client(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)

            # Chỉ cho phép đổi mật khẩu nếu người đang đăng nhập là chính họ
            if not request.user.is_superuser:
                messages.error(request, 'Chưa được cấp quyền.')
                return redirect('list_user_client')

            user.password = make_password(new_password)
            user.save()

            messages.success(request, f'Đổi mật khẩu thành công tài khoản ({username}).')
            return redirect('list_user_client')
        except User.DoesNotExist:
            messages.error(request, 'Người dùng không tồn tại.')
            return redirect('list_user_client')
    
def user_deposit_money_client(request):
    if not request.user.is_authenticated:
        return redirect('login_client')
    if not request.user.is_superuser:
        messages.error(request, 'Chưa được cấp quyền truy cập.')
        return redirect('list_user_client')
    if request.method == 'POST':
        username = request.POST.get('username')
        money = request.POST.get('money')
        try:
            user = User.objects.get(username=username)
            if user.Money:
                user.Money = int(user.Money) + int(money)
            else:
                user.Money = int(money)
            user.save()
            if int(money) >= 0:
                Transaction_history.objects.create(
                    Code = random.randint(100_000_000, 999_999_999),
                    Content = f'Nạp tiền cho ({user.username})',
                    Belong_User = request.user,
                    Status = True,
                    Value = f'+ {money}'
                    )
                messages.success(request, f'Nạp tiền thành công ({money} đ) cho tài khoản ({username}).')
            else:
                Transaction_history.objects.create(
                    Code = random.randint(100_000_000, 999_999_999),
                    Content = f'Trừ tiền cho ({user.username})',
                    Belong_User = request.user,
                    Status = True,
                    Value = f'{money}'
                    )
                messages.success(request, f'Trừ tiền thành công ({money} đ) cho tài khoản ({username}).')
            return redirect('list_user_client')
        except User.DoesNotExist:
            messages.error(request, 'Người dùng không tồn tại.')
            return redirect('list_user_client')
        

