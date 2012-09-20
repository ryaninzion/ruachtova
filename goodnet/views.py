# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.template import RequestContext
from goodnet.models import *
from goodnet.forms import *
from django.contrib.auth import authenticate, login, logout


def static_elements():
	sidebar_updates = Post.objects.all().order_by('-cdate')[:3] 
	sidebar_events = Event.objects.order_by('date')[:3]
	lform = LoginForm()
	profile_search = ProfileSearchForm()
	event_search = EventSearchForm()
	initiative_search = InitiativeSearchForm()
	return {'sidebar_updates':sidebar_updates,'sidebar_events':sidebar_events,'lform':lform,'profile_search':profile_search,'event_search':event_search,'initiative_search':initiative_search}

def post(request,id):
	post = get_object_or_404(Post,pk=id)
	type = 'post'
	results = {'post':post, 'type':type, 'request':request}
	results.update(static_elements())
	return render_to_response('goodnet/posts/view.html',results,context_instance=RequestContext(request))

def event(request,id):
	event = get_object_or_404(Event,pk=id)
	type = 'event'
	results = {'post':event, 'type':type, 'request':request}
	results.update(static_elements())
	return render_to_response('goodnet/posts/view.html',results,context_instance=RequestContext(request))

def initiative(request,id):
	initiative = get_object_or_404(Initiative,pk=id)
	type = 'initiative'
	results = {'post':initiative, 'type':type, 'request':request}
	results.update(static_elements())
	return render_to_response('goodnet/posts/view.html',results,context_instance=RequestContext(request))

def bookmark(request,type,id):
	post = id
	profile = request.user.get_profile()
	profile.likes.add(post)
	profile.save()
	if type == 'event':
		return HttpResponseRedirect('/goodnet/event/%s' % post)
	elif type == 'initiative':
		return HttpResponseRedirect('/goodnet/initiative/%s' % post)
	else:
		return HttpResponseRedirect('/goodnet/post/%s' % post)

def join_cause(request,type,id):
	post = id
	profile = request.user.get_profile()
	profile.causes_joined.add(post)
	profile.save()
	if type == 'event':
		return HttpResponseRedirect('/goodnet/event/%s' % post)
	elif type == 'initiative':
		return HttpResponseRedirect('/goodnet/initiative/%s' % post)
	else:
		return HttpResponseRedirect('/goodnet/post/%s' % post)

