import sys,os
BaseDir = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2])
sys.path.append(BaseDir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","OathBreaker.settings")

sys.path.append("/mnt/OathBreaker")
from OathBreaker import settings
#from jobs import models
import django
from datetime import datetime
from jobs.models import *
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

