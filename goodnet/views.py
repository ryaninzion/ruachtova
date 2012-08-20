from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from goodnet.models import *

def event(request,id):
	ev = get_object_or_404(Event,pk=id)
	return render_to_response('events/view.html',{'event':ev},context_instance=RequestContext(request))
	