def post_form(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			if request.POST['selected_form'] == 'pform':

				new_post = PostForm(request.POST, request.FILES)
				new_post.author = request.user
				if new_post.is_valid():
					post = new_post.save(commit=False)
					post.author = request.user
					post.save()
					return HttpResponseRedirect('/goodnet/post/%i' % post.id)
				else:
					return render_to_response('goodnet/posts/create.html', {'pform':new_post}, context_instance=RequestContext(request))
			elif request.POST['selected_form'] == 'eform':
				
				new_event = EventForm(request.POST, request.FILES)
				new_event.author = request.user
				if new_event.is_valid():
					event = new_event.save(commit=False)
					event.author = request.user
					event.save()
					return HttpResponseRedirect('/goodnet/event/%i' % event.id)
				else:
					return render_to_response('goodnet/posts/create.html', {'eform':new_event}, context_instance=RequestContext(request))
			else:
				new_initiative = InitiativeForm(request.POST, request.FILES)
				new_initiative.author = request.user
				if new_initiative.is_valid():
					initiative = new_initiative.save(commit=False)
					initiative.author = request.user
					initiative.save()
					return HttpResponseRedirect('/goodnet/initiative/%i' % initiative.id)
				else:
					return render_to_response('goodnet/posts/create.html', {'iform':new_initiative}, context_instance=RequestContext(request))
		else:
			pform = PostForm()
			eform = EventForm()
			iform = InitiativeForm()
			user = request.user
			results = {'pform':pform,'eform':eform,'iform':iform,'user':user}
			results.update(static_elements())
			return render_to_response('goodnet/posts/create.html', results, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/goodnet/login/')


def photo_form(request,id):
	if request.user.is_authenticated():
		if request.method == 'POST':
			for afile in request.FILES.getlist('image'):
    				obj = Photo(image=afile, creator=request.user).save()
			form = PhotoForm()
			success = "תמונות הועלו בהצלחה"
			return render_to_response('goodnet/profiles/photo_form.html', {'form':form, 'success':success}, context_instance=RequestContext(request))
		else:
			form = PhotoForm()
			return render_to_response('goodnet/profiles/photo_form.html', {'form':form}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/goodnet/not_logged_in/')


def profile(request,id):
	profile = get_object_or_404(Profile,pk=id)
	gallery = Photo.objects.filter(creator=profile.user.id)
	results = {'profile':profile, 'gallery':gallery, 'request':request}
	results.update(static_elements())
	return render_to_response('goodnet/profiles/view.html',results,context_instance=RequestContext(request))

def add_friend(request,id):
	profile = request.user.get_profile()
	target = Profile.objects.get(pk=id)
	profile.friends = (target.id,) 
	profile.save()
	return render_to_response('goodnet/profiles/friend_added.html', {'target':target}, context_instance=RequestContext(request))


def registration(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/goodnet/profile/')
	else:
		if request.method == 'POST':
			form = RegistrationForm(request.POST, request.FILES)
			if form.is_valid():
				user = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
				user.save()
				profile = Profile(user=user, profile_type = form.cleaned_data['profile_type'], name=form.cleaned_data['name'], avatar=form.cleaned_data['avatar'], agreement = form.cleaned_data['agreement'])
				profile.save()

				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				profile = authenticate(username=username, password=password)
				login(request, profile)
				return HttpResponseRedirect('/goodnet/profile-edit/%i/' % request.user.pk)
			else:
				return render_to_response('goodnet/profiles/register.html', {'form':form}, context_instance=RequestContext(request))
		else:
			form = RegistrationForm()
			results = {'form':form, 'request':request}
			results.update(static_elements())
			return render_to_response('goodnet/profiles/register.html', results, context_instance=RequestContext(request))



def profile_edit(request,id):
	if request.user.is_authenticated():
		user = User.objects.get(pk=id)
		if request.method == 'POST':
			form = ProfileForm(request.POST, request.FILES, instance=user.get_profile())
			if form.is_valid():
				profile = user.get_profile()
				profile.save()
				profile.categories = form.cleaned_data['categories']
				profile.areas = form.cleaned_data['areas']
				profile.save()
				return HttpResponseRedirect('/goodnet/profile/%i/' % request.user.get_profile().pk)
			else:
				results = {'form':form, 'request':request}
				results.update(static_sidebar())
				return render_to_response('goodnet/profiles/createprofile.html', results, context_instance=RequestContext(request))
		else:
			form = ProfileForm(instance=user.get_profile())
			results = {'form':form, 'request':request}
			results.update(static_elements())
			return render_to_response('goodnet/profiles/createprofile.html', results, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/goodnet/register/') 


def search_results(request):

	if request.POST:
		if request.POST['type'] == 'profile':
			search = ProfileSearchForm(request.POST)
			results = Profile.objects.filter()
			if search.data:
				if "category" in search.data and search.data['category'] != '':
					results = results.filter(categories__id = search.data['category'])
				if "area" in search.data and search.data['area'] != '':
					results = results.filter(areas__id = search.data['area'])
		elif request.POST['type'] == 'event':
			search = EventSearchForm(request.POST)
			results = Event.objects.filter()
			if search.data:
				if "category" in search.data and search.data['category'] != '':
					results = results.filter(category = search.data['category'])
				if "location" in search.data and search.data['location'] != '':
					results = results.filter(location = search.data['location'])
		elif request.POST['type'] == 'initiative':
			search = InitiativeSearchForm(request.POST)
			results = Initiatve.objects.filter()
			if search.data:
				if "category" in search.data and search.data['category'] != '':
					results = results.filter(category__id = search.data['category'])
				if "location" in search.data and search.data['location'] != '':
					results = results.filter(location__id = search.data['location'])
		else:
			return HttpResponseRedirect('/goodnet/')

	else:
		return HttpResponseRedirect('/goodnet/')
	
	pager = Paginator(results, 10) 

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1

	try:
		projects = pager.page(page)
	except (EmptyPage, InvalidPage):
		projects = pager.page(paginator.num_pages)

	querystring = request.META["QUERY_STRING"]
		
	rsults = {'projects':projects,'querystring':querystring}
	rsults.update(static_elements())
	return render_to_response('goodnet/search/results.html', rsults, context_instance=RequestContext(request))


def loginrequest(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/goodnet/profile/%i/' % request.user.get_profile().pk)
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			profile = authenticate(username=username, password=password)
			if profile is not None:
				login(request, profile)
				return HttpResponseRedirect('/goodnet/profile/%i/' % request.user.get_profile().pk)
			else:
				return HttpResponseRedirect('/goodnet/login/')
		else:
			return render_to_response('goodnet/profiles/login.html', {'form':form}, context_instance=RequestContext(request))	
	else:
		form = LoginForm()
		return render_to_response('goodnet/profiles/login.html', {'form':form}, context_instance=RequestContext(request))


def logoutrequest(request):
	logout(request)
	return HttpResponseRedirect('/goodnet/')
