# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from goodnet.models import *
from django.forms.widgets import *


PROFILE_TYPE_CHOICES = [['o', 'פרופיל ארגון'],['p', 'פרופיל חבר']]

class RegistrationForm(ModelForm):
	profile_type	= forms.ChoiceField(widget=RadioSelect(), choices=PROFILE_TYPE_CHOICES)
	username	= forms.CharField("שם משתמש")
	email		= forms.EmailField("כתובת דואל")
	password	= forms.CharField("סיסמה", widget=forms.PasswordInput(render_value=False))
	password1	= forms.CharField("אימות סיסמה", widget=forms.PasswordInput(render_value=False))

	class Meta:
		model = Profile
		exclude = ('user', 'datebirth', 'phone', 'website', 'facebook', 'desc', 'categories', 'area', 'likes', 'causes_joned',)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("שם משתמש כבר קיים. אנא בחר בשם משתמש שונה.")

	def clean(self):
		if self.cleaned_data['password'] != self.cleaned_data['password1']:
			password_match_error = u"סיסמות לא תאמו. אנא נסה שוב."
			self._errors['password'] = self.error_class([password_match_error])
		if self.cleaned_data['agreement'] != True:
			agreement_error = u"עליך להסכים לתנאי שימוש ומדיניות פרטיות של האתר."
			self._errors['agreement'] = self.error_class([agreement_error])
		return self.cleaned_data


class ProfileForm(ModelForm):
	datebirth = forms.DateField(widget=DateInput())
	categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),widget=forms.CheckboxSelectMultiple(),required=False)
	areas = forms.ModelMultipleChoiceField(queryset=Area.objects.all(),widget=forms.CheckboxSelectMultiple(),required=False)

	class Meta:
		model = Profile
		exclude = ('agreement', 'likes', 'causes_joined',)

	def clean(self):
		return self.cleaned_data


class PhotoForm(ModelForm):
	
	class Meta:
		model = Photo

class VideoForm(ModelForm):

	class Meta:
		model = Video
		exclude = ('creator', 'date', 'desc')


class LoginForm(forms.Form):
	username	= forms.CharField("username")
	password	= forms.CharField("Password", widget=forms.PasswordInput(render_value=False))


class PostForm(ModelForm):

	class Meta:
		model = Post
		exclude = ('author',)

class EventForm(ModelForm):

	class Meta:
		model = Event
		exclude = ('author',)

class InitiativeForm(ModelForm):
	
	class Meta:
		model = Initiative
		exclude = ('author',)

class ProfileSearchForm(ModelForm):
	categories = forms.ModelChoiceField(queryset=Category.objects.filter(type="profile"),empty_label='תחום',required=False)
	areas = forms.ModelChoiceField(queryset=Area.objects.all(),empty_label='אזור',required=False)

	class Meta:
		model = Profile
		fields = ('categories','areas',)	

class EventSearchForm(ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.filter(type="post"),empty_label='תחום',required=False)
	location = forms.ModelChoiceField(queryset=Area.objects.all(),empty_label='אזור',required=False)
	
	class Meta:
		model = Event
		fields = ('category','location',)

class InitiativeSearchForm(ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.filter(type="post"),empty_label='תחום',required=False)
	location = forms.ModelChoiceField(queryset=Area.objects.all(),empty_label='אזור',required=False)

	class Meta:
		model = Initiative
		fields = ('category','location',)
