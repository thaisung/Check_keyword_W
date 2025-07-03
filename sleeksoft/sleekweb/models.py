from django.db import models

# Create your models here.
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Quản lý tài khoản Đăng Nhập"
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('username').blank = False
    AbstractUser._meta.get_field('username').blank = False
    AbstractUser._meta.get_field('password').blank = False
    AbstractUser._meta.get_field('password').blank = False
    
    Avatar = models.ImageField(upload_to='user_image', default="user_image/user_empty.png", null=True,blank=True)
    Full_name = models.CharField('Họ và tên', max_length=255,blank=True, null=True)
    Phone_number = models.CharField('Số điện thoại', max_length=255,blank=True, null=True)
    OTP = models.CharField('Mã Otp',max_length=255, null=True,blank=True)
    Money = models.IntegerField('Tiền',max_length=255, null=True,blank=True,default=0)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['Full_name']),        
        ]

class Time_user(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Thời hạn"
    
    Start_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    End_time = models.DateTimeField('Thời gian Kết thúc',auto_now_add=True)
    Belong_User = models.OneToOneField(User, on_delete=models.CASCADE, related_name='obj_Time_user',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

    def days_left(self):
        if self.End_time:
            remaining = (self.End_time - timezone.now()).days
            return max(remaining, 0)
        return 0
    
class Keyword(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Bảng giá"
    
    Count_keyword = models.IntegerField('Số từ 1 ngày dã sử dụng',blank=True, null=True,default=0)
    Now_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Belong_User = models.OneToOneField(User, on_delete=models.CASCADE, related_name='obj_Keyword',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

class Transaction_history(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Lịch sử giao dịch"
    
    Code = models.CharField('Mã giao dịch', max_length=10,blank=True, null=True)
    Content = models.CharField('Nội dung GD', max_length=100,blank=True, null=True)
    Belong_User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_transaction_history',blank=True, null=True)
    Status = models.IntegerField('Trạng thái', max_length=50,blank=True, null=True,default=2)
    Value = models.CharField('Giá trị', max_length=50,blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

class Price_list(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Bảng giá"
    
    Price_one = models.IntegerField('Giá 1 lần', max_length=100,blank=True, null=True,default=0)
    Price_month = models.IntegerField('Giá 30 ngày', max_length=100,blank=True, null=True,default=0)
    Keyword_day = models.IntegerField('Số từ khoá 1 ngày', max_length=100,blank=True, null=True,default=0)
    Order = models.IntegerField('Thứ tự', max_length=50,blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

class API_key(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "API key"
    Key = models.CharField('Key', max_length=200,blank=True, null=True)
    Order = models.IntegerField('Thứ tự', max_length=50,blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)


# class Photo(models.Model):
#     class Meta:
#         ordering = ["id"]
#         verbose_name_plural = "Ảnh sản phẩm"
    
#     Avatar = models.ImageField(upload_to='PRODUCT',null=True,blank=True)
#     Belong_XY = models.ForeignKey(XY, on_delete=models.CASCADE, related_name='list_photo',blank=True, null=True)
#     Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
#     Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True) 

# class Video(models.Model):
#     class Meta:
#         ordering = ["id"]
#         verbose_name_plural = "Video nhân viên"
    
#     Video = models.FileField(upload_to='VIDEOS', null=True, blank=True)
#     Belong_XY = models.ForeignKey(XY, on_delete=models.CASCADE, related_name='list_video', blank=True, null=True)
#     Creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)
#     Update_time = models.DateTimeField('Thời gian cập nhật', auto_now=True)


# class Website(models.Model):
#     class Meta:
#         ordering = ["id"]
#         verbose_name_plural = "Thông tin trang web"
    
#     Logo = models.ImageField(upload_to='website/logo',null=True,blank=True)
#     Icon = models.ImageField(upload_to='website/icon',null=True,blank=True)
#     Domain = models.CharField('Tên miền bao gồm http/https', max_length=255,blank=True, null=True)
#     Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
#     Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    

# class Banner(models.Model):
#     class Meta:
#         ordering = ["id"]
#         verbose_name_plural = "Ảnh Banner"
    
#     Photo = models.ImageField(upload_to='website/banner',null=True,blank=True)
#     Belong_Website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='list_photo_banner',blank=True, null=True)
#     Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
#     Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
    


