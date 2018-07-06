from django.db import transaction
import models
import json
import subprocess
from OathBreaker import settings
import utils

class Task(object):
    def __init__(self,request):
        self.request = request
        self.task_type = self.request.POST.get("task_type")

    def handle(self):
        if self.task_type:
            if hasattr(self,self.task_type):
                func = getattr(self,self.task_type)
                return func()
            else:
                raise TypeError

    @transaction.atomic
    def multi_cmd(self):
        print "---going to run cmd---"
        print self.request.POST
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        cmd = self.request.POST.get("cmd")
        print "-->",selected_hosts,cmd
        #create task info
        task_obj = models.TaskLog(
            task_type = self.task_type,
            user_id = self.request.user.id,
            cmd = cmd,
        )
        task_obj.save()
        task_obj.hosts.add(*selected_hosts) # add many to many relationship
        #task_obj.hosts.add([1,2,3])

        #create task detailed record for all the hosts will be executed later
        for bind_host_id in selected_hosts:
            obj = models.TaskLogDetail(
                child_of_task_id = task_obj.id,
                bind_host_id = bind_host_id,
                event_log = "N/A"
            )
            obj.save()

        # invoke backend multitask script
        p = subprocess.Popen([
            'python',
            settings.MultiTaskScript,
            '-task_id', str(task_obj.id),
            '-run_type', settings.MultiTaskRunType,])
        #], preexec_fn=os.setsid)
        #print '----->pid:', p.pid
        return {"task_id":task_obj.id}


    def multi_file_transfer(self):
        print "---going to upload/download files"
        print self.request.POST
        data_dic = {}
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        transfer_type = self.request.POST.get("file_transfer_type")
        if self.request.POST.get("remote_path"):
            data_dic["remote_path"] = self.request.POST.get("remote_path")
        if self.request.POST.getlist("upload_files[]"):
            data_dic["upload_files"] = self.request.POST.getlist("upload_files[]")
        if self.request.POST.getlist("download_files[]"):
            data_dic["download_files"] = self.request.POST.getlist("download_files[]")


        # create task info
        task_obj = models.TaskLog(
            task_type=transfer_type,
            user_id=self.request.user.id,
            cmd=json.dumps(data_dic)
        )
        task_obj.save()
        task_obj.hosts.add(*selected_hosts)  # add many to many relationship
        # task_obj.hosts.add([1,2,3])

        # create task detailed record for all the hosts will be executed later
        for bind_host_id in selected_hosts:
            obj = models.TaskLogDetail(
                child_of_task_id=task_obj.id,
                bind_host_id=bind_host_id,
                event_log="N/A"
            )
            obj.save()

        # invoke backend multitask script
        p = subprocess.Popen([
            'python',
            settings.MultiTaskScript,
            '-task_id', str(task_obj.id),
            '-run_type', settings.MultiTaskRunType, ])
        # ], preexec_fn=os.setsid)
        # print '----->pid:', p.pid
        return {"task_id": task_obj.id}

    def operation_audit(self):
        print "---going to show operations audit----"
        print self.request.POST
        task_id_list = []
        child_task_id_list = []
        selected_hosts_list = set(self.request.POST.getlist("selected_hosts[]"))

        task_obj = models.TaskLog.objects.filter(user_id=self.request.user.id)
        child_task_obj = models.TaskLogDetail.objects.filter(child_of_task__tasklogdetail__bind_host_id__in=selected_hosts_list)
        for child_task in child_task_obj:
            child_task_id_list.append(child_task.id)
        print "--->child_task_id_list",child_task_id_list
        #task_obj = models.TaskLog.objects.filter(id=44)
        for task in task_obj:
            task_id_list.append(task.id)
        print "task_id_list--->",task_id_list
        print task_id_list,type(task_id_list)
        return {"task_id": task_id_list}

    def get_task_result(self):
        task_id = self.request.GET.get("task_id")
        if task_id:
            res_list = models.TaskLogDetail.objects.filter(child_of_task_id=task_id)
            return list(res_list.values(
                "id",
                "bind_host__host__hostname",
                "bind_host__host__ip_addr",
                "bind_host__host_user__username",
                "date",
                "event_log",
                "result"
            ))


    def get_operation_audit(self):
        task_id = self.request.GET.get("task_id")
        if task_id:
            res_list = models.TaskLogDetail.objects.filter(child_of_task_id=task_id)
            return list(res_list.values(
                "id",
                "bind_host__host__hostname",
                "child_of_task__cmd",
                "bind_host__host__ip_addr",
                "bind_host__host_user__username",
                "date",
                "result"
            ))

    def check_iplist(self):
        selected_ips = set(self.request.POST.getlist("selected_ips[]"))
        selected_hosts = {}


        for ip in selected_ips:
            if models.BindHostToUser.objects.filter(host__ip_addr=ip):
                #obj = models.Host.objects.all().filter(ip_addr=ip).values("id")
                obj = models.BindHostToUser.objects.filter(host__ip_addr=ip).values("id")
                obj = list(obj)

                print "obj",obj

                selected_hosts[ip] = obj
        print "selected_hosts==>",selected_hosts
        return selected_hosts


    def multi_script(self):
        print "---going to run script---"
        print self.request.POST
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        script_type = self.request.POST.get("script_type")
        script_param = self.request.POST.get("script_param")
        script_content = self.request.POST.get("script_content")
        #print "--->",selected_hosts,script_type,script_param,script_content
        script_abs_path = utils.save_script_content(script_type,script_content)
        print "script_abs_path--->",script_abs_path
        #create task info
        task_obj = models.TaskLog(
            task_type = self.task_type,
            user_id = self.request.user.id,
            script_type = script_type,
            script_param = script_param,
            script_path = script_abs_path
        )
        task_obj.save()
        task_obj.hosts.add(*selected_hosts)

        #create task detailed record for all the hosts will be executed later
        for bind_host_id in selected_hosts:
            obj = models.TaskLogDetail(
                child_of_task_id = task_obj.id,
                bind_host_id = bind_host_id,
                event_log = "N/A"
            )
            obj.save()

        # invoke backend multitask script
        p = subprocess.Popen([
            'python',
            settings.MultiTaskScript,
            '-task_id', str(task_obj.id),
            '-run_type', settings.MultiTaskRunType, ])
        # ], preexec_fn=os.setsid)
        # print '----->pid:', p.pid

        return {"task_id": task_obj.id}
