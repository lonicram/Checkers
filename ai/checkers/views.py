from django.shortcuts import render, render_to_response
from django.core.context_processors import request
from django.http.response import HttpResponse
from django.template.context import RequestContext

# Create your views here.
def homepage(request):

    return render_to_response('homepage.html', RequestContext(request))
