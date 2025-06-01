"""
URL configuration for luanvan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.contrib import admin
# from Data_Interaction.admin import admin_site
from django.urls import path

from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from django.urls import re_path,path


from django.views.generic.base import TemplateView
from django.conf.urls.static import serve

from django.views.generic import RedirectView

from django.contrib.auth import views as auth_views

from .views.client.login_client import *
from .views.client.reset_password_client  import *
from .views.client.register_client import *
from .views.client.home_client import *
from .views.client.detail_client import *
from .views.client.filter_client import *
from .views.client.contact_client import *

from .views.client.deposit_money_client import *
from .views.client.transaction_history_client import *
from .views.client.price_list_client import *
from .views.client.profile_client import *
from .views.client.list_user_client import *

from .views.admin.login_admin import *
from .views.admin.product_admin import *
from .views.admin.region_admin import *
from .views.admin.user_admin import *
from .views.admin.setting_admin import *

from sleekweb.sitemaps import *
from django.contrib.sitemaps.views import sitemap

sitemaps_dict = {
    'static': StaticViewSitemap,
    'product': detail_product_Sitemap,
}

urlpatterns = [
    path('deposit-money', deposit_money_client,name='deposit_money_client'),
    path('transaction-history', transaction_history_client,name='transaction_history_client'),
    path('price-list', price_list_client,name='price_list_client'),
    path('profile-client',profile_client,name='profile_client'),
    path('list-user',list_user_client,name='list_user_client'),
    # path('account/login', login_client,name='login_client'),
    # path('admin/account/login', login_admin,name='login_admin'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps_dict}, name='sitemap'),

    path('set-language/<str:lang_code>/', set_language, name='set_language'),
    path('', home_client,name='home_client'),
    path('detail/<str:pk>/', detail_client,name='detail_client'),
    path('filter/', filter_client,name='filter_client'),
    path('account/login', login_client,name='login_client'),

    path('account/reset-password', reset_password_client,name='reset_password_client'),
    path('account/change-password-otp', change_password_check_otp_client,name='change_password_check_otp_client'),

    path('account/register', register_client,name='register_client'),
    path('contact', contact_client,name='contact_client'),
    

    path('admin/login', login_admin,name='login_admin'),
    path('admin/logout', logout_admin,name='logout_admin'),
    path('admin/product', product_admin,name='product_admin'),
    path('admin/product/add', product_add_admin,name='product_add_admin'),
    path('ajax/get-nations/', get_nations, name='get_nations'),
    path('admin/product/edit/<str:pk>/', product_edit_admin,name='product_edit_admin'),
    path('admin/product/remove', product_remove_admin,name='product_remove_admin'),
    path('admin/product/order', product_order_admin,name='product_order_admin'),
    path('admin/region', region_admin,name='region_admin'),
    path('admin/region/edit',region_edit_admin,name='region_edit_admin'),
    path('admin/region-remove', region_remove_admin,name='region_remove_admin'),
    path('admin/nation-add', nation_add_admin,name='nation_add_admin'),
    path('admin/nation-remove', nation_remove_admin,name='nation_remove_admin'),

    path('admin/user', user_admin,name='user_admin'),
    path('admin/user/add', user_add_admin,name='user_add_admin'),
    path('admin/user/edit/<int:pk>/', user_edit_admin,name='user_edit_admin'),
    path('admin/user/remove/', user_remove_admin,name='user_remove_admin'),
    path('admin/user/change-password/', user_change_password_admin,name='user_change_password_admin'),
    path('admin/user/change-time/', user_change_time_user_admin,name='user_change_time_user_admin'),
    path('admin/user/reset-time/', user_reset_time_user_admin,name='user_reset_time_user_admin'),

    path('admin/setting/', setting_admin,name='setting_admin'),
] 