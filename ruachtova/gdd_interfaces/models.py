# coding=utf-8

from city_list import *
from django.db import models
from MultiSelectCommaField import *

GDD_FIELDS = [
	(6, 'איכות הסביבה ובעלי חיים'),
	(1, 'אריזה והגשת מזון'),
	(3, 'הפנינג והפעלות'),	
	(5, 'גינון וצביעה'),
	(4, 'סידור, ארגון, שוק קח-תן'),
	(8, 'ציורי קיר'),
	(9, 'אחר'),
]

GDD_GENDERS = (
	(1, 'זכר'),
	(2, 'נקבה'),
)

GDD_STD_FIELDS = [
	(6, 'איכות הסביבה ובעלי חיים'),
	(1, 'אריזה והגשת מזון'),
	(3, 'הפעלה והדרכה'),	
	(7, 'הקמת/חידוש גינה'),	
	(2, 'שינוע וליווי הסעות'),
	(5, 'חידוש וצביעה'),
	(4, 'סידור וארגון'),
	(8, 'ציורי קיר'),
	(9, 'אחר'),
]

GDD_POPULATIONS = [
	(1, 'ילדים'),
	(2, 'קשישים'),
	(3, 'אוכלוסיות מיוחדות'),
	(4, 'אחר'),
]

GDD_COMMUNICATIONS = [
	(1, 'טלפון'),
	(2, 'דוא\"ל'),
	(3, 'פקס'),
]

GDD_TIME = [
	(1, 'בוקר'),
	(2, 'צהריים'),
	(3, 'ערב'),
]

GDD_TYPE = [
	(1, 'מתנדבים יחידים'),
	(2, 'קבוצות מתנדבים'),
	(3, 'מתנדבים יחידים וקבוצות'),
]

GDD_WALL_TYPE = [
	(1, 'חיצוני'),
	(2, 'פנימי'),
	(3, 'גם וגם'),
]

GDD_WALL_colour = (
	(1, 'אדום'),
	(2, 'כחול'),
	(3, 'צהוב'),
)

GDD_PAINT_colour = (
	(1, 'אדום'),
	(2, 'כחול'),
	(3, 'צהוב'),
	(4, 'שחור'),
	(5, 'לבן'),
)

GDD_MATERIAL = (
	(1, 'אדום'),
	(2, 'כחול'),
	(3, 'צהוב'),
	(4, 'שחור'),
	(5, 'לבן'),
)

GDD_ORGINIZER = [
	(1, 'המתנדבים'),
	(2, 'המקום'),
	(3, "בטון"),
]

GDD_MATERIAL = [
	(1, 'מתכת'),
	(2, 'עץ'),
]

GDD_YES_NO = [
	(1, 'כן'),
	(2, 'לא'),
]

GDD_GARDENING_TYPE = [
	(1, 'צמחי תבלין'),
	(2, 'פרחים עונתיים'),
	(3, 'פרחים רב עונתיים'),
]

GDD_GARDEN_TYPE = [
	(1, 'גינון באדניות'),
	(2, 'גינת נוי'),
	(3, 'גינה קהילתית'),
]

class gddMaterial(models.Model):

	gdd_id = models.IntegerField()
	title = models.CharField(max_length=100)
	def __unicode__(self):
		return self.title
	
class gddGardening(models.Model):

	gdd_id = models.IntegerField()
	title = models.CharField(max_length=100)
	def __unicode__(self):
		return self.title
	
class gddField(models.Model):

	gdd_id = models.IntegerField()
	title = models.CharField(max_length=100)
	def __unicode__(self):
		return self.title

class gddColour(models.Model):

	gdd_id = models.IntegerField()
	title = models.CharField(max_length=100)
	is_extended = models.BooleanField()
	def __unicode__(self):
		return self.title

class gddCity(models.Model):

	guid = models.CharField(primary_key=True, max_length=40)
	title = models.CharField(max_length=150)
	is_volunteer_external = models.BooleanField(verbose_name = "האם להציג שדות מתנדבי חוץ",
		blank=True)
	is_logistic_address = models.BooleanField(verbose_name = "האם להציג כתובת הורדת ציוד",
		blank=True)
	is_logistic_contact = models.BooleanField(verbose_name = "האם להציג כתובת הורדת ציוד",
		blank=True)
		
	contact_fname = models.CharField(verbose_name = 'שם פרטי',
		max_length=170)
	contact_lname = models.CharField(verbose_name = 'שם משפחה',
		max_length=170)
	contact_phone_1 = models.CharField(verbose_name = 'טלפון',
		max_length=80)
	contact_phone_2 = models.CharField(verbose_name = 'טלפון נוסף',
		max_length=80,
		blank=True)
	
	logistic_address = models.TextField(verbose_name = 'כתובת הורדת ציוד')
	is_open = models.BooleanField(verbose_name = "האם היישוב פתוח לקליטת מידע",
		blank=True)
