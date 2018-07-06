#_*_coding:utf-8_*_
from django.db import models



# Create your models here.
from myauth import UserProfile
from assets.models import Asset
import assets

# class Host(models.Model):
#     hostname = models.CharField(max_length=64)
#     ip_addr = models.GenericIPAddressField(unique=True)
#     port = models.IntegerField(default=22)
#     idc = models.ForeignKey("IDC")
#     system_type_choice = (
#         ('linux',"Linux"),
#         ("windows","Windows")
#     )
#     system_type = models.CharField(choices=system_type_choice,max_length=32,default='linux')
#     enabled = models.BooleanField(default=True)
#     memo = models.TextField(blank=True,null=True)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __unicode__(self):
#         return "%s(%s)" % (self.hostname,self.ip_addr)
#     class Meta:
#         verbose_name = u'主机列表'
#         verbose_name_plural = u"主机列表"

class IDC(models.Model):
    name = models.CharField(u'机房名称',max_length=128,unique=True)
    memo = models.TextField(u'备注',blank=True,null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"

class HostUser(models.Model):
    auth_type_choices = (
        ("ssh-password","SSH/PASSWORD"),
        ("ssh-key","SSH/KEY")
    )
    auth_type = models.CharField(choices=auth_type_choices,max_length=32,default="ssh-password")
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128,blank=True,null=True)

    def __unicode__(self):
        return "(%s)%s" % (self.auth_type,self.username)
    class Meta:
        unique_together = ("auth_type","username","password")
        verbose_name = u'远程主机用户'
        verbose_name_plural = u"远程主机用户"

class HostGroup(models.Model):
    name = models.CharField(unique=True,max_length=64)
    memo = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = u"主机组"

class BindHostToUser(models.Model):
    host = models.ForeignKey("assets.Server")
    host_user = models.ForeignKey("HostUser")
    host_groups = models.ManyToManyField("HostGroup")

    def __unicode__(self):
        return "%s:%s" % (self.host.hostname,self.host_user.username)

    class Meta:
        unique_together = ("host","host_user")
        verbose_name = u'主机与用户绑定关系'
        verbose_name_plural = u"主机与用户绑定关系"

    def get_groups(self):
        return ",".join([g.name for g in self.host_groups.select_related()])

class TaskLog(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True,blank=True)
    task_type_choices = (('multi_cmd',"CMD"),('multi_script',"Script"),('file_send',"批量发送文件"),('file_get',"批量下载文件"))
    task_type = models.CharField(choices=task_type_choices,max_length=50)
    script_type = models.CharField(max_length=32,blank=True,null=True)
    script_param = models.CharField(max_length=256,blank=True,null=True)
    script_path = models.TextField(max_length=512,blank=True,null=True)
    user = models.ForeignKey('UserProfile')
    hosts = models.ManyToManyField('BindHostToUser')
    cmd = models.TextField()
    expire_time = models.IntegerField(default=30)
    task_pid = models.IntegerField(default=0)
    note = models.CharField(max_length=100,blank=True,null=True)
    def __unicode__(self):
        return "taskid:%s script:%s" %(self.id,self.script_path)
    class Meta:
        verbose_name = u'批量任务'
        verbose_name_plural = u'批量任务'

class TaskLogDetail(models.Model):
    child_of_task = models.ForeignKey('TaskLog')
    bind_host  = models.ForeignKey('BindHostToUser')
    date = models.DateTimeField(auto_now_add=True) #finished date
    event_log = models.TextField()
    result_choices= (('success','Success'),('failed','Failed'),('unknown','Unknown'))
    result = models.CharField(choices=result_choices,max_length=30,default='unknown')
    note = models.CharField(max_length=100,blank=True)

    def __unicode__(self):
        return "child of:%s result:%s" %(self.child_of_task.id, self.result)
    class Meta:
        verbose_name = u'批量任务日志'
        verbose_name_plural = u'批量任务日志'


class OperationAuditLog(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    task_type_choices = (('cmd', "CMD"),('script',"Script") ,('file_send', "发送文件"), ('file_get', "下载文件"))
    task_type = models.CharField(choices=task_type_choices, max_length=50)
    #user = models.ForeignKey('UserProfile')
    username = models.CharField(max_length=64)
    hostname = models.CharField(max_length=64)
    host_ip = models.GenericIPAddressField()
    #bind_host = models.ForeignKey('BindHostToUser')
    operation_log = models.TextField()
    result_choices = (('success','Success'),('failed','Failed'),('unknown','Unknown'))
    result = models.CharField(choices=result_choices, max_length=30, default='unknown')

    def __unicode__(self):
        return "resultid:%s event_log:%s" % (self.id,self.operation_log)
    class Meta:
        verbose_name = u'行为审计日志'
        verbose_name_plural = u'行为审计日志'

