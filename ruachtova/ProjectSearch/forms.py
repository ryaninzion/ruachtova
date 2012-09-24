# coding=utf-8

import os
from django import forms
from ProjectSearch.SelectTimeWidget import *
from ProjectSearch.models import *
from ProjectSearch.city_list import *
from django.contrib.formtools.wizard import FormWizard
from django.forms.forms import BoundField
from django.utils.translation import gettext_lazy as _

from django.http import HttpResponse

from django.template.loader import *

from django.shortcuts import *

from datetime import *
import codecs

 
FIELDS = [(field.id, field.title) for field in Field.objects.all()]
AREAS = [(area.id, area.title) for area in Area.objects.all()]
POPULATIONS = [(population.id, population.title) for population in Population.objects.all()]
CITIES = [(city.id, city.title) for city in City.objects.all().order_by('title')]
GRADES = [(grade.id, grade.title) for grade in Grade.objects.all().order_by('-id')]

ARABIC_FIELDS = [(field.id, field.ar_title) for field in VolunteerDomainDictionary.objects.filter(type = 'field')]
ARABIC_AREAS = [(area.id, area.ar_title) for area in VolunteerDomainDictionary.objects.filter(type = 'area')]
ARABIC_POPULATIONS = [(population.id, population.ar_title) for population in VolunteerDomainDictionary.objects.filter(type = 'population')]


GENDERS = (
	(21, 'זכר'),
	(22, 'נקבה'),
)

DAYS = (
	(162, 'ראשון'),
	(163, 'שני'),
	(164, 'שלישי'),
	(165, 'רביעי'),
	(166, 'חמישי'),
	(167, 'שישי'),
	(168, 'שבת'),
)

HOURS = (
	(170, 'בוקר'),
	(171, 'צהריים'),
	(266, 'אחרה"צ'),
	(172, 'ערב'),
	(173, 'לילה'),
)

LANGUAGES = (
	(97, 'עברית'),
	(98, 'אנגלית'),
	(99, 'רוסית'),
	(100, 'אמהרית'),
	(101, 'ערבית'),
	(102, 'צרפתית'),
	(103, 'ספרדית'),
	(104, 'אידיש'),
)

ARABIC_GENDERS = (
	(21, 'ذكر'),
	(22, 'أنثى'),
)

ARABIC_DAYS = (
	(162, 'الاحد'),
	(163, 'الاثنين'),
	(164, 'الثلاثاء'),
	(165, 'الاربعاء'),
	(166, 'الخميس'),
	(167, 'الجمعة'),
	(168, 'السبت'),
)

ARABIC_HOURS = (
	(170, 'الصباح'),
	(171, 'الظهر'),
	(266, 'العصر '),
	(172, 'المساء '),
	(173, 'ساعات الليل'),
)
 
ARABIC_LANGUAGES = (
	(97, 'العبريه'),
	(98, 'الانجليزيه'),
	(101, 'العربية'),
	(102, 'ألفرنسيه'),
	(103, 'الاسبانية'),
)

HOURS = [('','בחרו'),
        ('06:00:00','06:00'),
        ('06:30:00','06:30'),
		('07:00:00','07:00'),
        ('07:30:00','07:30'),
		('08:00:00','08:00'),
        ('08:30:00','08:30'),
		('09:00:00','09:00'),
        ('09:30:00','09:30'),
		('10:00:00','10:00'),
        ('10:30:00','10:30'),
		('11:00:00','11:00'),
        ('11:30:00','11:30'),
		('12:00:00','12:00'),
        ('12:30:00','12:30'),
		('13:00:00','13:00'),
        ('13:30:00','13:30'),
		('14:00:00','14:00'),
        ('14:30:00','14:30'),
		('15:00:00','15:00'),
        ('15:30:00','15:30'),
		('16:00:00','16:00'),
        ('16:30:00','16:30'),
		('17:00:00','17:00'),
        ('17:30:00','17:30'),
		('18:00:00','18:00'),
        ('18:30:00','18:30'),
		('19:00:00','19:00'),
        ('19:30:00','19:30'),
		('20:00:00','20:00'),
        ('20:30:00','20:30'),
		('21:00:00','21:00'),
        ('21:30:00','21:30'),
		('22:00:00','22:00'),
        ('22:30:00','22:30'),]


