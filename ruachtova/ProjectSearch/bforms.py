# coding=utf-8

import os
from django.forms import *
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

from form_utils import forms

GDD_GENDERS = (
	(1, 'זכר'),
	(2, 'נקבה'),
)

GDD_FIELDS = [
	(6, 'איכות הסביבה ובעלי חיים'),
	#(1, 'אריזה והגשת מזון'),
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

GDD_YES_NO = [
	(1, 'כן'),
	(2, 'לא'),
]

ARABIC_GDD_GENDERS = (
	(1, 'ذكر'),
	(2, 'أنثى'),
)

ARABIC_GDD_FIELDS = [
	(6, 'جودة البيئة والحيوانات'),
	(1, 'تغليف وتقديم الغذاء'),
	(3, 'تفعيل وإرشاد'),	
	(7, 'إنشاء\تجديد حدائق'),	
	(2, ' نقل ومرافقة السفريات'),
	(5, ' تجديد ودهان'),
	(4, 'ترتيب وتنظيم'),
	(8, 'رسم على الجدران'),
	(9, 'آخر'),
]

ARABIC_GDD_POPULATIONS = [
	(1, 'أولاد وشباب'),
	(2, 'مسنين'),
	(3, 'مجموعات خاصة'),
	(4, 'آخر'),
]

ARABIC_GDD_TIME = [
	(1, 'الصباح'),
	(2, 'الظهر'),
	(3, 'المساء'),
]


ARABIC_GDD_YES_NO = [
	(1, 'نعم'),
	(2, 'لا'),
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

GDD_WALL_COLOR = (
	(1, 'אדום'),
	(2, 'כחול'),
	(4, 'צהוב'),
)

GDD_PAINT_COLOR = (
	(1, 'אדום'),
	(2, 'כחול'),
	(3, 'צהוב'),
	(4, 'שחור'),
	(5, 'לבן'),
)

GDD_METAL_COLOR = (
	(1, 'אדום'),
	(2, 'כחול'),
	(3, 'ירוק'),
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
	(1, 'עץ'),
	(2, 'מתכת'),
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

class gddVGroupForm(forms.BetterForm):
	 
	owner = CharField(label='',
		widget = HiddenInput(),
		required=False)
		
	group_name = CharField(label = "שם קבוצה",
		required=True)
	volunteer_num = IntegerField(label = "מספר המתנדבים בקבוצה",
		min_value=0,
		required=True)
	group_ages = CharField(label = "גילאי הקבוצה",
		required=False)
	description = CharField(label = "תיאור הקבוצה",
		required=False,
		widget=Textarea())
	cityId = ChoiceField(label = _("יישוב"),
		choices = [('',_('בחרו'))] + GDD_CITIES,
		required=True)
		 
	fname = CharField(label = "שם פרטי",
		required=True)
	lname = CharField(label = "שם משפחה",
		required=True)
	 
	phone_1 = CharField(label = "טלפון",
		required=True)
	phone_2 = CharField(label = "טלפון נוסף",
		required=False)
	email = CharField(label = "כתובת דוא\"ל",
		required=False)
	genderId = ChoiceField(label="מין",
		choices=GDD_GENDERS,
		widget=RadioSelect(),
		required=False)
	
	field = MultipleChoiceField(label = "תחום הפעילות",
		choices=GDD_FIELDS, 
		required=False,
		widget=CheckboxSelectMultiple())
	population = MultipleChoiceField(label = "אוכלוסייה",
		choices=GDD_POPULATIONS, 
		required=False,
		widget=CheckboxSelectMultiple())
	time = MultipleChoiceField(label = "שעות ההתנדבות",
		choices=GDD_TIME, 
		required=False,
		widget=CheckboxSelectMultiple())
		
	comments = CharField(label = "הערות",
		required=False,
		widget=Textarea())
		
	class Meta:
		fieldsets = [('group-details',
						{'legend': 'פרטי הקבוצה', 
						'fields': 
							['owner', 'group_name', 'volunteer_num', 'group_ages', 'description', 'cityId', ],  
						#'description': 'Information',  
					}),
					('contact-details',
						{'legend': 'פרטי איש/ת הקשר',
						'fields':
							['fname', 'lname', 'genderId', 'phone_1', 'phone_2', 'email' ]
					}),
					('volunteering-details',
						{'legend': 'פרטי ההתנדבות המבוקשת',
						'fields':
							['field', 'population', 'time', ]
					}),
					('comments',
						{'legend': 'הערות ופרטים נוספים',
						'fields':
							['comments', ]
					}),]

					
class gddVolunteerForm(forms.BetterForm):
	
	fname = CharField(label = "שם פרטי",
		required=True)
	lname = CharField(label = "שם משפחה",
		required=True)		
	genderId = ChoiceField(label="מין",
		choices=GDD_GENDERS,
		widget=RadioSelect(),
		required=False)		
	group_ages = CharField(label = "גיל",
		required=False)
	proffession = CharField(label = "מקצוע",
		required=False)
		
	cityId = ChoiceField(label = _("יישוב"),
		choices = [('',_('בחרו'))] + GDD_CITIES,
		required=True)		 
	 
	phone_1 = CharField(label = "טלפון",
		required=True)
	phone_2 = CharField(label = "טלפון נוסף",
		required=False)
	email = CharField(label = "כתובת דוא\"ל",
		required=False)
	
	field = MultipleChoiceField(label = "תחום הפעילות",
		choices=GDD_FIELDS, 
		required=False,
		widget=CheckboxSelectMultiple())
	population = MultipleChoiceField(label = "אוכלוסייה",
		choices=GDD_POPULATIONS, 
		required=False,
		widget=CheckboxSelectMultiple())
	time = MultipleChoiceField(label = "שעות ההתנדבות",
		choices=GDD_TIME, 
		required=False,
		widget=CheckboxSelectMultiple())
	
	long_term = ChoiceField(label="האם תהיו מעוניינים בהתנדבות ארוכת טווח?",
		choices=GDD_YES_NO,
		required=False,
		widget=RadioSelect())	
		
	comments = CharField(label = "הערות",
		required=False,
		widget=Textarea())
		
	class Meta:
		fieldsets = [('group-details',
						{'legend': 'פרטים אישיים', 
						'fields': 
							['fname', 'lname', 'genderId', 'group_ages', 'proffession' ],
						}),
						('contact-details',
							{'legend': 'פרטי יצירת קשר',
							'fields':
								['cityId', 'phone_1', 'phone_2', 'email' ]
						}),
						('volunteering-details',
							{'legend': 'פרטי ההתנדבות המבוקשת',
							'fields':
								['field', 'population', 'time', 'long_term', ]
						}),
						('comments',
							{'legend': 'הערות ופרטים נוספים',
							'fields':
								['comments', ]
						}),]
						
class gddArabicGroupForm(forms.BetterForm):
	
	group_name = CharField(label = "اسم المجموعة ",
		required=True)
	volunteer_num = IntegerField(label = "عدد المتطوعين بالمجموعه",
		min_value=0,
		required=True) 
	group_ages = CharField(label = "أجيال المجموعة",
		required=False)
	description = CharField(label = "وصف المجموعة",
		required=False,
		widget=Textarea())
	cityId = ChoiceField(label = _("البلد"),
		choices = [('',_('בחרו'))] + GDD_CITIES,
		required=True)
		 
	fname = CharField(label = "الاسم",
		required=True)
	lname = CharField(label = "العائلة",
		required=True)
	 
	phone_1 = CharField(label = "هاتف",
		required=True)
	phone_2 = CharField(label = "هاتف إضافي",
		required=False)
	email = CharField(label = "بريد الكتروني",
		required=False)
	genderId = ChoiceField(label="الجنس",
		choices=ARABIC_GDD_GENDERS,
		widget=RadioSelect(),
		required=False)
	
	field = MultipleChoiceField(label = "مجال التطوع",
		choices=ARABIC_GDD_FIELDS, 
		required=False,
		widget=CheckboxSelectMultiple())
	population = MultipleChoiceField(label = "الجمهور",
		choices=ARABIC_GDD_POPULATIONS, 
		required=False,
		widget=CheckboxSelectMultiple())
	time = MultipleChoiceField(label = "ساعات التطوع المفضلة",
		choices=ARABIC_GDD_TIME, 
		required=False,
		widget=CheckboxSelectMultiple())
		
	comments = CharField(label = "ملاحظات",
		required=False,
		widget=Textarea())
		
	class Meta:
		fieldsets = [('group-details',
						{'legend': 'تفاصيل شخصية', 
						'fields': 
							['group_name', 'volunteer_num', 'group_ages', 'description', 'cityId', ],  
						#'description': 'Information',  
					}),
					('contact-details',
						{'legend': 'تفاصيل رجل الاتصال',
						'fields':
							['fname', 'lname', 'genderId', 'phone_1', 'phone_2', 'email' ]
					}),
					('volunteering-details',
						{'legend': 'تفاصيل التطوع المطلوبة',
						'fields':
							['field', 'population', 'time', ]
					}),
					('comments',
						{'legend': 'ملاحظات ومعلومات اضافية',
						'fields':
							['comments', ]
					}),]

					
class gddArabicVolunteerForm(forms.BetterForm):
	
	fname = CharField(label = "الاسم",
		required=True)
	lname = CharField(label = "العائلة",
		required=True)		
	genderId = ChoiceField(label="الجنس",
		choices=ARABIC_GDD_GENDERS,
		widget=RadioSelect(),
		required=False)		
	group_ages = CharField(label = "الجيل",
		required=False)
	proffession = CharField(label = "المهنة",
		required=False)
		
	cityId = ChoiceField(label = _("بلد التطوع"),
		choices = [('',_('בחרו'))] + GDD_CITIES,
		required=True)		 
	 
	phone_1 = CharField(label = "هاتف",
		required=True)
	phone_2 = CharField(label = "هاتف إضافي",
		required=False)
	email = CharField(label = "بريد الكتروني",
		required=False)
	
	field = MultipleChoiceField(label = "مجال التطوع",
		choices=ARABIC_GDD_FIELDS, 
		required=False,
		widget=CheckboxSelectMultiple())
	population = MultipleChoiceField(label = "الجمهور",
		choices=ARABIC_GDD_POPULATIONS, 
		required=False,
		widget=CheckboxSelectMultiple())
	time = MultipleChoiceField(label = "ساعات التطوع المفضلة",
		choices=ARABIC_GDD_TIME, 
		required=False,
		widget=CheckboxSelectMultiple())
	
	long_term = ChoiceField(label="هل ترغب/ي بالتطوع على مدار السنه ?",
		choices=ARABIC_GDD_YES_NO,
		required=False,
		widget=RadioSelect())	
		
	comments = CharField(label = "ملاحظات",
		required=False,
		widget=Textarea())
		
	class Meta:
		fieldsets = [('group-details',
						{'legend': 'تفاصيل شخصية', 
						'fields': 
							['fname', 'lname', 'genderId', 'group_ages', 'proffession' ],
						}),
						('contact-details',
							{'legend': 'معلومات الاتصال',
							'fields':
								['cityId', 'phone_1', 'phone_2', 'email' ]
						}),
						('volunteering-details',
							{'legend': 'تفاصيل التطوع المطلوبة',
							'fields':
								['field', 'population', 'time', 'long_term', ]
						}),
						('comments',
							{'legend': 'ملاحظات ومعلومات اضافية',
							'fields':
								['comments', ]
						}),]

