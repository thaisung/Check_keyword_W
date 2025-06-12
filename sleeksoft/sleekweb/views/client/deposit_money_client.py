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

from pathlib import Path
import os
import environ
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
# environ.Env.read_env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


@csrf_exempt  # Tắt CSRF vì request đến từ bên ngoài (my.sepay.vn)
def payment_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('data:',data)
            print('data.content:',data['content'])
            print('code:',data['content'].split()[0])
            print('data.transferAmount:',data['transferAmount'])
            try:
                obj_Transaction_history = Transaction_history.objects.get(Code=data['content'].split()[0])
                
                user = obj_Transaction_history.Belong_User
                if user.Money:
                    user.Money = int(user.Money) + int(data['transferAmount'])
                else:
                    user.Money = int(data['transferAmount'])
                user.save()

                obj_Transaction_history.Status = 1
                obj_Transaction_history.save()   
            except:
                return JsonResponse({'success': False}, status=400)
            # Trả về thành công
            return JsonResponse({'success': True}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def deposit_money_client(request):
    if request.method == 'GET':
        context = {}
        lc = request.COOKIES.get('language') or 'en'
        context['domain'] = settings.DOMAIN
        print('context:',context)
        return render(request, 'sleekweb/client/deposit_money_client.html', context, status=200)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Đăng nhập tài khoản trước khi nạp tiền.')
            return redirect('login_client')
        username = request.user
        money = request.POST.get('money')
        print('money:',money)
        code = request.POST.get('Code')
        if int(money) < int(env('MONEY')):
            messages.error(request, f"Nạp tối thiểu ({int(env('MONEY'))}đ).")
            return redirect('deposit_money_client')
        try:            
            obj_Transaction_history = Transaction_history.objects.create(
                Code = code,
                Content = 'Nạp tiền',
                Belong_User = request.user,
                Value = f'+ {money}'
                )
            for i in range(0,60):
                dk = Transaction_history.objects.get(Code=obj_Transaction_history.Code)
                if dk.Status == 1:
                    messages.success(request, f'Nạp tiền thành công ({money} đ) cho tài khoản ({username}).')
                    break
                time.sleep(3)
            if Transaction_history.objects.get(Code=obj_Transaction_history.Code).Status == 2:
                obj_Transaction_history.Status = 0
                obj_Transaction_history.save()
                messages.error(request, f'Nạp tiền không thành công cho tài khoản ({username}).')
            return redirect('deposit_money_client')
        except User.DoesNotExist:
            messages.error(request, 'Người dùng không tồn tại.')
            return redirect('deposit_money_client')

