from django.shortcuts import render
from .models import Bug, Project
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType  
from django.contrib.admin.models import LogEntry, ADDITION  
@login_required(login_url="/login/")
def projectlist(request):

    if request.user.is_superuser == 1:
            post =Bug.objects.select_related('project').values('project__created_at','project__project_name','project__completion_date').all().annotate(total=Count('project'))
    else:
            post =Bug.objects.select_related('project').values('project__created_at','project__project_name','project__completion_date').filter(assign_user= request.user.id).annotate(total=Count('project'))

   
    # students = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(post, 3)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request,'home/project.html',{'projects':post,'segment':'projects'})


@login_required(login_url="/login/")
def buglist(request):
    if request.user.is_superuser == 1:
            post =Bug.objects.all()
    else:
            post =Bug.objects.filter(assign_user= request.user.id)
    # students = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(post, 3)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request,'home/bug.html',{'bugs':post,'segment':'bugs'})

@login_required(login_url="/login/")
def bugloglist(request):
    # post =Bug.objects.all()
    post=LogEntry.objects.all()
    # students = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(post, 3)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request,'home/buglogs.html',{'bug':post,'segment':'buglog'})