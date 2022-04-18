from django.shortcuts import render
from .models import Bug, Project, ProjectModule
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType  
from django.contrib.admin.models import LogEntry, ADDITION  
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.postgres.aggregates import ArrayAgg
import logging
logger = logging.getLogger(__name__)
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


def likePost(request):
  
        if request.method == 'GET':
                post_id = request.GET['post_id']
                likedpost = Project.objects.filter(id=post_id).select_related()
                return JsonResponse(list(likedpost.values('assign','assign__username')), safe = False)
        else:
               return HttpResponse("Request method is not a GET")


def assignProjectUser(request):
    if request.method == 'POST':
        userData=[]
        select_user=[]
        
        select=ProjectModule.objects.filter(project=request.POST.get('project'),project_module=request.POST.get('project_module')).select_related().values('assign_module_user')
        for aum in select:
            select_user.append(aum['assign_module_user'])
            
        
        
        # return HttpResponse(request)
        likedpost = Project.objects.filter(id=request.POST.get('project')).select_related().values('assign','assign__username')
        if likedpost:
            for un in likedpost:
                user={}
                if un['assign'] in select_user:
                    user['select']='selected'   
                else:
                    user['select']=''    
                # return HttpResponse(user['select'])
                user['assign']=un['assign']
                user['username']=un['assign__username']
                userData.append(user)
        # user['select'] =select_user
        # Bug.objects.all().delete()
        return JsonResponse({'user':list(userData),'select_user':select_user}, safe = False)

    else:
        return HttpResponse("Request method is not a GET")

def assignProjectModels(request):
    if request.method == 'POST':
        userData=[]
        select_module=[]
        select_user=[]
        if request.POST.get('project_module') !='':
            select = ProjectModule.objects.filter(project=request.POST.get('project'),id=request.POST.get('project_module')).values('assign_module_user','assign_module_user__username')
            if select:
                for un in select:
                    user={}  
                    # return HttpResponse(user['select'])
                    user['id']=un['assign_module_user']
                    user['username']=un['assign_module_user__username']
                    select_user.append(user)
                    
        modules = ProjectModule.objects.filter(project=request.POST.get('project')).values('id','project_module')
        return JsonResponse({'module':list(modules),'select_user':list(select_user)}, safe = False)

    else:
        return HttpResponse("Request method is not a GET")