class gddLogisticType(models.Model):

	gdd_id = models.IntegerField()
	name = models.CharField(max_length=80)
	title = models.CharField(max_length=100)

class gddCityProject(models.Model):
	
	city = models.ForeignKey('gddCity')
	
	is_data_missing = models.BooleanField(verbose_name = 'מידע חסר')
			
	field = models.ForeignKey('gddField', 
		verbose_name = "תחום הפעילות",
		blank=False) 
	
	logistic_type = models.ManyToManyField("gddLogisticType", 
		verbose_name = "מה תרצו לעשות?",
		blank=True,
		null=True) 
	
	title = models.CharField(verbose_name = "שם פרויקט",
		max_length = 75,
		blank=False)
		
	description = models.TextField(verbose_name = "תיאור הפעילות",
		blank=False)
		
	volunteer_num = models.PositiveIntegerField(verbose_name = "מהו מספר המתנדבים אותם תגייסו?",
		blank=False)
		
	is_volunteer_external = models.BooleanField(verbose_name = "האם היישוב זקוק למתנדבים נוספים שיגוייסו על-ידי רוח טובה?",
		blank=True)
		
	volunteer_num_external = models.PositiveIntegerField(verbose_name = "מהו מספר המתנדבים שיגוייסו על-ידי רוח טובה?",
		blank=True)

	from_time = models.TimeField(verbose_name = "שעת תחילת הפעילות",
		blank=True)
	
	to_time = models.TimeField(verbose_name = "שעת סיום הפעילות",
		blank=True)
	 
	participant_num = models.PositiveIntegerField(verbose_name = "מספר המשתתפים",
		blank=False)
	
	fname = models.CharField(verbose_name = "שם פרטי",
		max_length=50,
		blank=False)
		
	lname = models.CharField(verbose_name = "שם המשפחה",
		max_length=50,
		blank=False)
		
	phone_1 = models.CharField(verbose_name = "טלפון",
		max_length=25,
		blank=False)
		
	email = models.EmailField(verbose_name = "כתובת דוא\"ל",
		blank=True)
		
	position = models.CharField(verbose_name = "תפקיד",
		max_length=50,
		blank=False)
		
	comments = models.TextField(verbose_name = "הערות",
		blank=True)	
	
	logistic_fname = models.CharField(verbose_name = "שם פרטי",
		max_length=50,
		blank=True)
		
	logistic_lname = models.CharField(verbose_name = "שם המשפחה",
		max_length=50,
		blank=True)
		
	logistic_phone_1 = models.CharField(verbose_name = "טלפון",
		max_length=25,
		blank=True)		
	
	city_title = models.CharField(verbose_name = "יישוב",
		max_length = 75,
		blank=True)
	
	street = models.CharField(verbose_name = "רחוב ומספר בית",
		max_length = 225,
		blank=True)

	is_stamped = models.BooleanField(verbose_name = "מיוחד לחברה מסחרית",
		blank=True)
		