class SearchForm(forms.Form):

	field = forms.ChoiceField(choices=[('','תחום')] + FIELDS, required=False)
	area = forms.ChoiceField(choices=[('','אזור')] + AREAS + [('1414','אוניברסיטת בן גוריון')], required=False)
	population = forms.ChoiceField(choices=[('','אוכלוסייה')] + POPULATIONS, required=False)
	words = forms.CharField(initial="חיפוש חופשי", required=False)
	
class VolunteerForm(forms.Form):
			
	fname = forms.CharField(label = "שם פרטי",
		required=True)
	lname = forms.CharField(label = "שם משפחה", 
		required=False)
	identity_num = forms.CharField(label = "מספר ת.ז.", 
		required=False)
	gender = forms.ChoiceField(label="מין",
		choices=GENDERS,
		widget=forms.RadioSelect(),
		required=False)
	street = forms.CharField(label = "רחוב ומספר", 
		required=False)
	city = forms.ChoiceField(label="יישוב",
		choices=[('','יישוב')] + CITIES,
		required=True)
	phone = forms.CharField(label = "טלפון",
		required=True) 
	cell = forms.CharField(label = "טלפון נוסף",
		required=False) 
	email = forms.CharField(label = "כתובת דוא\"ל",
		required=False) 

	B111 = forms.CharField(label = "האם יש מקום התנדבות שאת/ה מעוניין/ת להתנדב בו",
		required=False,
		widget=forms.Textarea()) 
	
	# field = forms.MultipleChoiceField(label="אופי ההתנדבות המועדף",
		# choices=FIELDS,
		# required=False,
		# widget=forms.CheckboxSelectMultiple())
	# population = forms.MultipleChoiceField(label="אני מעדיף לעבוד עם אנשים בגילאי",
		# choices=POPULATIONS,
		# required=False,
		# widget=forms.CheckboxSelectMultiple())
	# days = forms.MultipleChoiceField(label="ימים מועדפים להתנדבות",
		# choices=DAYS,
		# required=False,
		# widget=forms.CheckboxSelectMultiple())
	# hours = forms.MultipleChoiceField(label="באילו שעות?",
		# choices=HOURS,
		# required=False,
		# widget=forms.CheckboxSelectMultiple())
	
	B107 = forms.CharField(label = "נסיון קודם בעבודה התנדבותית (אם יש)",
		required=False,
		widget=forms.Textarea())
	
	proffesion = forms.CharField(label = "מקצוע",
		required=False) 
		
	B181 = forms.CharField(label = "תחביבים, כישורים או הערות ופרטים נוספים שהינך מעוניין/ת להוסיף:",
		required=False,
		widget=forms.Textarea())

	
class ArabicVolunteerForm(forms.Form):
	
	fname = forms.CharField(label = "الاسم")
	lname = forms.CharField(label = "ألعائله", 
		required=False)
	identity_num = forms.CharField(label = "رقم الهويه", 
		required=False)
	gendr = forms.ChoiceField(label="الجنس",
		choices=ARABIC_GENDERS,
		widget=forms.RadioSelect(),
		required=False)
	street = forms.CharField(label = "اسم الشارع ورقمه", required=False)
	city = forms.ChoiceField(label="مكان السكن",
		choices=CITIES)
	phone_1 = forms.CharField(label = "هاتف") 
	phone_2 = forms.CharField(label = "هاتف إضافي",
		required=False) 
	email = forms.CharField(label = "البريد الالكتروني") 

	field = forms.MultipleChoiceField(label="مجال التطوع المفضل",
		choices=ARABIC_FIELDS,
		required=False,
		widget=forms.CheckboxSelectMultiple())
	population = forms.MultipleChoiceField(label="اختاروا الجمهور",
		choices=ARABIC_POPULATIONS,
		required=False,
		widget=forms.CheckboxSelectMultiple())
	days = forms.MultipleChoiceField(label="الايام المفضله للتطوع",
		choices=ARABIC_DAYS,
		required=False,
		widget=forms.CheckboxSelectMultiple())
	hours = forms.MultipleChoiceField(label="اختاروا وقت التطوع المفضل",
		choices=ARABIC_HOURS,
		required=False,
		widget=forms.CheckboxSelectMultiple())
	
	languages = forms.MultipleChoiceField(label="لغات",
		choices=ARABIC_LANGUAGES,
		required=False, 
		widget=forms.CheckboxSelectMultiple())
	
	proffesion = forms.CharField(label = "مهنه",
		required=False) 
	
	experience = forms.CharField(label = "تجربة سابقة في العمل التطوعي (إذا كان هناك)",
		required=False,
		widget=forms.Textarea())
	
	comments = forms.CharField(label = "مزيد من المعلومات والملاحظات ",
		required=False,
		widget=forms.Textarea())

