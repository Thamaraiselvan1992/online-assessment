from django.contrib.contenttypes.models import ContentType
from django.contrib import admin

from apps.projects.models import Bug, Project,Priority,Status,Type
# Register your models here.
# from django_summernote.admin import SummernoteModelAdmin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt


@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    if instance.is_superuser:
        raise PermissionDenied
#user models
class MyUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['labels'] = {'groups': 'Roles'}
        return super().get_form(request, obj=obj, change=change, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        
            if obj: 
                if request.user.is_superuser != 1:
                    return ['username', 'is_active','is_staff','is_superuser','last_login_0','last_login_1','date_joined_0','date_joined_1','user_permissions','groups']
         
            return self.readonly_fields

    def get_queryset(self, request):
        if request.user.is_superuser == 1:
            return super().get_queryset(request).all()
        else:
            return super().get_queryset(request).filter(id=request.user.id)

  

# Bugs Models
class BugAdmin(admin.ModelAdmin):
    summernote_fields = ('descriptions')
    ordering =('-priority','status')
    list_display = ['task','project','priority','status','type','assign_user']
    search_fields = ['task', 'project__project_name','status__status_name','type__type_name','priority__priority_name']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    fieldsets = (               # Edition form
        (None,                   {'fields': ('task',
                                             ('project','assign_user'),('priority','type'),('descriptions','attachment'),('remark','status'))}),
                                             (_('More...'), {'fields': (('created_at', 'updated_at'), 'created_by'), 'classes': ('collapse',)}),
        
    )
  
  
    list_per_page = 10
    def save_model(self, request, obj,form,change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()
        
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['assign_user'].queryset = User.objects.filter(is_superuser=0)
         return super(BugAdmin, self).render_change_form(request, context, *args, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        
            if obj: 
                if request.user.is_superuser != 1:
                    
                    return ['task','project','priority','attachment','type','assign_user','created_at', 'updated_at', 'created_by']

            return self.readonly_fields

    def get_queryset(self, request):
        if request.user.is_superuser == 1:
            return super().get_queryset(request).all()
        else:
            return super().get_queryset(request).filter(assign_user=request.user)  


    def remark(self, instance):

        return "<span class='errors'>I can't determine this address.</span>"


#Project Models
class PostAdmin(admin.ModelAdmin):
    search_fields = ['project_name', 'descriptions','completion_date']
    list_display = ('project_name','created_by','completion_date')
    # fields = ['project_name','descriptions','completion_date']

    readonly_fields =['created_by']
    list_per_page = 10
    # fieldsets = (               # Edition form
    #     (None,                   {'fields': ('project_name', 'descriptions',
    #                                          ('assign', 'completion_date'))}),
        
    # )
    def save_model(self, request, obj,form,change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()

    # def render_change_form(self, request, context, *args, **kwargs):
    #     context['adminform'].form.fields['assign'].queryset = User.objects.filter(is_superuser=0)
    #     return super(BugAdmin, self).render_change_form(request, context, *args, **kwargs)
   

admin.site.register(Project,PostAdmin)
admin.site.register(Bug,BugAdmin)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Priority)
admin.site.register(Status)
admin.site.register(Type)

class BugLog(LogEntry):

    class Meta:
        proxy = True
        verbose_name_plural = "Bugs Reports"
@admin.register(LogEntry)
class LogAdmin(admin.ModelAdmin):
    """Create an admin view of the history/log table"""
    list_display = ('object_repr','action_time','user','content_type','change_message','action_flag','object_link')
    list_filter = ['action_time','user','content_type']
    readonly_fields = ('object_id','object_repr','action_time','user','content_type','change_message','is_addition','is_change','is_deletion')
    search_fields = ['object_repr', 'change_message']
    ordering = ('-action_time',)
    list_per_page = 10
    #We don't want people changing this historical record:
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        #returning false causes table to not show up in admin page :-(
        #I guess we have to allow changing for now
        return True
    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        if request.user.is_superuser == 1:
            return super().get_queryset(request).all()
        else:
            return super().get_queryset(request).filter(user_id=request.user.id)
        # qs = super(LogAdmin, self).get_queryset(request)
        # ct = ContentType.objects.get_for_model(Bug)
        # qs = qs.filter(id__in=list(
        #          LogEntry.objects.filter(content_type=ct)\
        #                          .values_list('object_id', flat=True)))
        # return qs


    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
#     # def log(request, obj, level, message=''):
#     #     LogEntry.objects.log_action(
#     #         content_type_id=ContentTypeHeader.objects.get_for_model(Bug).id
#     #     )
@admin.register(BugLog)
class LogAdmin(admin.ModelAdmin):
        list_display = ('object_repr','action_time','user','content_type','change_message','action_flag')
        list_filter = ['action_time','user','content_type']
        readonly_fields = ('object_id','object_repr','action_time','user','content_type','change_message','is_addition','is_change','is_deletion')
        search_fields = ['object_repr', 'change_message']
        ordering = ('-action_time',)
        list_per_page = 10
        #We don't want people changing this historical record:
        def has_add_permission(self, request):
            return False
        def has_change_permission(self, request, obj=None):
            #returning false causes table to not show up in admin page :-(
            #I guess we have to allow changing for now
            return True
        def has_delete_permission(self, request, obj=None):
            return False
        def get_queryset(self, request):
            qs = super(LogAdmin, self).get_queryset(request)
            ct = ContentType.objects.get_for_model(Bug)
            if request.user.is_superuser == 1:
                qs = qs.filter(id__in=list(
                        LogEntry.objects.filter(content_type=ct.id)\
                                        .values_list( flat=True)))
            else :
                qs = qs.filter(id__in=list(
                        LogEntry.objects.filter(content_type=ct.id,
                                                user=request.user)\
                                        .values_list( flat=True)))

            return qs

# admin.site.register(BugLoggAdmin)