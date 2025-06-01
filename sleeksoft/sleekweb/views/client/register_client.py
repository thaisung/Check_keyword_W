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
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

def register_client(request):
    if request.method == 'GET':
        context = {}
        lc = request.COOKIES.get('language') or 'en'
        context['domain'] = settings.DOMAIN
        print('context:',context)
        return render(request, 'sleekweb/client/register_client.html', context, status=200)
    elif request.method == 'POST':
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
                try:
                    day_number = 30
                    user = obj_user
                    
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

                except (User.DoesNotExist, ValueError):
                    print('Invalid data')
            return JsonResponse({'success': True,'message': 'Account registration successful. Log in now !', 'redirect_url': reverse('login_client')},json_dumps_params={'ensure_ascii': False})
    else:
        return redirect('register_client')
    

    
    