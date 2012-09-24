# coding=utf-8

from django.db import models

class VolunteerDomainDictionary(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	he_title = models.CharField(max_length=800)
	ar_title = models.CharField(max_length=800)
	type = models.CharField(max_length=200)
	
class Grade(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	title = models.CharField(max_length=800)
	
class Projects(models.Model):
	project_id = models.PositiveIntegerField()
	title = models.CharField(max_length=2000)
	description = models.TextField()
	field = models.ForeignKey('Field')
	area = models.ForeignKey('Area')
	population = models.ForeignKey('Population')
	parent = models.CharField(max_length=1000)
	
class Field(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	title = models.CharField(max_length=800)
	
class Area(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	title = models.CharField(max_length=800)
	
class Population(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	title = models.CharField(max_length=800)

class City(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	title = models.CharField(max_length=800)

class Feedback(models.Model):

	guid = models.CharField(max_length=40, 
		verbose_name = '')
		
	service_quality = models.ForeignKey(Grade, 
		blank= True,
		null=True,
		related_name='+',
		verbose_name = 'מהי מידת שביעות רצונך מהשירות שניתן לך על ידי רוח טובה?')
	rep_service_quality = models.ForeignKey(Grade, 
		blank= True,
		null=True,
		related_name='+',
		verbose_name = 'מהי מידת שביעות רצונך מאדיבות נציגנו ונכונותם לעזור?')
	rep_profesionality = models.ForeignKey(Grade, 
		blank= True,
		null=True,
		related_name='+',
		verbose_name = 'מהי מידת שביעות רצונך ממקצועיות הנציג/ה  ממנו/ה קיבלת מענה?')
	volunteering_options_diversity = models.ForeignKey(Grade, 
		blank= True,
		null=True,
		related_name='+',
		verbose_name = 'מהי מידת שביעות רצונך ממגוון אפשרויות ההתנדבות שהוצע לך?')
	rep_availability = models.ForeignKey(Grade, 
		blank= True,
		null=True,
		related_name='+',
		verbose_name = 'מהי מידת שביעות רצונך מזמינות נציגנו  במהלך התהליך?')
	process_length = models.ForeignKey(Grade, 
		blank= True,
		null=True,
		related_name='+',
		verbose_name = 'מהי מידת שביעות רצונך ממשך התהליך מרגע פנייתך ועד השלמתו?')
	process_quality = models.ForeignKey(Grade, 
		blank= True,
		null=True,
		related_name='+',
		verbose_name = 'מהי מידת שביעות רצונך מהתהליך שעברת ברוח טובה ביחס לציפיותיך הראשוניות?')
	
	comment = models.CharField(max_length=1000, 
		blank= True,
		verbose_name = 'מה כדאי לשפר או לשמר בשירות שניתן לך? נשמח לשמוע כל הערה, הצעה או מחמאה...')
