from django.db import models
import os
from django.conf import settings
# Create your models here.

class User(models.Model):
	user_name = models.CharField(max_length=200,unique=True)
	user_password = models.CharField(max_length=20)


class Image(models.Model):
	"""docstring for Image"""
	user_name = models.ForeignKey(User,models.CASCADE)
	url = models.CharField(max_length=200,default='null')


class Music(models.Model):
	"""docstring for music"""
	user_name = models.ForeignKey(User,models.CASCADE)
	song_name = models.CharField(max_length=200,default='null')
	singer_name = models.CharField(max_length=200,default='null')
	url = models.CharField(max_length=200,default='null')


class Video(models.Model):
	"""docstring for Video"""
	user_name = models.ForeignKey(User,models.CASCADE)
	url = models.CharField(max_length=200,default='null')
	video_name = models.CharField(max_length=200,default='null')


class Document(models.Model):
	"""docstring for Document"""
	user_name = models.ForeignKey(User,models.CASCADE)
	url = models.CharField(max_length=200,default='null')
	author = models.CharField(max_length=50,default='null')
	title = models.CharField(max_length=50,default='null')
	date = models.DateField()
	content = models.TextField(default='#')