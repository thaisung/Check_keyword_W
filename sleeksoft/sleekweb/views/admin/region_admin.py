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

def region_admin(request):
    if request.method == 'GET':
        context = {}
        lc = request.COOKIES.get('language') or 'en'
        # Nation.objects.all().delete()
        context['domain'] = settings.DOMAIN
        context['list_Region'] = Region.objects.all()
        s = request.GET.get('s')
        if s:
            context['list_Region'] = context['list_Region'].filter(Q(Name__icontains=s)).order_by('-id')
            context['s'] = s
        print('context:',context)
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, 'sleekweb/admin/region_admin.html', context, status=200)
        else:
            return redirect('login_admin')
    elif request.method == 'POST':
        fields = {}
        fields['Name'] = request.POST.get('Name')
        obj = Region.objects.create(**fields)
        return redirect('region_admin')
    
def region_edit_admin(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        new_name = request.POST.get("Name")
        try:
            obj = Region.objects.get(pk=pk)
            obj.Name = new_name
            obj.save()
        except Region.DoesNotExist:
            pass
    return redirect("region_admin")  # hoặc HttpResponseRedirect nếu bạn muốn
    
def region_remove_admin(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        try:
            obj_pk = Region.objects.get(pk=pk)
            obj_pk.delete()
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('region_admin')
            })
        except Region.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Region does not exist.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })

    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })
    
def nation_add_admin(request):
    if request.method == 'POST':
        fields = {}
        pk = request.POST.get('pk')
        try:
            obj_pk = Region.objects.get(pk=pk)
        except:
            return redirect('region_admin')
        fields['Name'] = request.POST.get('Name')
        fields['Belong_Region'] = obj_pk
        obj = Nation.objects.create(**fields)
        return redirect('region_admin')
    
def nation_remove_admin(request):
    if request.method == 'POST':
        fields = {}
        pk = request.POST.get('pk')
        try:
            obj_pk = Nation.objects.get(pk=pk)
            obj_pk.delete()
        except:
            return redirect('region_admin')
        return redirect('region_admin')
        

