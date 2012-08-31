# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Category(models.Model):
	title 		= models.CharField("שם",max_length=100)
	icon 		= models.ImageField("איקון",upload_to="images/cat-icons/")
	CATEGORY_TYPE_CHOICES = (
	('post', 'קטגוריה של פוסט, אירוע או יוזמה אישית'),
	('profile', 'קטגוריה של ארגון או חבר'),
	)
	cat_type	= models.CharField("סוג קטגוריה", max_length=100, choices=CATEGORY_TYPE_CHOICES)

	class Meta:
		verbose_name = "קטגוריה"
		verbose_name_plural = "קטגוריות"

	def __unicode__(self): return self.title


class Area(models.Model):
	name		= models.CharField("שם", max_length=100)

	class Meta:
		verbose_name = "אזור"
		verbose_name_plural = "אזורים"

	def __unicode__(self): return self.name



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


class Profile(models.Model):
	user		= models.OneToOneField(User)
	PROFILE_TYPE_CHOICES = (
	('org', 'פרופיל ארגון'),
	('personal', 'פרופיל חבר'),
	)
	profile_type	= models.CharField("סוג הפרופיל", max_length=100, choices=PROFILE_TYPE_CHOICES) 
	name		= models.CharField("שם", max_length=100, blank=True, null=True)
	avatar		= models.ImageField("תמונה", upload_to="images/avatars/", blank=True, null=True)
	agreement	= models.BooleanField()
	datebirth	= models.DateField("תאריך לידה", blank=True, null=True)
	phone		= models.CharField("מספר טלפון", max_length=100, blank=True, null=True)
	website		= models.URLField("אתר אינטרנט", blank=True, null=True)
	facebook	= models.URLField("פרופיל פייסבוק", blank=True, null=True)
	desc		= models.TextField("תאור", blank=True, null=True)
	categories	= models.ManyToManyField(Category, blank=True, null=True)
	area		= models.ManyToManyField(Area, blank=True, null=True)	
	likes		= models.ManyToManyField(Post, blank=True, null=True, related_name='liked')
	causes_joined	= models.ManyToManyField(Post, blank=True, null=True, related_name='our_helpers')

	class Meta:
		verbose_name = "פרופיל"
		verbose_name_plural = "פרופילים"

	#def __unicode__(self): return self.name	


#def create_user_profile_callback(sender, instance, **kwargs):
#	profile, new = Profile.objects.get_or_create(user=instance)
#post_save.connect(create_user_profile_callback, User)
