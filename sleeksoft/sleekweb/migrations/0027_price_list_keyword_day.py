# Generated by Django 5.0.13 on 2025-06-04 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleekweb', '0026_alter_keyword_belong_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='price_list',
            name='Keyword_day',
            field=models.IntegerField(blank=True, default=0, max_length=100, null=True, verbose_name='Số từ khoá 1 ngày'),
        ),
    ]
