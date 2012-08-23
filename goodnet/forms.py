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
		except: User.DoesNotExist:
			return username
		raise forms.ValidationError('שם משתמש כבר קיים. אנא בחר בשם משתמש שונה.')

	def clean_password(self):
		password = self.cleaned_data['password']
		password1 = self.cleaned_data['password1']
		if password != password1:
			raise forms.ValidationError('סיסמות לא תאמו. אנא נסה שוב.')
		return password