class gddCityLogistics(models.Model):

	parent = models.ForeignKey('gddCityProject')

	paint_several = models.IntegerField(verbose_name = "האם הצביעה מתבצעת במספר מוקדים?",
		choices=GDD_YES_NO, 
		blank=True,
		null=True)

	wall_type = models.IntegerField(verbose_name = "האם הקירות הם חיצוניים או פנימיים",
		choices=[('','בחרו')] + GDD_WALL_TYPE, 
		blank=True,
		null=True)

	wall_area = models.DecimalField(max_digits=6,decimal_places=2,verbose_name = "מהו סך שטח כל הקירות שתרצו לצבוע (במ\"ר)?",
		help_text="שטח קיר = אורך הקיר כפול גבוהו",
		blank=True,
		null=True)
	
	wall_colour = models.ManyToManyField("gddColour", 
		verbose_name = "במידה ותרצו לגוון את הצבע הלבן, אנא בחרו את המגוון הרצוי (ניתן לסמן כמה מגוונים)",
		blank=True,
		null=True)
		
	windows_num = models.PositiveIntegerField(verbose_name = "מהי כמות החלונות אותם תרצו לצבוע?",
		blank=True,
		null=True)
		
	windows_material = models.ForeignKey("gddMaterial",
		verbose_name = "האם החלונות עשויים ממתכת או מעץ?",
		related_name = "windows_material",
		blank=True,
		null=True)
	
	windows_colour = models.IntegerField(verbose_name = "באיזה צבע תרצו לצבוע את החלונות",
		choices=GDD_PAINT_colour, 
		blank=True,
		null=True)
		
	doors_num = models.PositiveIntegerField(verbose_name = "מהי כמות הדלתות אותן תרצו לצבוע?",
		blank=True,
		null=True)
		
	doors_material = models.ForeignKey("gddMaterial", 
		verbose_name = "האם הדלתות עשוויות ממתכת או עץ?",
		related_name = "doors_material",
		blank=True,
		null=True)
	
	doors_colour = models.ForeignKey('gddColour',
		verbose_name = "באיזה צבע תרצו לצבוע את הדלתות?",
		related_name = 'doors_colour',
		blank=True,
		null=True)
	
	grate_length = models.PositiveIntegerField(verbose_name = "מהו סך אורך הסורגים אותם תרצו לצבוע?",
		blank=True,
		null=True)
	
	grate_colour = models.ForeignKey('gddColour',
		verbose_name = "באיזה צבע תרצו לצבוע?",
		related_name='grate_colour',
		blank=True,
		null=True)
		
	grate_rusted = models.IntegerField(verbose_name = "האם יש על הסורגים חלודה?",
		choices=GDD_YES_NO, 
		blank=True,
		null=True)
		
	railing_length = models.PositiveIntegerField(verbose_name = "מהו סך אורך המעקות אותם תרצו לצבוע?",
		blank=True,
		null=True)
	
	railing_colour = models.ForeignKey('gddColour',
		related_name='railing_colour',
		verbose_name = "באיזה צבע תרצו לצבוע?",
		blank=True,
		null=True)
		
	railing_rusted = models.IntegerField(verbose_name = "האם יש על המעקות חלודה?",
		choices=GDD_YES_NO, 
		blank=True,
		null=True)

	wallpaint_height = models.DecimalField(max_digits=6,decimal_places=2,verbose_name = "מהו גובה הקיר (במטר)?",
		blank=True,
		null=True)
		
	wallpaint_width = models.DecimalField(max_digits=6,decimal_places=2,verbose_name = "מהו אורך הקיר (במטר)?",
		help_text="ערכה לציור קיר בשטח כ-12 מטר מרובע כוללת 5 אריזות צבע סופרקריל 1 ליטר בצבעים לבן, שחור, אדום, כחול וצהוב, סט מכחולים ו- 5 מברשות 2.5, דף הנחיות לערבוב גוונים וצבעים.",
		blank=True,
		null=True)
			
	gardening_type = models.ManyToManyField("gddGardening", 
		verbose_name = "מה תרצו לשתול?",
		blank=True,
		null=True)
	
	gardening_fence = models.DecimalField(max_digits=6,decimal_places=2,verbose_name = "במידה ותרצו לשתול גדר חיה, מהו אורך הגדר לאורכה תרצו לשתול?",
		blank=True,
		null=True)
	
	gardening_area = models.DecimalField(max_digits=6,decimal_places=2,verbose_name = "מהו שטח האזור בו תרצו לשתול?",
		blank=True,
		null=True)
		
	gardening_planters = models.DecimalField(max_digits=6,decimal_places=2,verbose_name = "אם תרצו לשתול באדניות בלבד, כתבו את כמות האדניות הרצויה",
		blank=True,
		null=True)
	
	facility_material = models.ManyToManyField("gddMaterial", 
		verbose_name = "מאיזה חומר/חומרים עשויים המתקנים?",
		blank=True,
		null=True)
		
	facility_num = models.PositiveIntegerField(verbose_name = "מהו מספר המתקנים אותם תרצו לצבוע?",
		blank=True,
		null=True)
	
	facility_colour = models.ManyToManyField("gddColour", 
		verbose_name = "באיזה צבע תרצו לצבוע? (ניתן לבחור יותר מאחד)",
		related_name = "facility_colour",
		blank=True,
		null=True)

	fence_material = models.ForeignKey('gddMaterial',
		verbose_name = "מאיזה חומר עשויה הגדר?",
		related_name = 'fence_material',
		blank=True,
		null=True)
		
	fence_length = models.PositiveIntegerField(verbose_name = "מהו אורך הגדר אותה תרצו לצבוע?",
		blank=True,
		null=True)
		
	fence_colour = models.ForeignKey("gddColour", 
		verbose_name = "באיזה צבע תרצו לצבוע?)",
		related_name = "fence_colour",
		blank=True,
		null=True)
		
	apartments_num = models.PositiveIntegerField(verbose_name = "כמה דירות ייצבעו?",
		blank=True,
		null=True)
		
	apartments_area = models.DecimalField(max_digits=6,decimal_places=2,verbose_name = "מהו שטחה הממוצע של כל דירה?",
		blank=True,
		null=True)

