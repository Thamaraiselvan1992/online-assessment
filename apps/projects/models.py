from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Priority(models.Model):
   
    priority_name =models.CharField(max_length=200,unique=True)
    class Meta:
        verbose_name_plural = "3. Bug Priorities"
    def __str__(self):
        return self.priority_name

class Type(models.Model):
   
    type_name =models.CharField(max_length=200,unique=True)
    class Meta:
        verbose_name_plural = "4. Bug Types"
    def __str__(self):
        return self.type_name

class Status(models.Model):
   
    status_name =models.CharField(max_length=200,unique=True)
    class Meta:
        verbose_name_plural = "5. Bug Status"
    def __str__(self):
        return self.status_name


# class Class(models.Model):
#     cnmae =models.CharField(max_length=200)
class Project(models.Model):

    project_name =models.CharField(max_length=200,unique=True)
    descriptions =models.TextField()
    assign = models.ManyToManyField(User,related_name='user')
    completion_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by =models.ForeignKey(User, null=True, blank=True,
    on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "1. Projects"
    def __str__(self):
        return self.project_name

class ProjectModule(models.Model):
    project =models.ForeignKey(Project,on_delete=models.PROTECT)
    project_module =models.CharField(max_length=200)
    assign_module_user = models.ManyToManyField(User,related_name='assign')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # created_by =models.ForeignKey(User, null=True, blank=True,
    # on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "2. Project Modules"
    def __str__(self):
        return self.project_module

class Bug(models.Model):
    task =models.CharField(max_length=200,verbose_name='bug name')
    project  = models.ForeignKey(Project,
    on_delete=models.PROTECT,related_name='bug')
    project_module =models.ForeignKey(ProjectModule,on_delete=models.PROTECT)
    priority  = models.ForeignKey(Priority,on_delete=models.PROTECT)
    
    status  = models.ForeignKey(Status,on_delete=models.PROTECT)

    type  = models.ForeignKey(Type,
    on_delete=models.PROTECT)
    assign_user  =models.ForeignKey(User,on_delete=models.CASCADE,related_name='assign_module_user')
    descriptions =models.TextField()
    attachment = models.ImageField(upload_to='images',null=True, blank=True)
    remark =models.CharField(max_length=500,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by =models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name='assign_auth_user')
    class Meta:
        verbose_name_plural = "6. Bugs"
    def __str__(self):
        return self.task

# class Class(models.Model):
#     cnmae =models.CharField(max_length=200)


# class Subject(models.Model):
#     cid= models.ManyToManyField(Class)

