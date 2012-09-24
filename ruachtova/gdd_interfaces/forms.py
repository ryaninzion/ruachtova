# coding=utf-8

from django.forms import *
from gdd_interfaces.models import *
from django.contrib.formtools.wizard import FormWizard
from django.forms.forms import BoundField
from django.http import HttpResponse, HttpRequest

from django.http import HttpResponse

from django.shortcuts import render_to_response

from datetime import *
import codecs
from form_utils import forms  

LOGISTIC_TYPES = [(dbtype.pk, dbtype.title) for dbtype in gddLogisticType.objects.all()]
MATERIAL_TYPES = [(dbtype.pk, dbtype.title) for dbtype in gddMaterial.objects.all()]
COLOUR_TYPES = [(dbtype.pk, dbtype.title) for dbtype in gddColour.objects.all()]
GARDENING_TYPES = [(dbtype.pk, dbtype.title) for dbtype in gddGardening.objects.all()]
FIELD_TYPES = [(dbtype.pk, dbtype.title) for dbtype in gddField.objects.all()]

YES_NO_TYPES = [
	(False, 'לא'),
	(True, 'כן'),
]

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


class CityForm(forms.BetterModelForm):  
	
	class Meta:  
		model = gddCity
		
		fieldsets = [('contact-details',
					{'legend': 'פרטי איש/ת קשר לתיאום הורדת הציוד', 
					'fields': 
						['contact_fname', 'contact_lname', 'contact_phone_1', 'contact_phone_2', ],  
					#'description': 'Information',  
				}),
				('logistic-address',
					{'legend': 'כתובת הורדת ציוד',
					'fields':
						['logistic_address', ]
				}),]
 
def CityProjectForm(request, *args, **kwargs):

	is_logistic_address = None
	is_volunteer_external = None
	is_logistic_contact = None
	try:
		is_logistic_address = bool(kwargs.pop('is_logistic_address'))
	except:
		is_logistic_address = False

	try:
		is_logistic_contact = bool(kwargs.pop('is_logistic_contact'))
	except:
		is_logistic_contact = False
		
	try:
		is_volunteer_external = bool(kwargs.pop('is_volunteer_external'))
	except:
		is_volunteer_external = False
	
	field_list = []
					
	if is_volunteer_external == True:
		field_list.append(('project-details',
									{'legend': 'פרטי הפרויקט', 
									'fields': 
										['city', 'title', 'field', 'logistic_type', 'description', 'volunteer_num', 'is_volunteer_external', ],  
									#'description': 'Information',  
								}))
		field_list.append(('external_volunteers',
									{'legend': 'גיוס מתנדבים על-ידי רוח טובה',
									'fields':
										['volunteer_num_external', 'from_time', 'to_time']
								}))
	else:
		field_list.append(('project-details',
									{'legend': 'פרטי הפרויקט', 
									'fields': 
										['city', 'title', 'field', 'logistic_type', 'description', 'volunteer_num_external', 'from_time', 'to_time' ],  
									#'description': 'Information',  
								}))
	
	field_list.append(('contact-details',
						{'legend': 'פרטי איש/ת הקשר', 
						'fields': 
							['fname', 'lname', 'phone_1', 'email', 'position'],  
						#'description': 'Information',  
					}))
					
	if is_logistic_address == True:
		field_list.append(('address-fields',
						{'legend': 'כתובת הורדת ציוד', 
						'fields': 
							['city_title', 'street', ],
						#'description': 'Information',  
					}))
					
	if is_logistic_address == True:
		field_list.append(('logistic-contact-fields',
						{'legend': 'פרטי איש/ת קשר לענייני לוגיסטיקה', 
						'fields': 
							['logistic_fname', 'logistic_lname', 'logistic_phone_1'],
						#'description': 'Information',  
					}))
	if request.META["REMOTE_ADDR"] != "192.192.192.2" :
		field_list.append(('additional-fields',
							{'legend': 'הערות ופרטים נוספים', 
							'fields': 
								['is_stamped', 'comments'],
						}))
	else:
		field_list.append(('additional-fields',
							{'legend': 'הערות ופרטים נוספים', 
							'fields': 
								['comments'],
						}))
	
	class Form(forms.BetterModelForm):  
		
		#field = ModelChoiceField(label = "תחום הפעילות",
		#	choices=[('', 'בחרו')] + FIELD_TYPES)
		
		logistic_type = MultipleChoiceField(label="מה ייעשה בפרויקט?",
			choices=LOGISTIC_TYPES,
			widget=CheckboxSelectMultiple,
			required=False)
			
		from_time = TimeField(label = "שעת תחילת הפעילות",
			widget=Select(choices=HOURS),
			required=False)
		
		to_time = TimeField(label = "שעת סיום הפעילות",
			widget=Select(choices=HOURS),
			required=False)
		
		description = CharField(label="תיאור הפעילות",
			initial="תיאור הפעילות שתקיימו ביום מעשים טובים",
			max_length=400,
			widget=Textarea(),
			required=True)
		
		is_volunteer_external = TypedChoiceField(label="האם יש צורך בגיוס מתנדבים על-ידי רוח טובה",
			choices=((True, 'כן'), (False, 'לא') ),
			initial=0,
			required=False,
			widget=RadioSelect)

		field = ModelChoiceField(queryset = gddField.objects.order_by('pk'),
			label="תחום הפעילות")
			
		class Meta:  
			model = gddCityProject  
			
			fieldsets = field_list
			widgets = {
				'city': HiddenInput,
			}
			
	return Form(*args, **kwargs)

