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
            'filter_client',
            'login_client',
            'register_client',
            'contact_client',
        ]

    def location(self, item):
        return reverse(item)
    
class detail_product_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = protocol

    def items(self):
        # Lấy tất cả các Category_product từ cơ sở dữ liệu
        return XY.objects.all()

    def lastmod(self, obj):
        return obj.Update_time

    def location(self, item):
        # Dùng slug của mỗi category_product để tạo đường dẫn
        return reverse('detail_client', kwargs={'pk': item.uuid})

# class detail_sound_Sitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.9
#     protocol = 'https'

#     def items(self):
#         return Sound_List.objects.all()

#     def lastmod(self, obj):
#         return obj.created_at_sound
    
#     def location(self, obj):
#         return reverse('detail_sound', args=[obj.sound_url])
    
# class detail_video_Sitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.9
#     protocol = 'https'

#     def items(self):
#         return Video_List.objects.all()

#     def lastmod(self, obj):
#         return obj.created_at_video
    
#     def location(self, obj):
#         return reverse('detail_video', args=[obj.video_url])
    
# class image_video_Sitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.9
#     protocol = 'https'

#     def items(self):
#         return Video_List.objects.all()

#     def lastmod(self, obj):
#         return obj.created_at_video
    
#     def location(self, obj):
#         image_path = obj.video_Image.url
#         return image_path
    
# class StaticSitemap1(Sitemap):
#     changefreq = "monthly"
#     priority = 0.5
#     protocol = 'https'
 
#     def items(self):
#         return ['about','copyright','contact'] 
    
#     def lastmod(self, obj):

#         return None
 
#     def location(self, item):
#         return reverse(item)
    

