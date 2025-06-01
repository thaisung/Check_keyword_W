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
    Belong_User = models.OneToOneField(User, on_delete=models.CASCADE, related_name='obj_user',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

    def days_left(self):
        if self.End_time:
            remaining = (self.End_time - timezone.now()).days
            return max(remaining, 0)
        return 0

class Region(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Khu lớn"
    
    Name = models.CharField('Tên Châu lục', max_length=100,blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

class Nation(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Khu nhỏ"
    
    Name = models.CharField('Tên quốc gia', max_length=100,blank=True, null=True)
    Belong_Region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='list_nation',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

class XY(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Người tham gia"
    
    uuid = models.CharField('uuid', max_length=100,blank=True, null=True)
    Avatar = models.ImageField(upload_to='AVATAR_PRODUCT',null=True,blank=True)
    Name = models.CharField('Tên NV', max_length=100,blank=True, null=True)
    Phone = models.CharField('Số đt', max_length=100,blank=True, null=True)
    Overnight = models.CharField('Qua đêm', max_length=10,blank=True, null=True,default='0')
    Year_of_birth = models.CharField('Năm sinh', max_length=50,blank=True, null=True)
    Height = models.CharField('Chiều cao', max_length=50,blank=True, null=True)
    Weight = models.CharField('Cân nặng', max_length=50,blank=True, null=True)
    Rounds = models.CharField('Số đo 3 vòng', max_length=100,blank=True, null=True)
    Service = models.TextField('Dịch vụ',blank=True, null=True)
    Segment = models.CharField('Phân khúc', max_length=50,blank=True, null=True)
    Content = models.TextField('Mô tả',blank=True, null=True)
    Price_call_in = models.TextField('Giá gọi đến',blank=True, null=True)
    Price_call_out = models.TextField('Giá gọi ra',blank=True, null=True)
    Order = models.IntegerField('Số thứ tự',blank=True, null=True)
    Belong_User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_xy',blank=True, null=True)
    Belong_Region = models.ForeignKey(Region, on_delete=models.SET_NULL, related_name='list_XY_region',blank=True, null=True)
    Belong_Nation = models.ForeignKey(Nation, on_delete=models.SET_NULL, related_name='list_XY_nation',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

class Photo(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Ảnh sản phẩm"
    
    Avatar = models.ImageField(upload_to='PRODUCT',null=True,blank=True)
    Belong_XY = models.ForeignKey(XY, on_delete=models.CASCADE, related_name='list_photo',blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True) 

class Video(models.Model):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Video nhân viên"
    
    Video = models.FileField(upload_to='VIDEOS', null=True, blank=True)
    Belong_XY = models.ForeignKey(XY, on_delete=models.CASCADE, related_name='list_video', blank=True, null=True)
    Creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)
    Update_time = models.DateTimeField('Thời gian cập nhật', auto_now=True)


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
    


