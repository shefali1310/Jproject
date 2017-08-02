# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid



# Create your models here.

class User(models.Model):
    email = models.EmailField(default = 'Anonymous')
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=120, default = 'Anonymous')
    password = models.CharField(max_length=40, default = 'Anonymous')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class SessionToken(models.Model):
    user = models.ForeignKey(User)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()




class Post(models.Models):
    user = models.ForeignKEy(UserModdel)
    image = models.FileField()
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    has_liked = False

    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))

    @property
    def comments(self):
        return CommentModel.objects.filter(post=self).order_by('-created_on')

class clarifai_data(models.Model):
	user = models.ForeignKey(UserModel)
	clarifai_data = models.CharField(max_length=100)
	created_on = models.DateTimeField(auto_now_add=True)

class LikeModel(models.Model):
	user = models.ForeignKey(UserModel)
	post = models.ForeignKey(PostModel)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
	user = models.ForeignKey(UserModel)
	post = models.ForeignKey(PostModel)
	comment_text = models.CharField(max_length=555)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)