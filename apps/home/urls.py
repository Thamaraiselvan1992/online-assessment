from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    
    path('assesments/', views.assesments, name="assesments"),
    path('test/', views.test, name="test"),
    path('create-assesment/', views. create_assesment, name="create-assesment"),
   

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]