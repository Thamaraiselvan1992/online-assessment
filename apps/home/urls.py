from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    
    path('assessments/', views.assesments, name="assessments"),
    path('test/', views.test, name="test"),
    path('create-assesment/', views. create_assesment, name="create-assesment"),
    path('add-candidate/<id>', views.add_candidate, name="add-candidate/<id>"),
    path('send_mail', views.send_mail_test, name="send_mail"),
   

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]