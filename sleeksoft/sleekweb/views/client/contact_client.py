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



    
def contact_client(request):
    if request.method == 'GET':
        context = {}
        lc = request.COOKIES.get('language') or 'en'
        context['domain'] = settings.DOMAIN
        context['list_Region'] = Region.objects.all()
        context['list_Nation'] = Nation.objects.all()
        context['list_Product'] = XY.objects.all().order_by('Order')
        context['list_random_products'] = random.sample(list(context['list_Product']), min(2, len(context['list_Product'])))
        context['list_random_products1'] = random.sample(list(context['list_Product']), min(2, len(context['list_Product'])))

        # context['obj_Product_en'] = XY_en.objects.get(uuid=pk)
        # context['obj_Product_cn'] = XY_cn.objects.get(uuid=pk)
        # context['list_Large_area'] = Large_area.objects.all()
        # context['list_Small_area'] = Small_area.objects.filter(Belong_Large_area=context['obj_Product_en'].Belong_Large_area)

        # context['list_Product'] = Product.objects.all()
        print('context:',context)
        return render(request, 'sleekweb/client/contact_client.html', context, status=200)
    