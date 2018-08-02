#_*_coding:utf-8_*_
from django.db import models

# Create your models here.
#from hosts.myauth import UserProfile

class Script(models.Model):
    scriptname = models.CharField(verbose_name=u'脚本',max_length=128,unique=True)
    description = models.TextField(verbose_name=u'脚本描述',max_length=100000,blank=True,null=True)
    script_type_choices = (
        ("shell","Shell"),
        ("batch","Batch"),
        ("python", "Python"),
        ("powershell", "Powershell")
    )
    script_type = models.CharField(choices=script_type_choices,max_length=64,default="shell")
    abs_path = models.CharField(verbose_name=u'绝对路径',max_length=1024,blank=True,null=True)
    rel_path = models.CharField(verbose_name=u'相对路径',max_length=1024,blank=True,null=True)
    create_user = models.ForeignKey('hosts.UserProfile', related_name=u'scipt_create_user',verbose_name=u'创建用户', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey('hosts.UserProfile', related_name=u'script_update_user',verbose_name=u'更新用户', null=True, blank=True)
    update_date = models.DateTimeField(blank=True,null=True)
    is_delete = models.BooleanField(default=False)
    shared_with = models.ManyToManyField('hosts.UserProfile',related_name=u'scipt_shared_user',verbose_name=u'授权用户',blank=True)

    def __unicode__(self):
        return self.scriptname
    class Meta:
        verbose_name = u'脚本名称'
        verbose_name_plural = u"脚本名称"
