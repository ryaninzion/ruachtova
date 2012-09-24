from django.conf.urls.defaults import patterns, include, url
from ProjectSearch.forms import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('', 
    (r'^taramta/index/$', 'ProjectSearch.views.index'),
	(r'^add-to-cart/$', 'ProjectSearch.views.add_to_cart'),
	(r'^remove-from-cart/$', 'ProjectSearch.views.remove_from_cart'),
	
	(r'^taramta/volunteer-form/$', 'ProjectSearch.views.volunteer_form'),
	(r'^thanks/$', 'ProjectSearch.views.thanks'),
	
	(r'^raanana/volunteer-form/$', 'ProjectSearch.views.raanana_volunteer_form'),
	(r'^raanana/thanks/$', 'ProjectSearch.views.raanana_thanks'),
	(r'^a-thanks/$', 'ProjectSearch.views.raanana_thanks'),
	
	(r'^arabic/volunteer-form/$', 'ProjectSearch.views.a_volunteer_form'),
	(r'^arabic/project-form/$', 'ProjectSearch.views.a_project_form'),

	(r'^feedback/([a-zA-Z0-9_.-]+)/$', 'ProjectSearch.views.volunteer_feedback'),

	(r'^Search/([a-zA-Z0-9_.-]+)/Search/$', 'ProjectSearch.views.theme_search'),
	(r'^Search/([a-zA-Z0-9_.-]+)/Vertical/$', 'ProjectSearch.views.theme_search'),
	(r'^Search/([a-zA-Z0-9_.-]+)/SearchLong/$', 'ProjectSearch.views.theme_search_long'),
	(r'^Search/([a-zA-Z0-9_.-]+)/Horizontal/$', 'ProjectSearch.views.theme_search_long'),
	(r'^Search/([a-zA-Z0-9_.-]+)/SearchMini/$', 'ProjectSearch.views.theme_search_mini'),
	
	(r'^Search/([a-zA-Z0-9_.-]+)/Index/$', 'ProjectSearch.views.theme_index'),
	(r'^Search/([a-zA-Z0-9_.-]+)/Volunteer-form/$', 'ProjectSearch.views.theme_volunteer_form'),
	(r'^Search/([a-zA-Z0-9_.-]+)/Thanks/$', 'ProjectSearch.views.theme_thanks'),
	 
	(r'^gdd-tel-aviv/$', 'gdd_interfaces.views.gdd_tel_aviv'),
	(r'^gdd-city/([a-zA-Z0-9_.-]+)$', 'gdd_interfaces.views.gdd_city'),
    (r'^gdd-city-project/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_city_project_form'),
    (r'^gdd-city-project-f/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_city_project_form', { 'is_fixed': True} ),
    (r'^gdd-city-project-d/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_city_project_form', { 'is_duplicate': True} ),
	(r'^gdd-city-logistics/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_city_logistics_form'),
	(r'^gdd-city-logistics-f/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_city_logistics_form', { 'is_fixed': True}),
	(r'^gdd-city-logistics-d/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_city_logistics_form', { 'is_duplicate': True}),
	(r'^gdd-city-group/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_city_group_form'),
	(r'^gdd-groups/([a-zA-Z0-9_.-]+)$', 'gdd_interfaces.views.gdd_city_groups'),
	(r'^gdd-city-form-end/([a-zA-Z0-9_.-]+)$', 'gdd_interfaces.views.gdd_city_form_end'),
    (r'^gdd-city-group-delete-verify/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_city_group_delete_verify'),
    (r'^gdd-city-group-delete/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_city_group_delete'),
	(r'^gdd-city-group-end/([a-zA-Z0-9_.-]+)$', 'gdd_interfaces.views.gdd_city_group_end'),
    (r'^gdd-city-form-delete/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_city_project_delete_verify'),
    (r'^gdd-city-project-delete/([a-zA-Z0-9_.-]+)/(\d+)$', 'gdd_interfaces.views.gdd_ctiy_project_delete'),

	(r'^gdd-volunteer-group-form/$', 'ProjectSearch.views.gdd_volunteer_group_form'),
	(r'^gdd-volunteer-group-form/tel-aviv/$', 'ProjectSearch.views.gdd_volunteer_group_form_ta'),
	(r'^gdd-volunteer-form/$', 'ProjectSearch.views.gdd_volunteer_form'),
	(r'^gdd-volunteer-form/(\d+)$', 'ProjectSearch.views.gdd_volunteer_form'),
	(r'^gdd-volunteer-group-form/arabic/$', 'ProjectSearch.views.gdd_arabic_volunteer_group_form'),
	(r'^gdd-volunteer-form/arabic/$', 'ProjectSearch.views.gdd_arabic_volunteer_form'),
	(r'^gdd-change-register-form/$', 'gdd_interfaces.views.gdd_change_register_form'),
	(r'^gdd-change-problem-form/([a-zA-Z0-9_.-]+)/$', 'gdd_interfaces.views.gdd_change_problem_form'),
	(r'^gdd-change-project-form/([a-zA-Z0-9_.-]+)/$', 'gdd_interfaces.views.gdd_change_project_form'),
	
	(r'^GetSearchEngine/$', 'ProjectSearch.views.create_engine'),
	(r'^GetSearchEngineColors/$', 'ProjectSearch.views.get_colors'),
	(r'^GenerateSearchEngine/$', 'ProjectSearch.views.get_search_engine'),

	(r'^gdd-project/$', ProjectFormWizard([gddProjectFormPlace, gddProjectFormProject])),
	(r'^gdd-project/tel-aviv/$', ProjectFormWizard([gddProjectFormPlace, gddProjectFormProject], initial = {0: {'owner': 'tel-aviv'}, })),
	(r'^gdd-project/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+)/$', 'ProjectSearch.views.gdd_add_project'),
	(r'^gdd-project-final/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+)/$', 'ProjectSearch.views.gdd_project_thanks'),
	(r'^gdd-city-project/$', CityFormWizard([gddProjectFormCity])),
	(r'^gdd-city/([a-zA-Z0-9_.-]+)/$', 'ProjectSearch.views.gdd_city'),
	
	(r'^gdd-group-thanks/$', 'ProjectSearch.views.gdd_group_thanks'),
	(r'^gdd-thanks/arabic/$', 'ProjectSearch.views.gdd_arabic_thanks'),
	
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '/var/django-code/ruachtova/Ruachtova/ruachtova/static-files'}),
    # Examples: 
    # url(r'^$', 'ProjectSearch.views.home', name='home'),
    # url(r'^ProjectSearch/', include('ProjectSearch.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
