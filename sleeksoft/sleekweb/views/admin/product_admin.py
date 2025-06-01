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

import re


    
def product_admin(request):
    if not request.user.is_superuser and request.user.obj_user.days_left() <= 0:
        return render(request, 'sleekweb/admin/product_admin_not.html', status=200)
    if request.method == 'GET':
        context = {}
        lc = request.COOKIES.get('language') or 'en'
        context['domain'] = settings.DOMAIN
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context['list_Product'] = XY.objects.all().order_by('Order')
            else:
                context['list_Product'] = XY.objects.filter(Belong_User=request.user)
        else:
            return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})
        context['list_Region'] = Region.objects.all()
        context['list_Nation'] = Nation.objects.all()
        s = request.GET.get('s')
        f = request.GET.get('f')
        f1 = request.GET.get('f1')
        if s:
            context['list_Product'] = context['list_Product'].filter(Q(Name__icontains=s)).order_by('-id')
            context['s'] = s
        if f:
            context['list_Product'] = context['list_Product'].filter(Belong_Region_id=f).order_by('-id')
            context['f'] = int(f)
        if f1:
            context['list_Product'] = context['list_Product'].filter(Belong_Nation_id=f1).order_by('-id')
            context['f1'] = int(f1)
        print('context:',context)
        if request.user.is_authenticated:
            return render(request, 'sleekweb/admin/product_admin.html', context, status=200)
        else:
            return redirect('login_admin')

def get_nations(request):
    region_id = request.GET.get('region_id')
    data = []
    print('region_id:',region_id)
    if region_id:
        nations = Nation.objects.filter(Belong_Region_id=region_id)
        data = [{'id': sa.id, 'name': sa.Name} for sa in nations]
    return JsonResponse({'nations': data})    

def alphanumeric_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


def product_add_admin(request):
    if not request.user.is_superuser and request.user.obj_user.days_left() <= 0:
        return render(request, 'sleekweb/admin/product_admin_not.html', status=200)
    if request.method == 'GET':
        context = {}
        context['domain'] = settings.DOMAIN
        context['list_Region'] = Region.objects.all()
        context['list_Nation'] = Nation.objects.all()
        print('context:',context)
        if request.user.is_authenticated:
            return render(request, 'sleekweb/admin/product_add_admin.html', context, status=200)
        else:
            return redirect('login_admin')
        
    elif request.method == 'POST':
        if request.user.is_authenticated:
            random_uuid = uuid.uuid4()

            region_id = request.POST.get('Belong_Region')
            nation_id = request.POST.get('Belong_Nation')

            fields = {}
            fields['Avatar'] = request.FILES.get('Avatar')
            fields['Name'] = request.POST.get('Name')
            fields['Phone'] = request.POST.get('Phone')
            fields['Segment'] = request.POST.get('Segment')
            fields['Overnight'] = request.POST.get('Overnight')
            fields['Year_of_birth'] = request.POST.get('Year_of_birth')
            fields['Height'] = request.POST.get('Height')
            fields['Weight'] = request.POST.get('Weight')
            fields['Rounds'] = request.POST.get('Rounds')
            fields['Service'] = request.POST.get('Service')
            fields['Content'] = request.POST.get('Content')
            fields['Price_call_in'] = request.POST.get('Price_call_in')
            fields['Price_call_out'] = request.POST.get('Price_call_out')
            fields['Belong_User'] = request.user
            fields['Belong_Region'] = Region.objects.get(id=region_id) if region_id else None
            fields['Belong_Nation'] = Nation.objects.get(id=nation_id) if nation_id else None
            print('fields:',fields)
            fields['uuid'] = random_uuid
            obj = XY.objects.create(**fields)
            
            List_Photo = request.FILES.getlist('List_Photo')
            List_Photo = sorted(List_Photo, key=lambda f: alphanumeric_key(f.name))
            if obj  and List_Photo:
                for i in List_Photo:
                    Photo.objects.create(Avatar=i,Belong_XY=obj)

            List_Video = request.FILES.getlist('List_Video')
            List_Video = sorted(List_Video, key=lambda f: alphanumeric_key(f.name))
            if obj  and List_Video:
                for i in List_Video:
                    Video.objects.create(Video=i,Belong_XY=obj)
            
            return redirect('product_admin')
        return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})


