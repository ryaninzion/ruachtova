from goodnet.models import *
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
	exclude = ('author',)

	def save_model(self, request, obj, form, change):
		obj.author = request.user
		obj.save()

admin.site.register(Post, PostAdmin)
admin.site.register(Event)
admin.site.register(Category)