def get_form(*args, **kwargs):

	try:
		fieldset_list = kwargs.pop('type_list')
	except:
		fieldset_list = []
		
	view_fieldsets = []
	
	view_fieldsets.append(('', 
					{'fields': 
						['parent', ],  
				}),)

	if "gddGardening" in fieldset_list:
		view_fieldsets.append(('הקמת גינה', 
					{'fields': 
						['gardening_type', 'gardening_area', 'gardening_fence', 'gardening_planters', ],  
				}),)
				
	if "gddGardeningFacility" in fieldset_list:
		view_fieldsets.append(('צביעת מתקנים בחצר', 
					{'fields': 
						['facility_material', 'facility_num', 'facility_colour', ],  
				}),)
	
	if "gddGardeningFence" in fieldset_list:
		view_fieldsets.append(('צביעת גדרות', 
					{'fields': 
						['fence_material', 'fence_length', 'fence_colour', ],  
				}),)
	
	if "gddWallPaint" in fieldset_list:
		view_fieldsets.append(('ציורי קיר', 
					{'fields': 
						['wallpaint_height', 'wallpaint_width', ],  
				}),)
	
	if "gddPaintWall" in fieldset_list:
		view_fieldsets.append(('צביעת קירות וחללים', 
					{'fields': 
						['wall_type', 'wall_area', 'wall_colour', ],  
				}),)
				
	if "gddPaintWindows" in fieldset_list:
		view_fieldsets.append(('צביעת חלונות', 
					{'fields': 
						['windows_num', 'windows_material', 'windows_colour', ],  
				}),)
				
	if "gddPaintDoors" in fieldset_list:
		view_fieldsets.append(('צביעת דלתות', 
					{'fields': 
						['doors_num', 'doors_material', 'doors_colour', ],  
				}),)
				
	if "gddPaintGrate" in fieldset_list:
		view_fieldsets.append(('צביעת סורגים', 
					{'fields': 
						['grate_length', 'grate_colour', 'grate_rusted', ],  
				}),)
				
	if "gddPaintRailing" in fieldset_list:
		view_fieldsets.append(('צביעת מעקות', 
					{'fields': 
						['railing_length', 'railing_colour', 'railing_rusted', ],  
				}),)
				
	
	if "gddApartments" in fieldset_list:
		view_fieldsets.append(('צביעת דירות רווחה', 
					{'fields': 
						['apartments_num', 'apartments_area', ],  
				}),)
				
	if len(fieldset_list) == 0:
		return None
	
	class TotalForm(forms.BetterModelForm):  	
	
		wall_colour = MultipleChoiceField(label="באילו צבעים תרצו לצבוע את הקיר?",
			choices=COLOUR_TYPES,
			widget=CheckboxSelectMultiple,
			required=False)
		gardening_type = MultipleChoiceField(label="מה תרצו לשתול?",
			choices=GARDENING_TYPES,
			widget=CheckboxSelectMultiple,
			required=False)
		facility_material = MultipleChoiceField(label="האם המתקנים הם מעץ או ממתכת?",
			choices=MATERIAL_TYPES,
			widget=CheckboxSelectMultiple,
			required=False)
		
		
		class Meta:  
			model = gddCityLogistics  
			fieldsets = view_fieldsets
			
			widgets = {
				'parent': HiddenInput,
				'facility_colour': CheckboxSelectMultiple,
			}
	
	#def __init__(self):
		#super(TotalForm, self).__init__(*args, **kwargs)
	
	return TotalForm(*args, **kwargs)