def product_edit_admin(request,pk):
    if not request.user.is_superuser and request.user.obj_user.days_left() <= 0:
        return render(request, 'sleekweb/admin/product_admin_not.html', status=200)
    if request.method == 'GET':
        context = {}
        context['domain'] = settings.DOMAIN
        try:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    context['obj_Product'] = XY.objects.get(uuid=pk)
                else:
                    context['obj_Product'] = XY.objects.get(uuid=pk,Belong_User=request.user)
            else:
                return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})
        except:
            return redirect('product_admin')
        context['list_Region'] = Region.objects.all()
        context['list_Nation'] = Nation.objects.all()
        print('context:',context)
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, 'sleekweb/admin/product_edit_admin.html', context, status=200)
        elif request.user.is_authenticated and request.user.obj_user.days_left() > 0:
            return render(request, 'sleekweb/admin/product_edit_admin.html', context, status=200)
        else:
            return redirect('login_admin')
    elif request.method == 'POST':
        try:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    obj = XY.objects.get(uuid=pk)
                else:
                    obj = XY.objects.get(uuid=pk,Belong_User=request.user)
            else:
                return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})
        except:
            return redirect('product_admin')

        region_id = request.POST.get('Belong_Region')
        nation_id = request.POST.get('Belong_Nation')

        fields = {}
        print('aaaaaa:',request.POST.get('Avatar'))
        if request.FILES.get('Avatar'):
            fields['Avatar'] = request.FILES.get('Avatar')
        fields['Name'] = request.POST.get('Name')
        fields['Phone'] = request.POST.get('Phone')
        fields['Segment'] = request.POST.get('Segment')
        fields['Overnight'] = request.POST.get('Overnight')
        fields['Year_of_birth'] = request.POST.get('Year_of_birth')
        fields['Height'] = request.POST.get('Height')
        fields['Weight'] = request.POST.get('Weight')
        fields['Rounds'] = request.POST.get('Rounds')
        fields['Service'] = request.POST.get('Service')
        fields['Content'] = request.POST.get('Content')
        fields['Price_call_in'] = request.POST.get('Price_call_in')
        fields['Price_call_out'] = request.POST.get('Price_call_out')
        fields['Belong_Region'] = Region.objects.get(id=region_id) if region_id else None
        fields['Belong_Nation'] = Nation.objects.get(id=nation_id) if nation_id else None
        for key, value in fields.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        obj.save()

        List_Photo = request.FILES.getlist('List_Photo')
        List_Photo = sorted(List_Photo, key=lambda f: alphanumeric_key(f.name))

        if obj  and List_Photo:
            obj.list_photo.all().delete()
            for i in List_Photo:
                Photo.objects.create(Avatar=i,Belong_XY=obj)

        List_Video = request.FILES.getlist('List_Video')
        List_Video = sorted(List_Video, key=lambda f: alphanumeric_key(f.name))
        if obj  and List_Video:
            obj.list_video.all().delete()
            for i in List_Video:
                Video.objects.create(Video=i,Belong_XY=obj)
    
        return redirect('product_edit_admin',pk=pk)
    
def product_remove_admin(request):
    if not request.user.is_superuser and request.user.obj_user.days_left() <= 0:
        return render(request, 'sleekweb/admin/product_admin_not.html', status=200)
    if request.method == 'POST':
        uuid = request.POST.get('uuid')
        try:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    obj = XY.objects.get(uuid=uuid)
                    obj.delete()
                else:
                    obj = XY.objects.get(uuid=uuid,Belong_User=request.user)
                    obj.delete()
            else:
                return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})
        except:
            return redirect('product_admin')
        return redirect('product_admin')
    
def product_order_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            context = {}
            id = request.POST.get('id')
            Order = request.POST.get('Order')
            try:
                obj = XY.objects.get(pk=id)
                obj.Order = Order
                obj.save()
            except:
                return redirect('product_admin')
            return redirect('product_admin')
    else:
            return JsonResponse({'success': False, 'message': 'Log in to your account and make sure it has access'},json_dumps_params={'ensure_ascii': False})    
    

