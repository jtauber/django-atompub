from django.shortcuts import render_to_response, get_object_or_404

from models import Workspace, Collection


def service(request):
    
    workspaces = Workspace.objects.all()
    
    return render_to_response("service.xml", {
        "workspaces": workspaces,
    })
