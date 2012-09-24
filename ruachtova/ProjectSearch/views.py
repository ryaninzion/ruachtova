# coding=utf-8

from ProjectSearch.models import *
from ProjectSearch.forms import *
from ProjectSearch.bforms import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.shortcuts import *

from django.template.loader import *

import codecs
import django.utils.simplejson as simplejson
import urllib

from ftplib import FTP

from datetime import *

def index(request):

	results = Projects.objects.filter()
	
	if request.GET: # If the form has been submitted...
		search = SearchForm(request.GET)
		
		if search.data:
			if "field" in search.data and search.data['field'] != '':
				results = results.filter(field__id = search.data['field'])
			if "area" in search.data and search.data['area'] != '':
				results = results.filter(area__id = search.data['area'])
			if "population" in search.data and search.data['population'] != '':
				results = results.filter(population__id = search.data['population'])
			# if search.data['words'] != u'חיפוש חופשי':
				# results = results.filter(description__contains = search.data['words'])

	else:
		search = SearchForm()
	
	pager = Paginator(results, 5) 

	# Make sure page request is an int. If not, deliver first page.
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1

    # If page request (9999) is out of range, deliver last page of results.
	try:
		projects = pager.page(page)
	except (EmptyPage, InvalidPage):
		projects = pager.page(paginator.num_pages)

	if request.session.has_key('cart'):
		cart = request.session['cart']
	else:
		cart = dict()
		
	querystring = request.META["QUERY_STRING"]
		
	return render_to_response('volunteer-results.html', {"projects": projects, 'search_form': search, 'cart': cart, 'querystring': querystring}, context_instance=RequestContext(request))
	
def add_to_cart(request):
	id = request.GET.get('id')
	title = Projects.objects.get(project_id = id).title
	
	if request.session.has_key('cart'):
		cart = request.session['cart']
		cart[id] = title
		request.session['cart'] = cart
	else:
		request.session['cart'] = { id: title }

	request.session.modified = True
	
	return HttpResponse(title)

def remove_from_cart(request):
	id = request.GET.get('id')
	
	del request.session['cart'][id]
	
	request.session.modified = True
	
	return HttpResponse(id)
	 
def volunteer_form(request):
	if request.method == 'POST': # If the form has been submitted...
		#form = VolunteerForm(request.POST)
		#if form.is_valid:
		return HttpResponseRedirect('/thanks/') 
	else:
		form = VolunteerForm()
	 
	return render_to_response('ruachtova-form.html', { 'form': form, 'title': 'הרשמה להתנדבות' }, context_instance=RequestContext(request))

def a_volunteer_form(request):
	if request.method == 'POST': # If the form has been submitted...
		form = ArabicVolunteerForm(request.POST)
		if form.is_valid:
			codecs.open("f:/web/forms/rtv-V-" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) +".xml", "w", "utf-8").write(render_to_string('form-output.xml', {'form': form, }))
		return render_to_response('generic-ruachtova-arabic-thanks.html')
	else:
		form = ArabicVolunteerForm()
	 
	return render_to_response('generic-ruachtova-form.html', { 'form': form, 'title': 'تسجيل للتطوع', 'send': 'إرسال' }, context_instance=RequestContext(request))

def a_project_form(request):
	if request.method == 'POST': # If the form has been submitted...
		form = ArabicProjectForm(request.POST)
		if form.is_valid:
			codecs.open("f:/web/forms/P-a-" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) +".xml", "w", "utf-8").write(render_to_string('form-output.xml', {'form': form, }))
		return HttpResponseRedirect('/a_thanks/') 
	else:
		form = ArabicProjectForm()
	 
	return render_to_response('generic-ruachtova-form.html', { 'form': form, 'title': '-تسجيل فعاليات تطوعيه لجمعيه "رواح طوبا"', 'send': 'إرسال' }, context_instance=RequestContext(request))

	 