class DesignForChange(models.Model):

	guid = age = models.CharField(max_length=40,
		blank=False)

	name = models.CharField(verbose_name = "שם מוסד",
		max_length=50,
		blank=False)
	group_name = models.CharField(verbose_name = "שם קבוצה",
		max_length=50,
		blank=False)
	age = models.CharField(verbose_name = "גילאי הקבוצה",
		max_length=50,
		blank=False)
		
	city = models.CharField(verbose_name = "יישוב",
		max_length=50,
		blank=False)
	street = models.CharField(verbose_name = "רחוב ומספר בית",
		max_length=50,
		blank=False)
	zip_code = models.CharField(verbose_name = "מיקוד",
		max_length=50,
		blank=True)
	volunteer_num = models.IntegerField(verbose_name = "מספר החברים בקבוצה",
		blank=False)
		
	fname = models.CharField(verbose_name = "שם פרטי",
		max_length=50,
		blank=False)
	lname = models.CharField(verbose_name = "שם משפחה",
		max_length=50,
		blank=False)
	phone_1 = models.CharField(verbose_name = "טלפון",
		max_length=50,
		blank=False)
	phone_2 = models.CharField(verbose_name = "טלפון נוסף",
		max_length=50,
		blank=True)
	email = models.CharField(verbose_name = "כתובת דוא\"ל",
		help_text='הכתובת באמצעותה ניצור עמך קשר, ונשלח אליך קישורים להמשך הרישום',
		max_length=75,
		blank=False)
	url = models.CharField(verbose_name = "כתובת אתר/פייסבוק",
		max_length=150,
		blank=True)
		
	problem_name = models.CharField(verbose_name = "אנא תנו שם לבעיה (בחרו שם קצר וממוקד המתאר באופן הטוב ביותר את הבעיה)",
		max_length=150,
		blank=False)	
	problem_description = models.TextField(verbose_name = "אנא מלאו מהי הבעיה אותה תרצו לפתור",
		blank=False)
		
	project_name = models.CharField(verbose_name = "מהו הפתרון הנבחר וכיצד הוא השפיע על הסביבה ועליכם. דווחו על מס' המשתתפים וגם על מספר האנשים שהושפעו מהשינוי",
		max_length=150,
		blank=False)	
	project_description = models.TextField(verbose_name = "תנו כותרת לסיפור השינוי שיצרתם",
		blank=False)
  
class DesignForChangeFiles(models.Model):
	parent = models.ForeignKey(DesignForChange)
	media_file = models.FileField(upload_to="upload/gdd/dfcmedia", verbose_name="Upload a picture")
	media_type = models.CharField(max_length=10, verbose_name="Project Name")


		
class gddCityGroup(models.Model):
	
	city = models.ForeignKey('gddCity')
	
	group_name = models.CharField(verbose_name = "שם קבוצה",
		max_length=150,
		blank=True)
	volunteer_num = models.IntegerField(verbose_name = "מספר המתנדבים בקבוצה",
		blank=True)
	group_ages = models.CharField(verbose_name = "גילאי הקבוצה",
		max_length=150,
		blank=False)
	description = models.CharField(verbose_name = "תיאור הקבוצה",
		max_length=1500,
		blank=False)
	cityId = models.IntegerField(verbose_name = "יישוב",
		choices = [('','בחרו')] + GDD_CITIES,
		blank=True)
		 
	fname = models.CharField(verbose_name = "שם פרטי",
		max_length=150,
		blank=True)
	lname = models.CharField(verbose_name = "שם משפחה",
		max_length=150,
		blank=True)
	 
	phone_1 = models.CharField(verbose_name = "טלפון",
		max_length=150,
		blank=True)
	phone_2 = models.CharField(verbose_name = "טלפון נוסף",
		max_length=150,
		blank=False)
	email = models.CharField(verbose_name = "כתובת דוא\"ל",
		max_length=150,
		blank=False)
	genderId = models.IntegerField(verbose_name="מין",
		choices=GDD_GENDERS,
		blank=False)
	
	comments = models.CharField(verbose_name = "הערות",
		max_length=1500,
		blank=True)
		