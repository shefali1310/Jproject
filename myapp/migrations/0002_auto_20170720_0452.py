# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 04:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_token', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_valid', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
        migrations.RemoveField(
            model_name='user',
            name='has_verified_mobile',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='Anonymous', max_length=254),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='Anonymous', max_length=40),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='Anonymous', max_length=120),
        ),
        migrations.AddField(
            model_name='sessiontoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.User'),
        ),
    ]
