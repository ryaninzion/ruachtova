# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	date =  models.DateField("תאריך")
	title = models.CharField("כותרת",max_length=100)
	desc = models.TextField("תיאור")
	location = models.CharField("מיקום",max_length=100)

	class Meta:
		verbose_name = "אירוע"
		verbose_name_plural = "אירועים"

	def __unicode__(self): return self.title



class Category(models.Model):
	title = models.CharField("שם",max_length=100)
	icon = models.ImageField("איקון",upload_to="images/cat-icons/")

	class Meta:
		verbose_name = "קטגוריה"
		verbose_name_plural = "קטגוריות"

	def __unicode__(self): return self.title


class Post(models.Model):
	title = models.CharField("כותרת",max_length=100)
	author = models.ForeignKey(User)
	POST_TYPE_CHOICES = (
       	('post', 'פוסט'),
       	('event', 'אירוע'),
	('initiative', 'יוזמה אישית'),
   	)
	post_type = models.CharField("סוג הפעילות",max_length=100, choices=POST_TYPE_CHOICES)
	post_image = models.ImageField("תמונה",upload_to="images/posts/") 
	category = models.ForeignKey(Category, verbose_name=u"קטגוריה")
	start_date = models.DateTimeField("תאריך ושעה")
	end_date = models.DateTimeField("עד תאריך ושעה", blank=True, null=True)
	ongoing = models.BooleanField("חד פעמי?")
	location = models.CharField("מיקום",max_length=100)
	address = models.CharField("רחוב ומםפר",max_length=100)
	desc = models.TextField("מידע נוסף")
	tags = models.CharField("תגיות",max_length=100)
	created_on = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "פוסט"
		verbose_name_plural = "פוסטים"

	def __unicode__(self): return self.title

