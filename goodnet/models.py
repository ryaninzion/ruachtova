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

class Initiative(models.Model):
	ongoing = models.BooleanField("חד פעמי")
	title = models.CharField("",max_length=100)	