class gddChangeRegisterForm(forms.BetterModelForm):
	
	class Meta:
		model = DesignForChange
		
		fieldsets = [('group-details',
						{'legend': 'פרטי הקבוצה', 
						'fields': 
							['guid', 'name', 'group_name', 'age', 'volunteer_num' ],  
						#'description': 'Information',  
					}),
					('address-details',
						{'legend': 'כתובת', 
						'fields': 
							['city', 'street', 'zip_code' ],  
						#'description': 'Information',  
					}),
					('contact-details',
						{'legend': 'פרטי איש/ת הקשר',
						'fields':
							['fname', 'lname', 'phone_1', 'phone_2', 'email', 'url' ]
					}),]
					
		widgets = {
			'guid': HiddenInput,
		}


class gddChangeProblemForm(forms.BetterModelForm):
	
	class Meta:
		model = DesignForChange
		
		fieldsets = [('problem',
						{'legend': 'תיאור הבעיה אותה תרצו לפתור',
						'fields':
							['guid', 'problem_name', 'problem_description' ]
					}),]
		
		widgets = {
			'guid': HiddenInput,
		}
 
class gddChangeProjectForm(forms.BetterModelForm):
	
	media_file = FileField(label = "צרפו את הפרויקט המתועד (מצגת, סרטון, תמונות)",
		required=False)
	
	class Meta:
		model = DesignForChange
		
		fieldsets = [('project',
						{'legend': 'טופס הפרויקט – שתפו את הסיפור שלכם אתנו',
						'fields':
							['guid', 'project_name', 'project_description', 'media_file' ]
					}),
					('group-details',
						{'legend': 'במידה ותרצו לעדכן את פרטיכם האישיים, תוכלו לעשות זאת להלן:', 
						'fields': 
							['guid', 'name', 'group_name', 'age', 'volunteer_num', 'city', 'street', 'fname', 'lname', 'phone_1', 'phone_2', 'email', 'url'],  
					}),]
		
		widgets = {
			'guid': HiddenInput,
		}

class CityGroupForm(forms.BetterModelForm):
	
	class Meta:
		model = gddCityGroup
		
		fieldsets = [('group-details',
						{'legend': 'פרטי הקבוצה', 
						'fields': 
							['city', 'group_name', 'volunteer_num', 'group_ages', 'description', 'cityId', ],  
						#'description': 'Information',  
					}),
					('contact-details',
						{'legend': 'פרטי איש/ת הקשר',
						'fields':
							['fname', 'lname', 'genderId', 'phone_1', 'phone_2', 'email' ]
					}),
					('comments',
						{'legend': 'הערות ופרטים נוספים',
						'fields':
							['comments', ]
					}),]
					
		widgets = {
			'city': HiddenInput,
		}