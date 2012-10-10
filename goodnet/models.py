# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings
from datetime import datetime
from PIL import Image
import os


class Category(models.Model):
	title 		= models.CharField("שם",max_length=100)
	icon 		= models.ImageField("איקון",upload_to="images/cat-icons/")
	CATEGORY_TYPE_CHOICES = (
	('post', 'קטגוריה של פוסט, אירוע או יוזמה אישית'),
	('profile', 'קטגוריה של ארגון או חבר'),
	)
	type	= models.CharField("סוג קטגוריה", max_length=100, choices=CATEGORY_TYPE_CHOICES)

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


class AbstractMedia(models.Model):
	desc 		= models.TextField("תאור", blank=True, null=True)
	date 		= models.DateTimeField("תאריך", default=datetime.now())
	creator		= models.ForeignKey(User)

	class Meta:
		ordering = ['-date']


class Photo(AbstractMedia):
	image 		= models.ImageField("תמונה", upload_to="images/gallery-photos/")
	thumb 		= models.ImageField(upload_to="images/gallery-thumbnails/", editable=False)

	def save(self, force_insert=False, force_update=False):
		super(Photo, self).save(force_insert, force_update)
		if self.image and not self.thumb:
			# Set the thumbnail size and maximum size.
			t_size = 100, 80
			max_size = 800, 600
			# Open the image that was uploaded.
			im = Image.open(settings.MEDIA_ROOT + '/' + str(self.image))
			# Compare the image size against the maximum size. If it is greater, the image will be resized.
			if im.size > max_size:
				# Using 'thumbnail', instead of 'resize', keeps the aspect ratio of the image.
				resize = im.thumbnail(max_size)
				resize.save(settings.MEDIA_ROOT + '/' + str(self.image))
			# Create the thumbnail and save the path to the database.
			im.thumbnail(t_size)
			im.save(settings.MEDIA_ROOT + '/' + os.path.splitext(str(self.image))[0] + ".thumbnail.jpg", "JPEG")
			self.thumb = os.path.splitext(str(self.image))[0] + ".thumbnail" + ".jpg"
			super(Photo, self).save(force_insert, force_update)


class Video(AbstractMedia):
#	video		= models.FileField("וידאו", upload_to=video_file_path)
	link		= models.CharField("כתובת וידאו",max_length=100)

	class Meta:
		verbose_name = "וידאו"
		verbose_name_plural = "וידאו"

	def __unicode__(self): return self.title


class AbstractPost(models.Model):
	title = models.CharField("כותרת",max_length=100)
	author = models.ForeignKey(User)
	image = models.ImageField("תמונה",upload_to="images/posts/") 
	category = models.ForeignKey(Category, verbose_name=u"קטגוריה",limit_choices_to={'type':'post'})
	desc = models.TextField("מידע נוסף")
	tags = models.CharField("תגיות",max_length=100)
	cdate = models.DateTimeField(auto_now_add=True)
	def __unicode__(self): return self.title

	@models.permalink
	def get_absolute_url(self):
		return ('goodnet.views.post', [str(self.id)])

class Post(AbstractPost):

	class Meta:
		verbose_name = "פוסט"
		verbose_name_plural = "פוסטים"

class Event(AbstractPost):
	date = models.DateTimeField("תאריך ושעה")
	location = models.ForeignKey(Area, verbose_name=u"מיקום")
	address = models.CharField("רחוב ומםפר",max_length=100)

	class Meta:
		verbose_name = "אירוע"
		verbose_name_plural = "אירועים"

	@models.permalink
	def get_absolute_url(self):
		return ('goodnet.views.event', [str(self.id)])

class Initiative(AbstractPost):
	start_date = models.DateTimeField("תאריך ושעה")
	end_date = models.DateTimeField("עד תאריך ושעה", blank=True, null=True)
	ongoing = models.BooleanField("מתמשך?")
	location = models.ForeignKey(Area, verbose_name=u"מיקום")
	address = models.CharField("רחוב ומםפר",max_length=100)

	class Meta:
		verbose_name = "יוזמה"
		verbose_name_plural = "יוזמות"



class Profile(models.Model):
	user		= models.OneToOneField(User)
	PROFILE_TYPE_CHOICES = (
	('o', 'פרופיל ארגון'),
	('p', 'פרופיל חבר'),
	)
	profile_type	= models.CharField("סוג הפרופיל", max_length=1, choices=PROFILE_TYPE_CHOICES) 
	name		= models.CharField("שם", max_length=100, default="פרופיל חדש")
	avatar		= models.ImageField("תמונה", upload_to="images/avatars/", blank=True, null=True)
	agreement	= models.BooleanField()
	datebirth	= models.DateField("תאריך לידה", blank=True, null=True)
	phone		= models.CharField("מספר טלפון", max_length=15, blank=True, null=True)
	website		= models.URLField("אתר אינטרנט", blank=True, null=True)
	facebook	= models.URLField("פרופיל פייסבוק", blank=True, null=True)
	desc		= models.TextField("תאור", blank=True, null=True)
	categories	= models.ManyToManyField(Category, blank=True, null=True, default="",verbose_name="קטגוריות",limit_choices_to={'type':'profile'})
	areas		= models.ManyToManyField(Area, blank=True, null=True, default="",verbose_name="אזורים")	
	likes		= models.ManyToManyField(AbstractPost, blank=True, null=True, related_name='liked', default="")
	causes_joined	= models.ManyToManyField(AbstractPost, blank=True, null=True, related_name='our_helpers', default="")
	friends		= models.ManyToManyField("self", blank=True, null=True, symmetrical=False, related_name='friendlies', default="")

	class Meta:
		verbose_name = "פרופיל"
		verbose_name_plural = "פרופילים"

	def __unicode__(self): return self.name	
	
	@models.permalink
	def get_absolute_url(self):
		return ('goodnet.views.profile', [str(self.id)])


#def create_user_profile_callback(sender, instance, **kwargs):
#	profile, new = Profile.objects.get_or_create(user=instance)
#post_save.connect(create_user_profile_callback, User)
