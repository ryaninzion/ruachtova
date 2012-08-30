# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from goodnet.models import *

class RegistrationForm(ModelForm):
	username	= forms.CharField(label=(u'שם משתמש'))
	email		= forms.EmailField(label=(u'כתובת דוא"ל'))
	password	= forms.CharField(label=(u'סיסמה'), widget=forms.PasswordInput(render_value=False))
	password1	= forms.CharField(label=(u'אימות סיסמה'), widget=forms.PasswordInput(render_value=False))

	class Meta:
		model = Profile
		exclude = ('user',)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(u'שם משתמש כבר קיים. אנא בחר בשם משתמש שונה.')

	def clean(self):
		if self.cleaned_data['password'] != self.cleaned_data['password1']:
			raise forms.ValidationError(u'סיסמות לא תאמו. אנא נסה שוב.')
		return self.cleaned_data


class LoginForm(forms.Form):
	username	= forms.CharField(label=(u'username'))
	password	= forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))


class PostForm(ModelForm):

	class Meta:
		model = Post
