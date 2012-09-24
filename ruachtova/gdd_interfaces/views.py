# coding=utf-8

from django import forms
from gdd_interfaces.models import *
from gdd_interfaces.forms import *
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.shortcuts import *

from django.forms.models import model_to_dict

import codecs
import urllib
import uuid
import os

from datetime import *

# City page, with list of city ptoject
def gdd_change_register_form(request):

	form = gddChangeRegisterForm()
	 
	if request.method == 'POST': # If the form has been submitted...
		form = gddChangeRegisterForm(request.POST)
		if form.is_valid():
			#codecs.open("f:/web/forms/V" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + theme + ".xml", "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			item = form.save()
			return render_to_response('gdd-change-mid-form.html', { 'guid': item.guid } )

	else:
		form = gddChangeRegisterForm(initial = { 'guid': uuid.uuid1() })
	 
	return render_to_response('gdd-change-form.html', { 'form': form, 'title': 'הרשמה להתנדבות' } )

def gdd_change_problem_form(request, guid):
 
	form = gddChangeProblemForm()
	 
	problem = DesignForChange.objects.get(guid = guid)
	 
	if request.method == 'POST': # If the form has been submitted...
		form = gddChangeProblemForm(request.POST, instance = problem)
		if form.is_valid():
			#codecs.open("f:/web/forms/V" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + theme + ".xml", "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			form.save()
			return render_to_response('gdd-change-end-form.html')
	else:
		form = gddChangeProblemForm(initial = { 'guid': guid } )
	 
	return render_to_response('gdd-change-form.html', { 'form': form, 'title': 'הרשמה להתנדבות' } )

def gdd_change_project_form(request, guid):
 
	form = gddChangeProjectForm()
	 
	problem = DesignForChange.objects.get(guid = guid)
	 
	if request.method == 'POST': # If the form has been submitted... 
		form = gddChangeProjectForm(request.POST, request.FILES, instance = problem)
		if form.is_valid():
			#codecs.open("f:/web/forms/V" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + theme + ".xml", "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			form.save()
			
			for file in request.FILES.getlist('media_file'):
				filename = file.name
				ext = os.path.splitext(filename)[1]
				ext = ext.lower()
				
				media_file = DesignForChangeFiles.objects.create(media_file = file, media_type = ext, parent = problem)
				media_file.save()
			
			return render_to_response('gdd-change-project-end-form.html')
	else:
		form = gddChangeProjectForm(initial = { 'guid': guid }, instance = problem )
			
	return render_to_response('gdd-change-form.html', { 'form': form, 'title': 'הרשמה להתנדבות' } )


def gdd_city(request, key):
	
	projects = gddCityProject.objects.filter(city__guid = key).order_by('id') 
	data_missing = gddCityProject.objects.filter(city__guid = key, is_data_missing = True)
	city = gddCity.objects.get(guid=key)
	form = CityForm(instance=city)
	
	# Check if a form has been submitted
	if request.POST:
		
		form = CityForm(request.POST, instance=city)
		 
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/gdd-city/" + str(key))
	
	if city.is_open:
		return render_to_response('city-index.html', { 'projects': projects, 'city': city, 'form': form, 'data_missing': data_missing, })
	else:
		return render_to_response('city-index-closed.html', { 'projects': projects, 'city': city, 'form': form, 'data_missing': data_missing, })
def gdd_city_groups(request, key):
	
	groups = gddCityGroup.objects.filter(city__guid = key).order_by('group_name') 
	city = gddCity.objects.get(guid=key)

	return render_to_response('city-group-index.html', { 'groups': groups, 'city': city })

# The city project's form

def gdd_city_project_form(request, guid, pid, is_duplicate = False, is_fixed = False):
	
	city = gddCity.objects.get(guid=guid)
	# Check if a form has been submitted
	is_logistic_address = city.is_logistic_address
	is_volunteer_external = city.is_volunteer_external
		
	if request.POST:
		if int(pid) == 0 or is_duplicate:
			form = CityProjectForm(request, request.POST, is_logistic_address=is_logistic_address, is_volunteer_external=is_volunteer_external)
		else:
			project = gddCityProject.objects.get(pk=pid)
			form = CityProjectForm(request, request.POST, instance=project, is_logistic_address=is_logistic_address, is_volunteer_external=is_volunteer_external)
		
		if form.is_valid():
			newform = form.save()
			pid = newform.pk 
			if is_fixed == True:
				return HttpResponseRedirect("/gdd-city-logistics-f/" + str(guid) + "/" + str(pid))
			if is_duplicate:
				return HttpResponseRedirect("/gdd-city-logistics-d/" + str(guid) + "/" + str(pid))
			else:
				return HttpResponseRedirect("/gdd-city-logistics/" + str(guid) + "/" + str(pid))
	
	# If a form has not been submitted, check if a new form should be created
	elif int(pid) == 0:
		form = CityProjectForm(request, initial={'city': guid}, is_logistic_address=is_logistic_address, is_volunteer_external=is_volunteer_external)
		
	# If not, an existing model is being edited 
	else:
		p = int(pid)
		project = gddCityProject.objects.get(pk = p)
		dictionary = model_to_dict(project)
		form = CityProjectForm(request, instance=project, is_logistic_address=is_logistic_address, is_volunteer_external=is_volunteer_external)
		
	return render_to_response('gdd-city-form.html', { 'form': form, 'guid': guid })

