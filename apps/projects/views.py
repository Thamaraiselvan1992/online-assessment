from django.shortcuts import render
from .models import Bug, Project
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def projectlist(request):

    if request.user.is_superuser == 1:
            post =Project.objects.all()
    else:
            post =Project.objects.get(user_id= request.user.id)

   
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
    post =Bug.objects.all()
    # students = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(post, 3)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request,'home/bug.html',{'projects':post,'segment':'bugs'})

@login_required(login_url="/login/")
def bugloglist(request):
    post =Bug.objects.all()
    # students = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(post, 3)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request,'home/buglogs.html',{'projects':post,'segment':'buglog'})