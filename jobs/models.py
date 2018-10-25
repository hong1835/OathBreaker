#_*_coding:utf-8_*_
from django.db import models
import assets
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


class Template(models.Model):
    name = models.CharField(verbose_name=u'模版名称',max_length=128,unique=True)
    template_types_choice = (
        ("undefined", u'未分类'),
        ("issuefix", u'故障处理'),
        ("usualtool", u'常用工具'),
        ("fortest", u'测试专用'),
    )
    template_type = models.CharField(choices=template_types_choice,max_length=64,default="undefined")
    business_unit = models.ForeignKey("assets.BusinessUnit",verbose_name=u'所属业务', null=True, blank=True)
    comments = models.TextField(max_length=2048,blank=True,null=True)
    templace_mode_choice = (
        ("slient", u'无人模式'),
        ("single", u'单步模式'),
        ("mix", u'混合模式'),
    )
    execute_mode = models.CharField(choices=templace_mode_choice,max_length=64,default="single")
    create_user = models.ForeignKey('hosts.UserProfile', related_name=u'template_create_user', verbose_name=u'创建用户',null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey('hosts.UserProfile', related_name=u'template_update_user', verbose_name=u'更新用户',null=True, blank=True)
    update_date = models.DateTimeField(blank=True, null=True)
    target = models.TextField(verbose_name=u'目标机器', blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    shared_with = models.ManyToManyField('hosts.UserProfile', related_name=u'template_shared_user', verbose_name=u'授权用户',blank=True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'模版'
        verbose_name_plural = u"模版"


class TemplateStep(models.Model):
    template = models.ForeignKey(Template,verbose_name=u"模版")
    name = models.CharField(max_length=128,verbose_name=u"步骤名称",blank=True,null=True)
    description = models.CharField(max_length=1024,verbose_name=u"步骤描述",blank=True,null=True)
    step_type_choice = (
        ("execute_script", u'执行脚本'),
        ("push_file", u'分发文件'),
        ("pull_file", u'拉取文件'),
        ("text_step", u'文本步骤'),
    )
    step_type = models.CharField(verbose_name=u"步骤类型",max_length=128,choices=step_type_choice,default="execute_script")
    order = models.IntegerField(verbose_name=u"步骤顺序",blank=True,null=True)
    private_setting = models.BooleanField(verbose_name=u"单独设定",default=False)
    target = models.TextField(verbose_name=u'目标机器', blank=True, null=True)
    is_checked = models.BooleanField(verbose_name=u"是否勾选",default=True)
    is_delete = models.BooleanField(verbose_name=u"是否删除",default=False)

    def __unicode__(self):
        #return self.name
        return unicode(self.name) or u''

    class Meta:
        verbose_name = "TemplateStep"
        verbose_name_plural = "TemplateStep"


class TemplateStepScript(models.Model):
    step = models.ForeignKey(TemplateStep,verbose_name=u"模版步骤")
    script = models.ForeignKey(Script,verbose_name=u"脚本名",blank=True,null=True)
    parameter = models.CharField(max_length=512,verbose_name=u"入口参数",blank=True,null=True)

    def __unicode__(self):
        return "%s:%s" % (self.step.name,self.script.scriptname)

    class Meta:
        verbose_name = "TemplateStepScript"
        verbose_name_plural = "TemplateStepScript"


class TemplateStepText(models.Model):
    step = models.ForeignKey(TemplateStep,verbose_name=u"模版步骤")
    description = models.CharField(max_length=512,verbose_name=u"文本描述",default="")

    def __unicode__(self):
        return "%s:%s" % (self.step.name,self.description)

    class Meta:
        verbose_name = "TemplateStepText"
        verbose_name_plural = "TemplateStepText"



class History(models.Model):
    template = models.ForeignKey(Template,verbose_name="作业")
    start_time = models.DateTimeField(auto_now_add=True,verbose_name=u"开始时间")
    end_time = models.DateTimeField(blank=True, null=True,verbose_name=u"结束时间")
    cost_time = models.IntegerField(verbose_name=u"总耗时",blank=True,null=True)
    run_user = models.ForeignKey('hosts.UserProfile', related_name=u'history_create_user', verbose_name=u'执行人',null=True, blank=True)
    HISTORY_STATUS_CHOICES = (
        ("not_start", u'未执行'),
        ("success", u'执行成功'),
        ("fail", u'执行失败'),
        ("in_process", u'执行中'),
    )
    status = models.CharField(verbose_name=u"作业执行状态",max_length=128,choices=HISTORY_STATUS_CHOICES,default="not_start")
    HISTORY_RUN_TYPE_CHOICES = (
        ("manual", u'手动执行任务'),
        ("auto", u'自动执行任务'),
    )
    startup_type = models.CharField(verbose_name=u"作业启动方式",max_length=128,choices=HISTORY_RUN_TYPE_CHOICES,default="manual")

    def __unicode__(self):
        return self.template.name

    class Meta:
        verbose_name = "History"
        verbose_name_plural = "History"


class HistoryStep(models.Model):
    history = models.ForeignKey(History,verbose_name=u"作业历史")
    templatestep = models.ForeignKey(TemplateStep,verbose_name=u"作业步骤")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=u"开始时间")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name=u"结束时间")
    cost_time = models.IntegerField(verbose_name=u"步骤耗时", blank=True, null=True)
    HISTORYSTEP_RESULT_CHOICES = (
        ("not_start", u'未执行'),
        ("running", u'正在执行'),
        ("success", u'执行成功'),
        ("complete",u"执行完毕"),
        ("fail", u'执行失败'),
        ("skip", u'跳过'),
        ("ignore", u'忽略错误'),
        ("wait_user", u'等待用户'),
        ("manual_stop", u'手动结束'),
        ("abnormal", u'状态异常'),
        ("force_stop", u'步骤强制终止中'),
        ("force_stop_success", u'步骤强制终止成功'),
        ("force_stop_fail", u'步骤强制终止失败'),
    )
    result = models.CharField(verbose_name=u"步骤执行结果",max_length=128,choices=HISTORYSTEP_RESULT_CHOICES,default="not_start")
    total_hosts = models.TextField(verbose_name=u"目标机器",blank=True,null=True)
    success_hosts = models.TextField(verbose_name=u"执行成功的机器",blank=True,null=True)
    fail_hosts = models.TextField(verbose_name=u"执行失败的机器",blank=True,null=True)
    task_id = models.IntegerField(verbose_name=u"TaskID",default=0)

    def __unicode__(self):
        return self.templatestep.name

    class Meta:
        verbose_name = "HistoryStep"
        verbose_name_plural = "HistoryStep"


class RunningResult(models.Model):
    step = models.ForeignKey(HistoryStep,verbose_name=u"历史作业步骤")
    tasklog = models.ForeignKey("hosts.TaskLog")
    tasklogdetail = models.ForeignKey("hosts.TaskLogDetail")