def gdd_city_group_form(request, guid, gid, isis_fixed = False):
	
	city = gddCity.objects.get(guid=guid)
		
	if request.POST:
		if int(gid) == 0:
			form = CityGroupForm(request.POST)
		else:
			group = gddCityGroup.objects.get(pk=gid)
			form = CityGroupForm(request.POST, instance=group)
		
		if form.is_valid():
			newform = form.save()
			pid = newform.pk  
			return render_to_response('gdd-city-group-end.html', { 'guid': guid })
			#return HttpResponseRedirect("/gdd-city-g/" + str(guid) + "/" + str(pid))
	
	# If a form has not been submitted, check if a new form should be created
	elif int(gid) == 0:
		form = CityGroupForm(initial={'city': guid})
		
	# If not, an existing model is being edited
	else:
		g = int(gid)
		group = gddCityGroup.objects.get(pk = g)
		dictionary = model_to_dict(group)
		form = CityGroupForm(request, instance=group)
		
	return render_to_response('gdd-city-form.html', { 'form': form, 'guid': guid })

# Logistics form, dynamically built according to the city project form

def gdd_city_logistics_form(request, guid, pid, is_duplicate = False, is_fixed = False):

	lid = 0
	logistics = None
	try:
		logistics = gddCityLogistics.objects.get(parent__pk = pid)
		lid = logistics.pk
	except gddCityLogistics.DoesNotExist:
		lid = 0
	
	project = gddCityProject.objects.get(pk = pid)
	if project.field.id == 8:
		logistic_types = ['gddWallPaint']
	elif project.field.id == 5:
		logistic_types = project.logistic_type.all().values_list('name', flat=True)
	else:
		logistic_types = []
	#for item in project.
	
	# Check if a form has been submitted
	if request.POST:
		if logistics == None or is_duplicate:
			form = get_form(request.POST, type_list=logistic_types)
		else:
			#logistics = gddLogistics.objects.get(pk=lid)
			form = get_form(request.POST, type_list=logistic_types, instance=logistics)

		if form.is_valid():
			data_missing = False
			for key, value in request.POST.iteritems():
				if value == '':
					data_missing = True
					
			form.save()
			
			project.is_data_missing = data_missing
			project.save()
			
			if is_fixed == True:
				return render_to_response('gdd-city-form-end-fixed.html', { 'form': form, 'lid': lid, 'guid': guid })
			else:
				return HttpResponseRedirect("/gdd-city-form-end/" + guid)
	
	# If a form has not been submitted, check if a new form should be created
	elif int(lid) == 0:
		form = get_form(type_list=logistic_types, initial={'parent': pid})
		if form == None:
			return HttpResponseRedirect("/gdd-city-form-end/" + guid)
		
	# If not, an existing model is being edited
	else:
		logistics_data = gddCityLogistics.objects.get(pk=lid)
		
		if logistics_data.parent.city.guid != guid:
			return HttpResponseRedirect("/gdd-error")
			
		form = get_form(type_list=logistic_types, instance=logistics_data)
		if form == None:
			return HttpResponseRedirect("/gdd-city-form-end/" + guid)
	
	return render_to_response('gdd-city-form.html', { 'form': form, 'lid': lid, 'guid': guid })

def gdd_city_project_delete_verify(request, key, pid):

	project = gddCityProject.objects.get(pk = pid)
	return render_to_response('gdd-city-form-delete.html', { 'key': key, 'pid': pid, 'project': project, 'guid': key })

def gdd_city_group_delete_verify(request, key, gid):

	group = gddCityGroup.objects.get(pk = gid)
	return render_to_response('gdd-city-group-delete.html', { 'key': key, 'gid': gid, 'group': group, 'guid': key })

	
def gdd_ctiy_project_delete(request, key, pid):

	project = gddCityProject.objects.get(pk=pid)
	project.delete()
	
	return HttpResponseRedirect("/gdd-city/" + key)

def gdd_city_group_delete(request, key, gid):

	group = gddCityGroup.objects.get(pk=gid)
	group.delete()
	
	return HttpResponseRedirect("/gdd-groups/" + key)

	
def gdd_city_form_end(request, key):
	
	return render_to_response('gdd-city-form-end.html', { 'key': key })

def gdd_tel_aviv(request):
	
	return render_to_response('reg-index.html')