def raanana_volunteer_form(request):
	if request.method == 'POST': # If the form has been submitted...
		form = VolunteerForm(request.POST)
		if form.is_valid():
			#form.cleaned_data["lname"] = form.data["lname"] + " RAANANA"
			#codecs.open("f:/web/forms/V" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) +"000000.xml", "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))

			filename = "V" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + "00000.xml"
			codecs.open("/var/django-code/ruachtova/forms/" + filename, "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			
			ftp = FTP("172.17.10.15") 
			ftp.login("Administrator", "rua1024")
			ftp.cwd("/Data/forms/D")
			
			ftp.storbinary("STOR " + filename, open("/var/django-code/ruachtova/forms/" + filename, "rb"))
			ftp.quit()
			
			return HttpResponseRedirect('/raanana/thanks/') 

	else:
		form = VolunteerForm() 
	 
	return render_to_response('raanana-ruachtova-form.html', { 'form': form, 'title': 'הרשמה להתנדבות' }, context_instance=RequestContext(request))

	
def thanks(request):
	return render_to_response('thanks.html')
	
def a_thanks(request):
	return render_to_response('a-thanks.html')
	
def raanana_thanks(request):
	return render_to_response('raanana-thanks.html')

def volunteer_feedback(request, guid):
	if request.method == 'POST': # If the form has been submitted...
		form = FeedbackForm(request.POST)
		if form.is_valid:
			form.save()
			return render_to_response('feedback-thanks.html')
	else:
		form = FeedbackForm(initial = { 'guid': guid } )
	 
	return render_to_response('feedback-form.html', { 'form': form, 'title': 'הרשמה להתנדבות' }, context_instance=RequestContext(request))

def theme_index(request, theme):

	results = Projects.objects.filter()
	
	if request.method == 'POST': # If the form has been submitted...
		search = SearchForm(request.POST)

		if search.data['field'] != '':
			results = results.filter(field__id = search.data['field'])
		if search.data['area'] != '':
			results = results.filter(area__id = search.data['area'])
		if search.data['population'] != '':
			results = results.filter(population__id = search.data['population'])
		if search.data['words'] != u'חיפוש חופשי':
			results = results.filter(description__contains = search.data['words'])
	
	else:
		search = SearchForm()
	
	pager = Paginator(results, 5) 

	# Make sure page request is an int. If not, deliver first page.
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1

    # If page request (9999) is out of range, deliver last page of results.
	try:
		projects = pager.page(page)
	except (EmptyPage, InvalidPage):
		projects = pager.page(paginator.num_pages)

	if request.session.has_key('cart'):
		cart = request.session['cart']
	else:
		cart = dict()
		
	return render_to_response('theme-volunteer-results.html', {"projects": projects, 'search_form': search, 'cart': cart, 'theme': theme}, context_instance=RequestContext(request))

def theme_volunteer_form(request, theme):

	form = VolunteerForm()
	
	if request.method == 'POST': # If the form has been submitted...
		form = VolunteerForm(request.POST)
		if form.is_valid():
			#form.cleaned_data["lname"] = form.data["lname"] + " BEN GURI"
			#codecs.open("f:/web/forms/V" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + theme + ".xml", "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			
			filename = "V" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + ".xml"
			codecs.open("/var/django-code/ruachtova/forms/" + filename, "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			
			ftp = FTP("172.17.10.15") 
			ftp.login("Administrator", "rua1024")
			ftp.cwd("/Data/forms/D")
			
			ftp.storbinary("STOR " + filename, open("/var/django-code/ruachtova/forms/" + filename, "rb"))
			ftp.quit()
			
			return HttpResponseRedirect('/Search/' + theme + '/Thanks/') 
	else:
		form = VolunteerForm()
	 
	return render_to_response('theme-ruachtova-form.html', { 'form': form, 'title': 'הרשמה להתנדבות', 'theme': theme }, context_instance=RequestContext(request))

def gdd_volunteer_form(request, project_id = 0):
 
	form = gddVolunteerForm()
	 
	if request.method == 'POST': # If the form has been submitted...
		form = gddVolunteerForm(request.POST)
		if form.is_valid():
			codecs.open("f:/web/forms/gdd-V-" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + ".xml", "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			return HttpResponseRedirect('/gdd-group-thanks/') 
	
	form.project_id = project_id
	 
	return render_to_response('gdd-registration-form.html', { 'form': form, 'title': 'הרשמה להתנדבות' } )

	
def gdd_volunteer_group_form(request):

	form = gddVGroupForm()
	 
	if request.method == 'POST': # If the form has been submitted...
		form = gddVGroupForm(request.POST)
		if form.is_valid():
			codecs.open("f:/web/forms/gdd-G-" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + ".xml", "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			return HttpResponseRedirect('/gdd-group-thanks/') 
	 
	return render_to_response('gdd-registration-form.html', { 'form': form, 'title': 'הרשמה להתנדבות' } )
 
def gdd_volunteer_group_form_ta(request):

	form = gddVGroupForm(initial = {'owner': 'tel-aviv'})
	 
	if request.method == 'POST': # If the form has been submitted...
		form = gddVGroupForm(request.POST)
		if form.is_valid():
			form.cleaned_data['owner'] = "KAR\\morb"
			codecs.open("f:/web/forms/gdd-G-" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + ".xml", "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			return HttpResponseRedirect('/gdd-group-thanks/') 
	 
	return render_to_response('gdd-registration-form.html', { 'form': form, 'title': 'הרשמה להתנדבות' } )


def gdd_arabic_volunteer_form(request):

	form = gddArabicVolunteerForm()
	 
	if request.method == 'POST': # If the form has been submitted...
		form = gddArabicVolunteerForm(request.POST)
		if form.is_valid():
			codecs.open("f:/web/forms/gdd-V-" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + ".xml", "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			return HttpResponseRedirect('/gdd-thanks/arabic/') 
	 
	return render_to_response('gdd-registration-arabic-form.html', { 'form': form } )

	
def gdd_arabic_volunteer_group_form(request):

	form = gddArabicGroupForm()
	 
	if request.method == 'POST': # If the form has been submitted...
		form = gddArabicGroupForm(request.POST)
		if form.is_valid():
			codecs.open("f:/web/forms/gdd-G-" + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + ".xml", "w", "cp1255").write(render_to_string('form-output.xml', {'form': form, }))
			return HttpResponseRedirect('/gdd-thanks/arabic/') 
	 
	return render_to_response('gdd-registration-arabic-form.html', { 'form': form } )


	
	
def gdd_group_thanks(request):
	
	return render_to_response('gdd-group-form-end.html' )

def gdd_arabic_thanks(request):
	
	return render_to_response('gdd-arabic-form-end.html' )

	
def theme_thanks(request, theme):
	return render_to_response('theme-thanks.html', {'theme': theme})

def theme_search(request, theme):
	form = SearchForm()
	
	return render_to_response('theme-search.html', {'form': form, 'theme': theme})
	
def theme_search_long(request, theme):
	form = SearchForm()
	
	return render_to_response('theme-search-long.html', {'form': form, 'theme': theme})
	
def theme_search_mini(request, theme):
	form = SearchForm()
	
	return render_to_response('theme-search-mini.html', {'form': form, 'theme': theme})
	
def create_engine(request):
	#form = EngineGenerateForm()
	
	return render_to_response('generate-engine.html')
	
def get_colors(request):
	website = request.GET["website"]
	
	sock = urllib.urlopen("http://vmshp02/Integration/AjaxColors?webpage=" + website) 
	htmlSource = sock.read()                            
	sock.close()  

	colors = simplejson.loads(htmlSource)
	
	return render_to_response('generate-engine-colors.html', {'colors': colors})

	
def get_search_engine(request):
	orientation = request.GET["orientation"]
	color = request.GET["color"]
	
	sock = urllib.urlopen("http://vmshp02/Integration/CreateColor/" + color) 
	#htmlSource = sock.read()                            
	sock.close()  

	#colors = simplejson.loads(htmlSource)
	
	return HttpResponseRedirect('/Search/' + color + '/' + orientation) 

def gdd_city(request, key):
	
	return render_to_response('city-index.html')
	
def gdd_add_project(request, signature, number):
    
    initial = {0: {'signature': signature, 'number': number }, }

    # Create the form wizard
    form = AddProjectFormWizard([gddProjectFormProject, gddProjectFormPlace], initial=initial)

    # Call the form wizard passing through the context and the request
    return form(context=RequestContext(request), request=request)
	
def gdd_project_thanks(request, signature, number):

	return render_to_response('gdd-project-form-end.html', { 'signature': signature, 'number': number })

