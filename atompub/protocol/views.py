from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader
from django.http import HttpResponse

from models import Workspace, Collection


def service(request):
    
    workspaces = Workspace.objects.all()
    
    return HttpResponse(loader.render_to_string("service.xml", {"workspaces": workspaces}), mimetype="application/atomsvc+xml")
