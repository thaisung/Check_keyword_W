# Generated by Django 5.0.13 on 2025-06-02 08:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleekweb', '0017_xy_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xy',
            name='Belong_Nation',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='Belong_XY',
        ),
        migrations.RemoveField(
            model_name='xy',
            name='Belong_Region',
        ),
        migrations.RemoveField(
            model_name='video',
            name='Belong_XY',
        ),
        migrations.RemoveField(
            model_name='xy',
            name='Belong_User',
        ),
        migrations.AddField(
            model_name='user',
            name='Money',
            field=models.IntegerField(blank=True, max_length=255, null=True, verbose_name='Tiền'),
        ),
        migrations.CreateModel(
            name='Transaction_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Mã giao dịch')),
                ('Content', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nội dung GD')),
                ('Creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Thời gian tạo')),
                ('Update_time', models.DateTimeField(auto_now=True, verbose_name='Thời gian cập nhật')),
                ('Belong_User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='list_transaction_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Lịch sử giao dịch',
                'ordering': ['id'],
            },
        ),
        migrations.DeleteModel(
            name='Nation',
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
        migrations.DeleteModel(
            name='Video',
        ),
        migrations.DeleteModel(
            name='XY',
        ),
    ]