# class ArabicOrganizationForm(forms.Form):
 
class ArabicProjectForm(forms.Form):

	title = forms.CharField(label = "عنوان المشروع-")
	parent = forms.CharField(label = "المنظمة الرئيسية")
	description = forms.CharField(label = "وصف المشروع",
		required=False,
		widget=forms.Textarea())

	street = forms.CharField(label = "اسم الشارع ورقمه", required=False)
	city = forms.ChoiceField(label="البلد",
		choices=CITIES)
	phone_1 = forms.CharField(label = "هاتف") 
	phone_2 = forms.CharField(label = "هاتف إضافي",
		required=False) 
	fax = forms.CharField(label = "فاكس", 
		required=False) 
	email = forms.CharField(label = "البريد الالكتروني") 
	
	volunteer_num = forms.CharField(label = "عدد المتطوعين المطلوب للمشروع") 

	field = forms.MultipleChoiceField(label="مجال التطوع",
		choices=ARABIC_FIELDS,
		required=False,
		widget=forms.CheckboxSelectMultiple())
		
	population = forms.MultipleChoiceField(label="اختاروا الجمهور",
		choices=ARABIC_POPULATIONS,
		required=False,
		widget=forms.CheckboxSelectMultiple())
		
	days = forms.MultipleChoiceField(label="وتيرة العمل التطوع",
		choices=ARABIC_DAYS,
		required=False, 
		widget=forms.CheckboxSelectMultiple())
		
	hours = forms.MultipleChoiceField(label="اختاروا وقت التطوع المفضل",
		choices=ARABIC_HOURS,
		required=False,
		widget=forms.CheckboxSelectMultiple())
	
	languages = forms.MultipleChoiceField(label="لغات",
		choices=ARABIC_LANGUAGES,
		required=False,
		widget=forms.CheckboxSelectMultiple())
		
	proffesion = forms.CharField(label = "مهنه",
		required=False) 
	
	volunteer_profile = forms.CharField(label = "مواصفات المتطوع المطلوب ",
		required=False,
		widget=forms.Textarea())
		
	comments = forms.CharField(label = "مزيد من المعلومات والملاحظات ",
		required=False,
		widget=forms.Textarea())
 
class FeedbackForm(forms.ModelForm):

	class Meta:
		model = Feedback
		exclude = ('id', 'name', 'city')
		widgets = {
            'comment': forms.Textarea(),
			'guid': forms.HiddenInput()
        }

	def __init__(self, *args, **kwargs):
		super(FeedbackForm, self).__init__(*args, **kwargs)

		RadioFields = ['service_quality', 'rep_service_quality', 'rep_profesionality', 'volunteering_options_diversity', 'rep_availability', 'process_length', 'process_quality']
		for field in RadioFields:
			self.fields[field].widget = forms.RadioSelect(choices = GRADES)
			
		# HiddenFields = ['id', 'name', 'city']
		# for field in HiddenFields:
			# self.fields[field].widget = forms.HiddenInput()

class FieldStack(object):
	def __init__(self, fields, title, help_text):
		self.fields = fields
		self.title = title
		self.help_text = help_text
		
	def __get__(self, form, objtype=None):
		for field in self.fields:
			yield BoundField(form, form.fields[field], field)
			
