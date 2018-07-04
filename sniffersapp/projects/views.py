from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Project
from .forms import ProjectForm

def project_list(request, template='projects/project_list.html'):
    context = {
         'project_list': Project.objects.all(),
     }
    return render(request, template, context)

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {
        'project': project,
    }
    template = 'projects/project_detail.html'
    return render(request, template, context)

def project_form(request, project_id=None, template='projects/project_form.html'):
    if project_id:
        existing_project = get_object_or_404(Project, pk=project_id)
    else:
        existing_project = None

    project_form = ProjectForm(request.POST or None, instance=existing_project)
    
    if request.method == 'POST':
        if project_form.is_valid():
            project = project_form.save(commit=False)
            if not existing_project:
                project.created_user = request.user
            project.save()
            messages.success(request, f'Project "{project.project_name}" saved successfully.')
            return redirect('projects:list')

    context = {
        'project_form': project_form,
        'title': str(existing_project) if existing_project else 'New Project',
    }

    return render(request, template, context)
