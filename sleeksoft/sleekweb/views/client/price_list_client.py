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