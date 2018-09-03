#_*_coding:utf-8_*_
import sys,os
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
BaseDir = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2])
sys.path.append(BaseDir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","OathBreaker.settings")

sys.path.append("/mnt/OathBreaker")
from OathBreaker import settings
#from jobs import models
import django
import subprocess
from ast import literal_eval
from datetime import datetime
from jobs.models import *
from hosts.models import *
django.setup()

def save_script_content_v2(script_name,script_type,script_content):
    script_dir = "%s/%s" % (settings.ScriptUploadDir,script_type)
    master_ip = settings.Salt_API['url'].split('/')[-2].split(':')[0]
    script_root_path = settings.Salt_Script_Path + script_type
    script_relative_path = settings.Salt_Script_Relative_Path + script_type
    script_path_dict = {}

    if not os.path.isdir(settings.ScriptUploadDir):
        os.mkdir(settings.ScriptUploadDir)

    if not os.path.isdir(script_dir):
        os.mkdir(script_dir)

    if script_type == "shell":
        shell_name = script_name + ".sh"
        shell_script_abs_path = "%s/%s" % (script_dir,shell_name)
        save_content2file(shell_script_abs_path,script_content)
        if os.path.isfile(shell_script_abs_path):
            os.system("scp -P 55210 %s root@%s:%s" % (shell_script_abs_path,master_ip,script_root_path))
            script_salt_abs_path = script_root_path + "/" + shell_script_abs_path.split("/")[-1]
            script_salt_relative_path = script_relative_path + "/" + shell_script_abs_path.split("/")[-1]
            script_path_dict = {
                "abs_path":script_salt_abs_path,
                "rel_path":script_salt_relative_path
            }
            return script_path_dict

    elif script_type == "batch":
        batch_name = script_name + ".bat"
        batch_script_abs_path = "%s/%s" % (script_dir,batch_name)
        save_content2file(batch_script_abs_path,script_content)
        if os.path.isfile(batch_script_abs_path):
            os.system("scp -P 55210 %s root@%s:%s" % (batch_script_abs_path,master_ip,script_root_path))
            script_salt_abs_path = script_root_path + "/" + batch_script_abs_path.split("/")[-1]
            script_salt_relative_path = script_relative_path + "/" + batch_script_abs_path.split("/")[-1]
            script_path_dict = {
                "abs_path": script_salt_abs_path,
                "rel_path": script_salt_relative_path
            }
            return script_path_dict

    elif script_type == "python":
        python_name = script_name + ".py"
        python_script_abs_path = "%s/%s" % (script_dir,python_name)
        save_content2file(python_script_abs_path,script_content)
        if os.path.isfile(python_script_abs_path):
            os.system("scp -P 55210 %s root@%s:%s" % (python_script_abs_path,master_ip,script_root_path))
            script_salt_abs_path = script_root_path + "/" + python_script_abs_path.split("/")[-1]
            script_salt_relative_path = script_relative_path + "/" + python_script_abs_path.split("/")[-1]
            script_path_dict = {
                "abs_path": script_salt_abs_path,
                "rel_path": script_salt_relative_path
            }
            return script_path_dict

    elif script_type == "powershell":
        powershell_name = script_name + ".ps1"
        powershell_script_abs_path = "%s/%s" % (script_dir,powershell_name)
        save_content2file(powershell_script_abs_path,script_content)
        if os.path.isfile(powershell_script_abs_path):
            os.system("scp -P 55210 %s root@%s:%s" % (powershell_script_abs_path,master_ip,script_root_path))
            script_salt_abs_path = script_root_path + "/" + powershell_script_abs_path.split("/")[-1]
            script_salt_relative_path = script_relative_path + "/" + powershell_script_abs_path.split("/")[-1]
            script_path_dict = {
                "abs_path": script_salt_abs_path,
                "rel_path": script_salt_relative_path
            }
            return script_path_dict
    else:
        print "Wrong script type"


def save_content2file(file_path,file_content):
    f = file(file_path,"w+")
    f.writelines(file_content)
    f.flush()
    f.close()


def get_script_content(script_type,script_name):
    script_path = "%s/%s/%s" % (settings.ScriptUploadDir, script_type,script_name)
    if os.path.isfile(script_path):
        with open(script_path,'r') as myfile:
            script_content = myfile.read()
        return script_content
    else:
        return "script does not exit"

def get_script_store_path(script_name):
    pass

class ScriptGen(object):
    def __init__(self,request,abs_path,rel_path):
        self.request = request
        self.abs_path = abs_path
        self.rel_path = rel_path

    def parse_data(self):
        script_data ={
            "scriptname":self.request.POST.get("script_name"),
            "description":self.request.POST.get("script_description"),
            "script_type":self.request.POST.get("script_type"),
            "abs_path":self.abs_path,
            "rel_path":self.rel_path,
            "create_user_id":self.request.user.id,
        }
        return script_data

    def parse_data2(self):
        script_data = {
            "scriptname": self.request.POST.get("script_name"),
            "description": self.request.POST.get("script_description"),
            "script_type": self.request.POST.get("script_type"),
            "abs_path": self.abs_path,
            "rel_path": self.rel_path,
            "update_user_id": self.request.user.id,
        }
        return script_data

    def create(self):
        self.data = self.parse_data()
        script_obj = Script(**self.data)
        script_obj.save()
        return script_obj

    def update(self,script_id):
        self.data = self.parse_data2()
        script_obj = Script.objects.get(id=script_id)
        script_obj.scriptname = self.data["scriptname"]
        script_obj.description = self.data["description"]
        script_obj.abs_path = self.data["abs_path"]
        script_obj.rel_path = self.data["rel_path"]
        script_obj.update_user_id = self.data["update_user_id"]
        script_obj.update_date = datetime.now()
        script_obj.save()
        return script_obj


def addScriptSuffix(script_name,script_type):
    if script_name.split(".")[-1] in ["sh","bat","py","ps1"]:
        print "script name already has suffix"
    else:
        if script_type == "shell":
            script_name = script_name + ".sh"
        elif script_type == "batch":
            script_name = script_name + ".bat"
        elif script_type == "python":
            script_name = script_name + ".py"
        elif script_type == "powershell":
            script_name = script_name + ".ps1"
        else:
            print "No such script type!"
        return script_name


def handle_template_type_choice_to_en(template_type_cn):
    template_types_choice = (
        ("undefined", u'未分类'),
        ("issuefix", u'故障处理'),
        ("usualtool", u'常用工具'),
        ("fortest", u'测试专用'),
    )
    for choice in template_types_choice:
        if choice[1] == template_type_cn:
            return choice[0]

def handle_template_type_choice_to_cn(template_type_en):
    template_types_choice = (
        ("undefined", u'未分类'),
        ("issuefix", u'故障处理'),
        ("usualtool", u'常用工具'),
        ("fortest", u'测试专用'),
    )
    for choice in template_types_choice:
        if choice[0] == template_type_en:
            return choice[1]

def handle_business_unit(business_unit):
    bn_tuple = (business_unit,"","NULL")
    return bn_tuple

class TemplateGen(object):
    def __init__(self,request):
        self.request = request

    def init_create(self,template_type,business_unit_obj):
        template_data = {
            "name":self.request.POST.get("template_name"),
            "template_type":template_type,
            "business_unit":business_unit_obj,
            "comments":self.request.POST.get("template_comments"),
            "create_user_id":self.request.user.id
        }
        template_obj = Template(**template_data)
        template_obj.save()
        return template_obj


def handle_step_type_to_cn(step_type_en):
    step_type_choice = (
        ("execute_script", u'执行脚本'),
        ("push_file", u'分发文件'),
        ("pull_file", u'拉取文件'),
        ("text_step", u'文本步骤'),
    )
    for step_type in step_type_choice:
        if step_type[0] == step_type_en:
            return step_type[1]


class TemplateStepGen(object):
    def __init__(self,request):
        self.request = request

    def parse_data(self):
        templatestep_data = {
            "name": self.request.POST.get("step_script_name"),
            "description": self.request.POST.get("step_script_description"),
            "target": self.request.POST.get("script_type"),

        }
        return templatestep_data




class RunJobStep(object):
    def __init__(self,request):
        self.request = request
        self.history_step_id =  self.request.POST.get("history_step_id")

    def handle(self):
        history_step_obj = HistoryStep.objects.get(id=self.history_step_id)
        history_step_type = (TemplateStep.objects.get(id=history_step_obj.templatestep_id)).step_type
        if hasattr(self,history_step_type):
            func = getattr(self,history_step_type)
            return func()
        else:
            raise TypeError

    @transaction.atomic
    def execute_script(self):
        print "---going to execute_script---"
        history_step_obj = HistoryStep.objects.get(id=self.history_step_id)
        print "history_step_obj===>",history_step_obj
        template_obj = Template.objects.get(id=self.request.POST.get("template_id"))
        print "template_obj===>",template_obj
        private_setting_flag = (TemplateStep.objects.get(id=history_step_obj.templatestep_id)).private_setting
        print "private_setting_flag===>",private_setting_flag
        templatestep_id = (TemplateStep.objects.get(id=history_step_obj.templatestep_id)).id
        print "templatestep_id===>",templatestep_id


        #target hosts
        target_list = []
        if private_setting_flag:
            target_hosts = (TemplateStep.objects.get(id=history_step_obj.templatestep_id)).target
        else:
            target_hosts = template_obj.target

        print "target_hosts===>",target_hosts

        if isinstance(target_hosts, basestring):

            if target_hosts not in ["NULL", "None"]:
                for target in literal_eval(target_hosts):
                    target_list.append(target)
        elif all(isinstance(item, basestring) for item in target_hosts):  # check iterable for stringness of all items. Will raise TypeError if some_object is not iterable
            for target in target_hosts:
                target_list.append(target)
        else:
            raise TypeError  # or something along that line


        print "target_list===>",target_list

        #script type
        templatescript_obj = TemplateStepScript.objects.get(step_id=templatestep_id)
        print "templatescript_obj===>",templatescript_obj
        script_id = templatescript_obj.script_id
        print "script_id===>",script_id
        try:
            script_obj = Script.objects.get(id=script_id)
        except ObjectDoesNotExist, e:
            err_msg = str(e)
        script_type = script_obj.script_type
        print "script_type===>",script_type

        #script param
        script_param = templatescript_obj.parameter
        print "script_param===>",script_param
        #script abs path
        script_abs_path = script_obj.abs_path
        print "script_abs_path===>",script_abs_path

        task_obj = TaskLog(
            task_type="multi_script",
            user_id=self.request.user.id,
            script_type=script_type,
            script_param=script_param,
            script_path=script_abs_path
        )
        task_obj.save()
        task_obj.hosts.add(*target_list)

        for bind_host_id in target_list:
            taskdetail_obj = TaskLogDetail(
                child_of_task_id = task_obj.id,
                bind_host_id = bind_host_id,
                event_log = "N/A"
            )
            taskdetail_obj.save()


        # invoke backend multitask script
        # p = subprocess.Popen([
        #     'python',
        #     settings.MultiTaskScript,
        #     '-task_id', str(task_obj.id),
        #     '-run_type', settings.MultiTaskRunType, ])
        # ], preexec_fn=os.setsid)
        # print '----->pid:', p.pid

        return {"task_id": task_obj.id}