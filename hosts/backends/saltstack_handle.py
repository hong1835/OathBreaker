import time
import json
from hosts import models
from django.utils import timezone
import sys,os
from OathBreaker import settings
from saltapi import SaltAPI

def salt_run_script(task_id,host_obj,script_type,script_path,script_param,user_name):
    print "going to run--->",host_obj,script_type,script_param,script_path
    bind_host = host_obj
    saltapi = SaltAPI(
        url=settings.Salt_API['url'],
        username=settings.Salt_API['user'],
        password=settings.Salt_API['password']
    )
    try:
        if script_param:
            if script_type == "powershell":
                result = saltapi.saltRun(tgt=bind_host.host.ip_addr,func='cmd.script',arg1=script_path,arg2=script_param,arg3='shell=powershell')
            else:
                result = saltapi.saltRun(tgt=bind_host.host.ip_addr,func='cmd.script',arg1=script_path,arg2=script_param)
        else:
            if script_type == "powershell":
                result = saltapi.saltRun(tgt=bind_host.host.ip_addr, func='cmd.script', arg1=script_path,arg2='shell=powershell')
            else:
                result = saltapi.saltRun(tgt=bind_host.host.ip_addr, func='cmd.script', arg1=script_path)

        stderr = result['return'][0][bind_host.host.ip_addr]["stderr"]
        stdout = result['return'][0][bind_host.host.ip_addr]["stdout"]
        result = stdout, stderr
        cmd_result_flag = filter(lambda x: len(x) > 0, result)
        if cmd_result_flag:
            cmd_result = filter(lambda x: len(x) > 0, result)[0]
        else:
            cmd_result = 'no result return'
        result = "success"
    except Exception,e:
        print("\033[31;1m%s\033[0m" % e)
        cmd_result = e
        result = 'failed'

    #save output to db
    log_obj = models.TaskLogDetail.objects.get(child_of_task_id=task_id, bind_host_id=bind_host.id)
    log_obj.event_log = cmd_result
    log_obj.date = timezone.now()
    log_obj.result = result

    log_obj.save()

    audit_log_obj = models.OperationAuditLog(
        task_type="script",
        username=user_name,
        hostname=bind_host.host.hostname,
        host_ip=bind_host.host.ip_addr,
        operation_log=script_path,
        result=result
    )
    audit_log_obj.save()
