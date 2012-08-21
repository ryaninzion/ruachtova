# -*- coding: utf-8 -*-

from django.db import models

class Event(models.Model):
	date =  models.DateField("תאריך")
	title = models.CharField("כותרת",max_length=100)
	desc = models.TextField("תיאור")
	location = models.CharField("מיקום",max_length=100)

	class Meta:
		verbose_name = "אירוע"
		verbose_name_plural = "אירועים"

	def __unicode__(self): return self.title


class Post(models.Model):
	title = models.CharField("כותרת",max_length=100)
	POST_TYPE_CHOICES = (
       	('post', 'פוסט'),
       	('event', 'אירוע'),
	('initiative', 'יוזמה אישית'),
   	)
	post_type = models.CharField("סוג הפעילות",max_length=1, choices=POST_TYPE_CHOICES)
	post_image = models.ImageField("תמונה",upload_to="images/posts/") 
	start_date = models.DateTimeField("תאריך ושעה")
	end_date = models.DateTimeField("עד תאריך ושעה", null=True)
	ongoing = models.BooleanField("חד פעמי?")
	location = models.CharField("מיקום",max_length=100)
	address = models.CharField("רחוב ומםפר",max_length=100)
	desc = models.TextField("מידע נוסף")

	def __unicode__(self): return self.title

class Category(models.Model):
	title = models.CharField("שם",max_length=100)
	icon = models.ImageField("איקון",upload_to="images/cat-icons/")

	class Meta:
		verbose_name = "קטגוריה"
		verbose_name_plural = "קטגןריות"
