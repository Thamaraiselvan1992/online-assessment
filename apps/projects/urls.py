from django.urls import path, re_path
from apps.projects import views

urlpatterns = [

    path('projects/', views.projectlist,name='project'),
    path('bugs/', views.buglist,name='bugs'),
    path('buglogs/', views.bugloglist,name='buglog')


]