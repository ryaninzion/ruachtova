# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from goodnet.models import *
from goodnet.forms import *
from django.contrib.auth import authenticate, login, logout


def static_sidebar():
#	TODO :  implement 
	return {'sidebar_updates':['a','b','c'],'sidebar_events':['v','x','y']}

def post(request,id):
	post = get_object_or_404(Post,pk=id)
	return render_to_response('goodnet/posts/view.html',{'post':post},context_instance=RequestContext(request))

def bookmark(request,id):
	post = id
	profile = request.user.get_profile()
	profile.likes.add(post)
	profile.save()
	return HttpResponseRedirect('/goodnet/post/%s' % post)

def join_cause(request,id):
	post = id
	profile = request.user.get_profile()
	profile.causes_joined.add(post)
	profile.save()
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
				if new_event.is_valid():
					new_event.author = user
					new_event.save()
					return HttpResponseRedirect('/goodnet/event/%i' % new_event.pk)
				else:
					return render_to_response('goodnet/posts/create.html', {'eform':new_event}, context_instance=RequestContext(request))
			else:
				new_initiative = InitiativeForm(request.POST, request.FILES)
				if new_initiative.is_valid():
					new_initiative.author = user
					new_initiative.save()
					return HttpResponseRedirect('/goodnet/initiative/%i' % new_initiative.pk)
				else:
					return render_to_response('goodnet/posts/create.html', {'iform':new_initiative}, context_instance=RequestContext(request))
		else:
			pform = PostForm()
			eform = EventForm()
			iform = InitiativeForm()
			user = request.user
			return render_to_response('goodnet/posts/create.html', {'pform':pform, 'eform':eform, 'iform':iform, 'user':user}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/goodnet/post/not_logged_in/')


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
	results.update(static_sidebar())
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
			return render_to_response('goodnet/profiles/register.html', {'form':form}, context_instance=RequestContext(request))



def profile_edit(request,id):
	if request.user.is_authenticated():
		user = User.objects.get(pk=id)
		if request.method == 'POST':
			form = ProfileForm(request.POST, request.FILES, instance=user.get_profile())
			if form.is_valid():
				profile = user.get_profile()
				profile.save()
				profile.categories = form.cleaned_data['categories']
				profile.area = form.cleaned_data['area']
				profile.save()
				return HttpResponseRedirect('/goodnet/profile/%i/' % request.user.get_profile().pk)
			else:
				return render_to_response('goodnet/profiles/createprofile.html', {'form':form}, context_instance=RequestContext(request))
		else:
			form = ProfileForm(instance=user.get_profile())
			return render_to_response('goodnet/profiles/createprofile.html', {'form':form}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/goodnet/register/') 


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
