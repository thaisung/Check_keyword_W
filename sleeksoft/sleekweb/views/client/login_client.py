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



    
def login_client(request):
    if request.method == 'GET':
        context = {}
        lc = request.COOKIES.get('language') or 'en'
        context['domain'] = settings.DOMAIN
        print('context:',context)
        if request.user.is_authenticated:
            return redirect('product_admin')
        else:
            return render(request, 'sleekweb/client/login_client.html', context, status=200)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is None or password is None:
            return JsonResponse({'success': False, 'message': 'Hành động đăng nhập của bạn không được chấp nhận. Vui lòng vào trang WEBSITE chính thức để đăng nhập.'},json_dumps_params={'ensure_ascii': False})
        elif not username or not password:
            return JsonResponse({'success': False, 'message': 'Điền đầy đủ thông tin trước khi đăng nhập.'},json_dumps_params={'ensure_ascii': False})
        else:
            if User.objects.filter(username=username).exists():
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return JsonResponse({'success': True, 'redirect_url': reverse('home_client')},json_dumps_params={'ensure_ascii': False})
                    else:
                        return JsonResponse({'success': False, 'message': 'Tài khoản của bạn đã bị vô hiệu hóa.'},json_dumps_params={'ensure_ascii': False})
                else:
                    return JsonResponse({'success': False, 'message': 'Mật khẩu đăng nhập sai.'},json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'success': False, 'message': 'Tên tài khoản đăng nhập không đúng.'},json_dumps_params={'ensure_ascii': False})
    
def logout_client(request):
    logout(request)
    return redirect('login_client')

def change_password_client(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)

            # Chỉ cho phép đổi mật khẩu nếu người đang đăng nhập là chính họ
            if request.user != user:
                messages.error(request, 'Không được phép đổi mật khẩu người khác.')
                return redirect('profile_client')
                # return JsonResponse({'success': False, 'message': 'Không được phép đổi mật khẩu người khác.'},json_dumps_params={'ensure_ascii': False})

            user.password = make_password(new_password)
            user.save()

            # Đăng nhập lại để duy trì session
            login(request, user)
            messages.success(request, 'Đổi mật khẩu thành công.')
            return redirect('profile_client')
            # return JsonResponse({'success': True, 'message': 'Đổi mật khẩu thành công.', 'redirect_url': reverse('profile_client')},json_dumps_params={'ensure_ascii': False})
        except User.DoesNotExist:
            messages.error(request, 'Người dùng không tồn tại.')
            return redirect('profile_client')
            # return JsonResponse({'success': False, 'message': 'Người dùng không tồn tại.'},json_dumps_params={'ensure_ascii': False})

        
    