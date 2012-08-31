from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from goodnet.models import *
from goodnet.forms import RegistrationForm, PostForm, LoginForm
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
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])	
			user.save()
#			profile = user.get_profile()
#			profile.save()
			profile = Profile(user=user, profile_type=form.cleaned_data['profile_type'], name=form.cleaned_data['name'], avatar=form.cleaned_data['avatar'], agreement=form.cleaned_data['agreement'], datebirth=form.cleaned_data['datebirth'], phone=form.cleaned_data['phone'], website=form.cleaned_data['website'], facebook=form.cleaned_data['facebook'], desc=form.cleaned_data['desc'], categories=form.cleaned_data['categories'], area=form.cleaned_data['area'], likes=form.cleaned_data['likes'], causes_joined=form.cleaned_data['causes_joined'])
			profile.save()
			return HttpResponseRedirect('/profile/')
		else:
			return render_to_response('profiles/register.html', {'form':form}, context_instance=RequestContext(request))	
	else:
		form = RegistrationForm()
		return render_to_response('profiles/register.html', {'form':form}, context_instance=RequestContext(request))


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
