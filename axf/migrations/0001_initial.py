# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-05-27 02:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AxfUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_username', models.CharField(max_length=30, verbose_name='用户名')),
                ('u_password', models.CharField(max_length=255, verbose_name='密码')),
                ('u_email', models.EmailField(max_length=254, verbose_name='邮箱')),
            ],
        ),
    ]