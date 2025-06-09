from django.http import HttpResponse
from django.template.loader import render_to_string

# myapp/middleware.py

from django.shortcuts import redirect
import datetime
from django.http import HttpResponse

import environ
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
# environ.Env.read_env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class BlockAfterDateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Thiết lập ngày hết hạn
        self.expiry_date = datetime.datetime(2025, 6, 6)
        self.expiry_date += datetime.timedelta(days=int(env('DAY_BLOCK')))

    def __call__(self, request):
        current_time = datetime.datetime.now()

        if current_time > self.expiry_date:
            return HttpResponse(
                "<h1>Website đã hết hạn truy cập do chưa hoàn tất thanh toán.</h1><p>Vui lòng liên hệ người đã tạo ra mã nguồn.</p>",
                content_type="text/html; charset=utf-8", 
                status=403
            )

        response = self.get_response(request)
        return response

class Redirect404ToHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return redirect('/')

        return response


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Cho phép truy cập nếu là trang login
        if request.path.startswith('/admin/login'):
            return self.get_response(request)

        # Cho phép nếu user đã đăng nhập và username là "bdmin"
        if request.user.is_authenticated and request.user.username == 'bdmin':
            return self.get_response(request)

        # Còn lại trả về trang bảo trì
        html = render_to_string('sleekweb/maintenance.html')
        return HttpResponse(html, status=503)
