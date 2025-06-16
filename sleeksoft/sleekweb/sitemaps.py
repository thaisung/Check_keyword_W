# blog/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import *

from datetime import datetime

from .views.client.login_client import *
from .views.client.reset_password_client  import *
from .views.client.register_client import *
from .views.client.home_client import *

protocol = 'https'

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'
    protocol = protocol

    def items(self):
        return [
            'home_client',
            'login_client',
            'register_client',
            'deposit_money_client',
            'price_list_client'
        ]

    def location(self, item):
        return reverse(item)
    
