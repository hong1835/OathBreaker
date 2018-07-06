#_*_coding:utf-8_*_
from django.contrib import admin
import auth_admin
import models
from assets import models as assets_models
# Register your models here.

class BaseAdmin(object):
    """自定义admin类"""


    choice_fields = []
    fk_fields = []
    dynamic_fk = None
    dynamic_list_display = []
    dynamic_choice_fields = []
    m2m_fields = []

class HostAdmin(admin.ModelAdmin):
    list_editable = ('hostname', 'ip_addr')
    list_display = ('hostname', 'ip_addr', 'port', 'idc', 'system_type', 'enabled')
    search_fields = ('hostname', 'ip_addr')
    list_filter = ('idc', 'system_type')

class HostUserAdmin(admin.ModelAdmin):
    list_display = ('auth_type','username','password')

class BindHostToUserAdmin(admin.ModelAdmin):
    list_display = ('host','host_user','get_groups')
    filter_horizontal = ('host_groups',)


class OperationAuditLogAdmin(admin.ModelAdmin,BaseAdmin):
    list_display = ('hostname','host_ip','task_type','operation_log','date','username','result')
    search_fields = ('hostname',)
    list_filter = ('task_type','hostname','host_ip','date','username','result')

admin.site.register(models.UserProfile,auth_admin.UserProfileAdmin)
#admin.site.register(models.Host,HostAdmin)
#admin.site.register(assets_models.Server,HostAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.IDC)
admin.site.register(models.HostUser,HostUserAdmin)
admin.site.register(models.BindHostToUser,BindHostToUserAdmin)
admin.site.register(models.TaskLog)
admin.site.register(models.TaskLogDetail)
admin.site.register(models.OperationAuditLog,OperationAuditLogAdmin)