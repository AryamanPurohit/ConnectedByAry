from django.shortcuts import render, redirect
from .models import Project,Review,Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from .utils import searchProjects,paginateProjects
from django.contrib import messages
# Create your views here.

def projects(request):

    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    
    context ={'projects':projects, 'search_query':search_query,'custom_range':custom_range}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectObj = Project.objects.get(id = pk)

    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        #Updating project and owner related to that review
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.voteCount
        
        messages.success(request, "Review Submitted Successfully!")
        return redirect('single-project',pk=projectObj.id)
    
    context={"project" : projectObj, 'form':form}
    return render(request,'projects/single-project.html',context)

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newTags = request.POST.get('newtags').split(',')
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile   
            project.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
                
            return redirect('account')

    #Processing the submitted info
    context ={'form':form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='login')
def updateProject(request,pk):

    profile = request.user.profile 
    project = profile.project_set.get(id=pk) # 1 To N relation between Profile and Project models
    form = ProjectForm(instance = project)  #To auto fill the form information regarding the existing project
 
    if request.method == 'POST':
        newTags = request.POST.get('newtags').split(',')
        
        form = ProjectForm(request.POST , request.FILES,instance=project)

        if form.is_valid():
            project = form.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    #Processing the submitted info
    context ={'form':form,'project':project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='login')
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context ={'object' : project}
    return render(request, 'delete_temp.html',context)
