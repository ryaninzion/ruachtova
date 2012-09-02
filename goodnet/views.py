from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from goodnet.models import *
from goodnet.forms import RegistrationForm, ProfileForm, PostForm, LoginForm
from django.contrib.auth import authenticate, login, logout


def post(request,id):
	post = get_object_or_404(Post,pk=id)
	return render_to_response('posts/view.html',{'post':post},context_instance=RequestContext(request))


def post_form(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			pass
		else:
			form = PostForm()
			return render_to_response('posts/create.html', {'form':form}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/goodnet/post/not_logged_in/')


def registration(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/goodnet/profile/')
	else:
		if request.method == 'POST':
			form = RegistrationForm(request.POST)
			if form.is_valid():
				user = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
				user.save()
				profile = Profile(user=user, profile_type = form.cleaned_data['profile_type'], agreement = form.cleaned_data['agreement'])
				profile.save()

				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				profile = authenticate(username=username, password=password)
				login(request, profile)
				return HttpResponseRedirect('/goodnet/profile-edit/')
			else:
				return render_to_response('profiles/register.html', {'form':form}, context_instance=RequestContext(request))
		else:
			form = RegistrationForm()
			return render_to_response('profiles/register.html', {'form':form}, context_instance=RequestContext(request))



def profile_edit(request):
	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		if request.method == 'POST':
			form = ProfileForm(request.POST, instance=user.get_profile())
			if form.is_valid():
				profile = user.get_profile()
				profile.save()
				profile.categories = form.cleaned_data['categories']
				profile.area = form.cleaned_data['area']
				profile.save()
				return HttpResponseRedirect('/goodnet/profile/')
			else:
				return render_to_response('profiles/createprofile.html', {'form':form}, context_instance=RequestContext(request))
		else:
			form = ProfileForm(instance=user.get_profile())
			return render_to_response('profiles/createprofile.html', {'form':form}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/goodnet/register/') 


def loginrequest(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			profile = authenticate(username=username, password=password)
			if profile is not None:
				login(request, profile)
				return HttpResponseRedirect('/profile/')
			else:
				return HttpResponseRedirect('/login/')
		else:
			return render_to_response('profiles/login.html', {'form':form}, context_instance=RequestContext(request))	
	else:
		form = LoginForm()
		return render_to_response('profiles/login.html', {'form':form}, context_instance=RequestContext(request))


def logoutrequest(request):
	logout(request)
	return HttpResponseRedirect('/')
