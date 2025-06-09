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

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random


def set_language(request, lang_code):
    response = redirect(request.META.get('HTTP_REFERER', '/'))  # quay lại trang vừa bấm
    response.set_cookie('language', lang_code, max_age=60*60*24*30)  # 30 ngày
    return response

def check_count_keyword(request,count_keyword):
    try:
        obj = Price_list.objects.get(Order=1)
        Keyword_day = obj.Keyword_day
        Keyword_month = Keyword_day*30
    except:
        pass
    # Lấy thời gian hiện tại
    now = timezone.now()
    today = now.date()

    try:
        obj_Keyword = request.user.obj_Keyword
    except:
        obj_Keyword = Keyword.objects.create(Belong_User=request.user)

    # So sánh ngày/tháng/năm
    if obj_Keyword.Now_time.date() == today:
        if obj_Keyword.Count_keyword >= Keyword_day:
            messages.error(request, 'Hết giới hạn tìm kiếm trong ngày.')
            return redirect('home_client')
        else:
            obj_Keyword.Count_keyword += count_keyword
    else:
        # Nếu khác ngày, reset Count và cập nhật ngày mới
        obj_Keyword.Now_time = now
        obj_Keyword.Count_keyword = count_keyword

    obj_Keyword.save()

    # Tiếp tục xử lý
    return True

def check_rank_keyword(non_empty_lines,domain,proxy,device):
    data_check_rank_keyword = []
    for i in non_empty_lines:
        result = check_keyword_rank(i, domain, proxy=proxy,device=device)
        obj = {
            "keyword" : i,
            "rank" : result['rank']
        }
        data_check_rank_keyword.append(obj)
    return data_check_rank_keyword

def check_keyword_rank(keyword, domain, proxy=None, device='desktop'):
    ua = UserAgent()

    results = []

    for page in range(10):  # 10 pages => 100 results
        user_agent = ua.chrome if device == 'Desktop' else ua.android
        headers = {
            "User-Agent": user_agent,
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/",
        }

        start = page * 10
        url = f"https://www.google.com.vn/search?q={requests.utils.quote(keyword)}&start={start}&hl=vi"

        try:
            response = requests.get(
                url,
                headers=headers,
                proxies={"http": proxy, "https": proxy} if proxy else None,
                timeout=10
            )
            if response.status_code != 200:
                print(f"❌ Lỗi HTTP {response.status_code} ở trang {page + 1}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            blocks = soup.select('div.g')

            if not blocks:
                print("🔍 Không tìm thấy kết quả.")
                break

            for idx, block in enumerate(blocks):
                a_tag = block.select_one('a[href]')
                if not a_tag:
                    continue
                link = a_tag['href']
                rank = start + idx + 1
                results.append({'rank': rank, 'url': link})
                if domain in link:
                    return {
                        'keyword': keyword,
                        'domain': domain,
                        'rank': rank,
                        'url': link
                    }

            # Random delay
            time.sleep(random.uniform(2, 4))

        except Exception as e:
            print("⚠️ Lỗi:", e)
            break

    return {
        'keyword': keyword,
        'domain': domain,
        'rank': None,
        'url': None,
        'message': 'Không tìm thấy trong top 100'
    }

def get_proxy():
    pass
    return 0
def home_client(request):
    if request.method == 'GET':
        context = {}
        lc = request.COOKIES.get('language') or 'en'
        context['lc'] = lc
        context['domain'] = settings.DOMAIN
        context['message'] = f"Hello, I saw profile on https://{settings.DOMAIN}"
        # context['list_Product'] = Product.objects.all()
        # print('context:',context)
        # p = request.GET.get('p','1')
        # context['p'] = p
        # # Sử dụng Paginator để chia nhỏ danh sách (10 là số lượng mục trên mỗi trang)
        # paginator = Paginator(context['list_Product'], settings.PAGE)
        # # Lấy số trang hiện tại từ URL, nếu không mặc định là trang 1
        # context['list_Product'] = paginator.get_page(p)
        try:
            obj = Price_list.objects.get(Order=1)
            context['Price_one'] = obj.Price_one
            context['Price_month'] = obj.Price_month
            context['Keyword_day'] = obj.Keyword_day
            context['Keyword_month'] = context['Keyword_day']*30
        except:
            pass
        context['data_check_rank_keyword'] = request.session.pop('data_check_rank_keyword', None)
        context['Device'] = request.session.pop('Device', None)
        context['Domain'] = request.session.pop('Domain', None)
        return render(request, 'sleekweb/client/home_client.html', context, status=200)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Đăng nhập tài khoản trước khi tìm kiếm.')
            return redirect('login_client')
        
        Device = request.POST.get('Device')
        Domain = request.POST.get('Domain')
        Content_keyword = request.POST.get('Content_keyword')
        # Tách các dòng, xoá khoảng trắng đầu/cuối, và loại bỏ dòng rỗng
        lines = Content_keyword.strip().splitlines()
        non_empty_lines = [line for line in lines if line.strip() != '']
        # Đếm số dòng có nội dung
        count_keyword = len(non_empty_lines)

        Condition_check_count_keyword = check_count_keyword(request,count_keyword)
        try:
            Condition_time_user = request.user.obj_Time_user.days_left()
        except:
            obj_Time_user = Time_user.objects.create(Belong_User=request.user)
            Condition_time_user = obj_Time_user.days_left()

        print('Condition_time_user:',Condition_time_user)
        proxy = get_proxy()
        if Condition_check_count_keyword:
            if int(Condition_time_user) > 0:
                data_check_rank_keyword = (non_empty_lines,Domain,proxy,Device)
            else:
                try:
                    obj_Price_list = Price_list.objects.get(Order=1)
                except:
                    obj_Price_list={}
                data_check_rank_keyword = (non_empty_lines,Domain,proxy,Device)
                Transaction_history.objects.create(
                    Code='SerGoogle',
                    Content='Tiềm kiếm thứ hạng',
                    Belong_User=request.user,
                    Status=1,
                    Value = f"-{obj_Price_list.Price_one}"
                    )
        request.session['data_check_rank_keyword'] = data_check_rank_keyword
        request.session['Device'] = Device
        request.session['Domain'] = Domain
        return redirect('home_client')
