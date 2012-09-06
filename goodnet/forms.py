# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from goodnet.models import *
from django.forms.widgets import *


PROFILE_TYPE_CHOICES = [['org', 'פרופיל ארגון'],['personal', 'פרופיל חבר']]

class RegistrationForm(ModelForm):
	profile_type	= forms.ChoiceField(widget=RadioSelect(), choices=PROFILE_TYPE_CHOICES)
	username	= forms.CharField("שם משתמש")
	email		= forms.EmailField("כתובת דואל")
	password	= forms.CharField("סיסמה", widget=forms.PasswordInput(render_value=False))
	password1	= forms.CharField("אימות סיסמה", widget=forms.PasswordInput(render_value=False))

	class Meta:
		model = Profile
		exclude = ('user', 'avatar', 'datebirth', 'phone', 'website', 'facebook', 'desc', 'categories', 'area', 'likes', 'causes_joned',)

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
	area = forms.ModelMultipleChoiceField(queryset=Area.objects.all(),widget=forms.CheckboxSelectMultiple(),required=False)

	class Meta:
		model = Profile
		exclude = ('agreement', 'likes', 'causes_joined',)

	def clean(self):
		return self.cleaned_data


class LoginForm(forms.Form):
	username	= forms.CharField("username")
	password	= forms.CharField("Password", widget=forms.PasswordInput(render_value=False))


class PostForm(ModelForm):

	class Meta:
		model = Post
