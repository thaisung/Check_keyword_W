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



    
def reset_password_client(request):
    if request.method == 'GET':
        context = {}
        lc = request.COOKIES.get('language') or 'en'
        context['domain'] = settings.DOMAIN
        print('context:',context)
        return render(request, 'sleekweb/client/reset_password_client.html', context, status=200)
    elif request.method == 'POST':
        username = request.POST.get('username')
        if username is None:
            return JsonResponse({'success': False, 'message': 'Your login action is not accepted. Please go to the official WEBSITE page to login.'})
        elif not username:
            return JsonResponse({'success': False, 'message': 'Fill in all information before logging in.'})
        else:
            if User.objects.filter(email=username).exists():
                try:
                    user = User.objects.get(email = username)
                    otp = random.randint(10000000, 99999999)
                    user.OTP = otp
                    user.save()
                    if user:
                        email = username
                        subject = f'Notification from customer service system - {settings.DOMAIN}'
                        message = f"""
                        <html>
                        <body>
                            <p><strong>The OTP code to retrieve your password is:</strong></p>
                            <p>OTP code : {otp}</p>
                        </body>
                        </html>
                        """

                        email = EmailMessage(subject, message, to=[email])
                        email.content_subtype = "html"  # Đặt định dạng nội dung email là HTML
                        email.send()
                    return JsonResponse({'success': True,'message': 'OTP code successfully sent to your Email', 'redirect_url': reverse('change_password_check_otp_client')})
                except:
                    user = None
                    return JsonResponse({'success': False, 'message': 'Account does not exist'})
            else:
                return JsonResponse({'success': False, 'message': 'Incorrect login account name'})
            
def change_password_check_otp_client(request):
    if request.method == 'GET':
        context = {}
        print('context:',context)
        return render(request, 'sleekweb/client/change_password_check_otp_client.html', context, status=200)
    elif request.method == 'POST':
        context = {}
        print('context:',context)
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        try:
            user = User.objects.get(OTP = otp)
            if user:
                user.OTP = ''
                user.password = make_password(new_password)
                user.save()
                return JsonResponse({'success': True,'message': 'Account password changed successfully','redirect_url': reverse('login_client')})
            else:
                return JsonResponse({'success': False, 'message': 'Incorrect OTP code'})
        except:
            user = None
            return JsonResponse({'success': False, 'message': 'Incorrect OTP code'})
    else:
        return JsonResponse({'success': False, 'message': 'No method exists.'})