GDD_FIELDS = [
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

GDD_WALL_COLOR = [
	(1, 'אדום'),
	(2, 'כחול'),
	(4, 'צהוב'),
]

GDD_PAINT_COLOR = [
	(1, 'אדום'),
	(2, 'כחול'),
	(3, 'צהוב'),
	(4, 'שחור'),
	(5, 'לבן'),
]

GDD_METAL_COLOR = [
	(1, 'אדום'),
	(2, 'כחול'),
	(3, 'ירוק'),
]

GDD_MATERIAL = [
	(1, 'אדום'),
	(2, 'כחול'),
	(3, 'צהוב'),
	(4, 'שחור'),
	(5, 'לבן'),
]

GDD_ORGINIZER = [
	(1, 'המתנדבים'),
	(2, 'המקום'),
	(3, "בטון"),
]

GDD_MATERIAL = [
	(1, 'עץ'),
	(2, 'מתכת'),
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
 
 #GDD_GARDENING_FIELDS = [
 #]
 
 #GDD_PAINTING_FIELDS = [
 #]
 
class gddVolunteerForm(forms.Form):
	
	project_id = forms.CharField(label = "",
		required=False,
		widget=forms.HiddenInput())
	
	fname = forms.CharField(label = "שם פרטי",
		required=True)
	lname = forms.CharField(label = "שם משפחה",
		required=True)
	
	phone_1 = forms.CharField(label = "טלפון",
		required=True)
	phone_2 = forms.CharField(label = "טלפון נוסף",
		required=False)
	email = forms.CharField(label = "כתובת דוא\"ל",
		required=False)
	
	field = forms.MultipleChoiceField(label = "תחום הפעילות",
		choices=GDD_FIELDS, 
		required=False,
		widget=forms.CheckboxSelectMultiple())
	population = forms.MultipleChoiceField(label = "אוכלוסייה",
		choices=GDD_POPULATIONS, 
		required=False,
		widget=forms.CheckboxSelectMultiple())
	time = forms.MultipleChoiceField(label = "שעות ההתנדבות",
		choices=GDD_TIME, 
		required=False,
		widget=forms.CheckboxSelectMultiple())
		
	comments = forms.CharField(label = "הערות",
		required=False,
		widget=forms.Textarea())
	
class gddProjectFormCalculate(forms.Form):
	pass
	
	
class gddProjectFormPlace(forms.Form):
	
	owner = forms.CharField(label='',
		widget = forms.HiddenInput(),
		required=False) 
	
	title = forms.CharField(label = _("שם המקום"),
		widget=forms.TextInput(attrs = { 'placeholder': _("שם הארגון או המוסד בו מתקיימת הפעילות") }),
		required=True)
	place_description = forms.CharField(label = _("תיאור מקום ההתנדבות"),
		widget=forms.Textarea(attrs = { 'placeholder': _("תיאור הפעילות המתקיימת במקום במשך כל השנה") }),
		required=True)
	
	is_accesible = forms.ChoiceField(label="האם המקום נגיש לבעלי נכויות?",
			choices=((True, 'כן'), (False, 'לא')),
			required=False,
			widget=forms.RadioSelect)
			
	populationId = forms.ChoiceField(label = _("האוכלוסייה עמה עובד המקום"),
		choices=[('',_('איזו אוכלוסייה משרת המקום'))] + GDD_POPULATIONS, 
		required=False)
	
	organization_name = forms.CharField(label = _("שם ארגון הגג"),
		required=False)
		
	cityId = forms.ChoiceField(label = _("יישוב"),
		choices = [('',_('בחרו'))] + GDD_CITIES,
		required=True)
	street = forms.CharField(label = _("רחוב ומספר בית"),
		required=True)
		
	logistic_cityId = forms.ChoiceField(label = _("יישוב"),
		choices = [('',_('בחרו'))] + GDD_CITIES,
		required=False)
	logistic_street = forms.CharField(label = _("רחוב ומספר בית"),
		required=False)
	
	fname = forms.CharField(label = _("שם פרטי"),
		required=True)
	lname = forms.CharField(label = _("שם המשפחה"),
		required=True)
	phone_1 = forms.CharField(label = _("טלפון"),
		required=True)
	phone_2 = forms.CharField(label = _("טלפון נוסף"),
		required=False)
	fax = forms.CharField(label = _("פקס"),
		required=False)
	email = forms.EmailField(label = _("כתובת דוא\"ל"),
		required=False)
	position = forms.CharField(label = _("תפקיד"),
		required=False)
		
	place_fields = FieldStack(title="", help_text="", fields=["owner", "title", "place_description", "is_accesible", "populationId", "organization_name"])
	contact_fields = FieldStack(title="פרטי איש/ת הקשר", help_text="מי שיעמוד בקשר המקום מטעם צוות \"יום מעשים טובים\"", fields=["fname", "lname", "phone_1", "phone_2", "email", "position", "fax"])
	address_fields = FieldStack(title="כתובת המקום", help_text="", fields=["cityId", "street"])
	logistic_address_fields = FieldStack(title="כתובת המקום", help_text="", fields=["logistic_cityId", "logistic_street"])

class gddProjectFormProject(forms.Form):

	signature = forms.CharField(label = "חתימה",
		max_length=12,
		required=False,
		widget=forms.HiddenInput())
		
	number = forms.CharField(label = "מספר",
		max_length=12,
		required=False,
		widget=forms.HiddenInput())
	
	fieldId = forms.ChoiceField(label = _("תחום הפעילות"),
		choices=[('',_("סוג הפעילות אותה תרצו לקיים ביום מעשים טובים"))] + GDD_FIELDS, 
		help_text = _("שימו לב! באפשרותכם למלא כמה פריקטים בתחומים שונים. לאחר הזנת הפרטים הרלוונטיים לכל פרויקט, תינתן לכם האפשרות להזין פרויקט נוסף."),
		required=True) 
		
	description = forms.CharField(label = _("תיאור הפעילות"),
		widget=forms.Textarea(attrs = { 'placeholder': _("תיאור הפעילות שתתקיים במהלך \"יום מעשים טובים\"") }),
		required=True)
	
	volunteer_typeId = forms.ChoiceField(label = _("עבור אילו מתנדבים מיועדת הפעילות"),
		choices=[('',_('האם הפעילות מיועדת ליחידים או קבוצה מגובשת?'))] + GDD_TYPE, 
		required=True)
	
	from_time = forms.TimeField(label = _("שעת תחילת הפעילות"),
		widget=forms.Select(choices=HOURS),
		required=True)
	
	to_time = forms.TimeField(label = _("שעת סיום הפעילות"),
		widget=forms.Select(choices=HOURS),
		required=True)
	
	volunteer_num = forms.IntegerField(label = _("מספר המתנדבים הדרושים עבור הפעילות "),
		help_text=_("שימו לב נעשה כל שביכולתנו לגייס מתנדבים לפעילות, אולם איננו יכולים להבטיח כי ימצאו די מתנדבים לפעילותכם. במידה ולא יהיה ביקוש מספיק לפעילות תוכלו לנסות לגייס מתנדבים בכוחות עצמכם, אחרת לא תוכל הפעילות לצאת לפועל."),
		min_value=0,
		required=False)
	
	form_comment = forms.CharField(label = _("הערות"),
		required=False,
		widget=forms.Textarea())

#class gddProjectDefault(forms.Forms):
		
class gddProjectFormActivity(forms.Form):

	orginaizer = forms.ChoiceField(label = _("האם הפעילות מארוגנת על-ידי המתנדבים או המקום?"),
		choices=[('','בחרו')] + GDD_ORGINIZER, 
		required=True)
			
	people = forms.CharField(label = _("מספר המופעלים"),
		required=False)
		
	people_ages = forms.CharField(label = _("גילאי המופעלים"),
		required=False)
		
	population_description = forms.CharField(label = _("מאפיינים מיוחדים של המופעלים"),
		required=False,
		widget=forms.Textarea())

class gddProjectFormFood(forms.Form):

	parallal_volunteer_num = forms.IntegerField(label = _("מהו מספר המתנדבים המירבו שיוכלו להגיע בכל משמרת?"),
		min_value=0,
		required=True)
		
class gddProjectFormPaint(forms.Form):

	wall_area = forms.DecimalField(label = _("מהו סך שטח כל הקירות שתרצו לצבוע (במ\"ר)?"),
		help_text=_("שטח קיר = אורך הקיר כפול גבוהו"),
		min_value=0,
		required=False)
	
	wall_color = forms.MultipleChoiceField(label = _("במידה ותרצו לגוון את הצבע הלבן, אנא בחרו את המגוון הרצוי (ניתן לסמן כמה מגוונים)"),
		choices=GDD_WALL_COLOR, 
		required=False,
		widget=forms.CheckboxSelectMultiple())
		
	windows_num = forms.IntegerField(label = _("מהי כמות החלונות אותם תרצו לצבוע?"),
		min_value=0,
		required=False)
		
	windows_materialId = forms.ChoiceField(label = _("האם החלונות עשויים ממתכת או מעץ?"),
		choices=[('',_('בחרו'))] + GDD_MATERIAL, 
		required=False)
	
	windows_colourId = forms.ChoiceField(label = _("באיזה צבע תרצו לצבוע את החלונות"),
		choices=[('',_('בחרו'))] + GDD_WALL_COLOR, 
		required=False)
		
	doors_num = forms.IntegerField(label = _("מהי כמות הדלתות אותן תרצו לצבוע?"),
		min_value=0,
		required=False)
		
	doors_materialId = forms.ChoiceField(label = _("האם הדלתות עשוויות ממתכת או עץ?"),
		choices=[('',_('בחרו'))] + GDD_MATERIAL, 
		required=False)
	
	doors_colourId = forms.ChoiceField(label = _("באיזה צבע תרצו לצבוע את הדלתות?"),
		choices=[('',_('בחרו'))] + GDD_WALL_COLOR, 
		required=False)
	
	grate_length = forms.IntegerField(label = _("מהו שטח הסורגים אותם תרצו לצבוע?"),
		min_value=0,
		required=False)
	
	grate_colourId = forms.ChoiceField(label = _("באיזה צבע תרצו לצבוע?"),
		choices=[('',_('בחרו'))] + GDD_WALL_COLOR, 
		required=False)
		
	grate_rusted = forms.ChoiceField(label = _("האם יש על הסורגים חלודה?"),
		choices=GDD_YES_NO, 
		required=False, 
		widget=forms.RadioSelect())
		
	railing_length = forms.IntegerField(label = _("מהו סך אורך המעקות אותם תרצו לצבוע?"),
		min_value=0,
		required=False)
	
	railing_colourId = forms.ChoiceField(label = _("באיזה צבע תרצו לצבוע?"),
		choices=[('',_('בחרו'))] + GDD_WALL_COLOR, 
		required=False)
		
	railing_rusted = forms.ChoiceField(label = _("האם יש על המעקות חלודה?"),
		choices=GDD_YES_NO, 
		required=False,
		widget=forms.RadioSelect())
	
	wall_fields = FieldStack(title="", help_text="", fields=["wall_area", "wall_color"])
	windows_doors_fields = FieldStack(title="", help_text="", fields=["windows_num", "windows_materialId", "windows_colourId", "doors_num", "doors_materialId", "doors_colourId"])
	grate_fields = FieldStack(title="", help_text="", fields=["grate_length", "grate_colourId", "grate_rusted"])
	railing_fields = FieldStack(title="", help_text="", fields=["railing_length", "railing_colourId", "railing_rusted"])

class gddProjectFormWallPaint(forms.Form):

	wallpaint_height = forms.DecimalField(label = _("מהו אורך הקיר (במטר)?"),
		min_value=0,
		required=True)
		
	wallpaint_width = forms.DecimalField(label = _("מהו רוחב הקיר (במטר)?"),
		min_value=0,
		help_text=_("ערכה לציור קיר בשטח כ-12 מטר מרובע כוללת 5 אריזות צבע סופרקריל 1 ליטר בצבעים לבן, שחור, אדום, כחול וצהוב, סט מכחולים ו- 5 מברשות 2.5, דף הנחיות לערבוב גוונים וצבעים."),
		required=True)
		
class gddProjectFormGardening(forms.Form):
			
	gardening_type = forms.MultipleChoiceField(label = _("מה תרצו לשתול?"),
		choices=GDD_GARDENING_TYPE, 
		required=False,
		widget=forms.CheckboxSelectMultiple())
	
	#gardening_fence = forms.DecimalField(label = _("במידה ותרצו לשתול גדר חיה, מהו אורך הגדר לאורכה תרצו לשתול?"),
	#	min_value=0,
	#	required=False)
	
	gardening_area = forms.DecimalField(label = _("מהו שטח האזור בו תרצו לשתול?"),
		min_value=0,
		required=True)
		
	gardening_planters = forms.DecimalField(label = _("אם תרצו לשתול באדניות בלבד, כתבו את כמות האדניות הרצויה"),
		min_value=0,
		required=False)
	
	facility_material = forms.MultipleChoiceField(label = _("מאיזה חומר/חומרים עשויים המתקנים?"),
		choices=GDD_MATERIAL, 
		required=False,
		widget=forms.CheckboxSelectMultiple())
		
	facility_num = forms.IntegerField(label = _("מהו מספר המתקנים אותם תרצו לצבוע?"),
		min_value=1,
		required=False)
	
	facility_color = forms.MultipleChoiceField(label = _("באיזה צבע תרצו לצבוע? (ניתן לבחור יותר מאחד)"),
		choices=GDD_WALL_COLOR, 
		required=False,
		widget=forms.CheckboxSelectMultiple())

	fence_material = forms.ChoiceField(label = _("מאיזה חומר עשויה הגדר?"),
		choices=GDD_MATERIAL, 
		required=False)
		
	fence_length = forms.IntegerField(label = _("מהו אורך הגדר אותה תרצו לצבוע?"),
		min_value=0,
		required=False)
		
	fence_color = forms.ChoiceField(label = _("באיזה צבע תרצו לצבוע?"),
		choices=GDD_METAL_COLOR, 
		required=False)
	
	garden_fields = FieldStack(title="", help_text="", fields=["gardening_type", "gardening_area"])
	facility_fields = FieldStack(title="", help_text="", fields=["facility_material", "facility_num", "facility_color"])
	fence_fields = FieldStack(title="", help_text="", fields=["fence_length", "fence_color", "fence_material"])
	planters_fields = FieldStack(title="", help_text="", fields=["gardening_planters"])

class gddProjectFormCity(forms.Form):
	
	fieldId = forms.ChoiceField(label = _("תחום הפעילות"),
		choices=[('','בחרו')] + GDD_FIELDS, 
		required=True) 
		
	title = forms.CharField(label = _("שם פרויקט"),
		required=True)
		
	description = forms.CharField(label = _("תיאור הפעילות"),
		required=True,
		widget=forms.Textarea())
		
	volunteer_num = forms.IntegerField(label = _("מהו מספר המתנדבים שיגוייסו על-ידי היישוב?"),
		min_value=0,
		required=True)
		
	volunteer_num = forms.IntegerField(label = _("במידה ויש צורך במתנדבים נוספים (שיגוייסו ע\"י \"רוח טובה\"), מהו מספרם?"),
		min_value=0,
		required=True)

	from_time = forms.TimeField(label = _("שעת תחילת הפעילות"),
		widget=SelectTimeWidget(),
		required=True)
	
	to_time = forms.TimeField(label = _("שעת סיום הפעילות"),
		widget=SelectTimeWidget(),
		required=True)
		
	description = forms.CharField(label = _("הערות"),
		required=False,
		widget=forms.Textarea())
	
class ProjectFormWizard(FormWizard):  
	def done(self, request, form_list):
		signature = str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)
		id_name = "f:/web/forms/" + signature
		#os.mkdir(id_name)
		#for form in form_list:
		#	if type(form) == gddProjectFormPlace:
		#		if form.cleaned_data['owner'] == "tel-aviv":
		#			form.cleaned_data['owner'] = "KAR\\morb"
		#		pass
		#		codecs.open(id_name +"/place.xml", "w", "utf-8").write(render_to_string('object-output.xml', {'form': form, 'object': 'place', }))
		#	elif  type(form) == gddProjectFormProject:
		#		pass
		#		codecs.open(id_name +"/project-0.xml", "w", "utf-8").write(render_to_string('object-output.xml', {'form': form,  'object': 'project', }))
		#	else:
		#		pass
		#		codecs.open(id_name +"/logistics-0.xml", "w", "utf-8").write(render_to_string('object-output.xml', {'form': form, 'object': 'logistic_data', }))
		
		return HttpResponseRedirect("/gdd-project-final/" + signature + "/1")
		
  
	def process_step(self, request, form, step):
		if step == 1:
			#if len(self.form_list) % 2 == 1:
				#self.form_list.pop(len(self.form_list) - 1)
			if form.data['1-fieldId'] == u'1':				
				self.form_list.append(gddProjectFormFood)
			if form.data['1-fieldId'] == u'3':				
				self.form_list.append(gddProjectFormActivity)
			if form.data['1-fieldId'] == u'5':				
				self.form_list.append(gddProjectFormPaint)
				self.form_list.append(gddProjectFormCalculate)
			if form.data['1-fieldId'] == u'7':				
				self.form_list.append(gddProjectFormGardening)
				self.form_list.append(gddProjectFormCalculate)
			if form.data['1-fieldId'] == u'8':				
				self.form_list.append(gddProjectFormWallPaint)
				self.form_list.append(gddProjectFormCalculate)
	
	def get_template(self, step): 
		return 'gdd-project-form/step-%s.html' % self.form_list[step].__name__.lower().replace("gddprojectform", "")
		
 
class AddProjectFormWizard(FormWizard):  
	def done(self, request, form_list):
		signature = form_list[0].cleaned_data["signature"]
		number = int(form_list[0].cleaned_data["number"])
		id_name = "f:/web/forms/" + signature 
		for form in form_list:
			if  type(form) == gddProjectFormProject:
				codecs.open(id_name +"/project" + "-" + str(number) + ".xml", "w", "utf-8").write(render_to_string('object-output.xml', {'form': form,  'object': 'project', }))
			else:
				codecs.open(id_name +"/logistics" + "-" + str(number) + ".xml", "w", "utf-8").write(render_to_string('object-output.xml', {'form': form, 'object': 'logistic_data', }))
		
		return HttpResponseRedirect("/gdd-project-final/" + signature + "/" + str(number + 1))
		
	def process_step(self, request, form, step):
		if step == 0:
			if len(self.form_list) % 2 == 0:
				self.form_list.pop(len(self.form_list) - 1)
			if form.data['0-fieldId'] == u'1':				
				self.form_list.append(gddProjectFormFood)
			if form.data['0-fieldId'] == u'3':				
				self.form_list.append(gddProjectFormActivity)
			if form.data['0-fieldId'] == u'5':				
				self.form_list.append(gddProjectFormPaint)
			if form.data['0-fieldId'] == u'7':				
				self.form_list.append(gddProjectFormGardening)
			if form.data['0-fieldId'] == u'8':				
				self.form_list.append(gddProjectFormWallPaint)
	
	def get_template(self, step):
		return 'gdd-project-form/step-%s.html' % self.form_list[step].__name__.lower().replace("gddprojectform", "")

		
class CityFormWizard(FormWizard):  
	def done(self, request, form_list):
		id_name = str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)
		for form in form_list:
			if type(form) == gddProjectFormCity:
				codecs.open("f:/web/forms/P-CT" + id_name +".xml", "w", "utf-8").write(render_to_string('form-output.xml', {'form': form, }))
			else:
				codecs.open("f:/web/forms/P-DT" + id_name +".xml", "w", "utf-8").write(render_to_string('form-output.xml', {'form': form, }))
		
		return HttpResponseRedirect('/city-index/') 
  
	def process_step(self, request, form, step):
		if step == 0:
			if len(self.form_list) % 2 == 0:
				self.form_list.pop(len(self.form_list) - 1)
			if form.data['0-field'] == u'3':				
				self.form_list.append(gddProjectFormActivity)
			if form.data['0-field'] == u'5':				
				self.form_list.append(gddProjectFormPaint)
			if form.data['0-field'] == u'7':				
				self.form_list.append(gddProjectFormGardening)
			if form.data['0-field'] == u'8':				
				self.form_list.append(gddProjectFormWallPaint)
	
	def get_template(self, step):
		return 'gdd-project-form/step-%s.html' % self.form_list[step].__name__.lower().replace("gddprojectform", "")