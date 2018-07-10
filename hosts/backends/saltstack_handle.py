import time
import json
from hosts import models
from django.utils import timezone
import sys,os
from OathBreaker import settings
from saltapi import SaltAPI
from hosts import utils
import datetime

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



def salt_transfer_file(task_id,host_obj,task_content,task_type,user_id,user_name):
    bind_host = host_obj
    saltapi = SaltAPI(
        url=settings.Salt_API['url'],
        username=settings.Salt_API['user'],
        password=settings.Salt_API['password']
    )
    try:
        task_dic = json.loads(task_content)
        if task_type == "file_send":
            upload_files = task_dic["upload_files"]
            remote_files = []
            for file_path in upload_files:
                salt_file_relative_path = "%s/%s" % (settings.Salt_File_Transfer_Upload,file_path)
                remote_filename = file_path.split("/")[-1]
                remote_files.append(remote_filename)
                remote_file_abs_path = "%s/%s" % (task_dic['remote_path'].rstrip("/"),remote_filename)
                result = saltapi.saltRun(tgt=bind_host.host.ip_addr, func='cp.get_file', arg1=salt_file_relative_path, arg2=remote_file_abs_path)
            cmd_result = "successfully send files %s to remote path [%s]" % (remote_files, task_dic['remote_path'])
            stdout = result['return'][0][bind_host.host.ip_addr]
            result = "success"
        elif task_type == "file_get":
            download_files = task_dic["download_files"]
            successful_download_files = []
            datetime_prefix = datetime.datetime.now().strftime("%Y-%m-%d")
            master_ip = settings.Salt_API['url'].split('/')[-2].split(':')[0]
            local_file_path = "%s/%s/%s/%s" % (settings.Salt_File_Transfer_Download,user_name,datetime_prefix,bind_host.host.ip_addr)
            #print "download_files-->", download_files,type(download_files)
            for download_file in download_files:
                result = saltapi.saltRun(tgt=bind_host.host.ip_addr, func='cp.push',arg1=download_file)
                # for windows type eg. C:\temp\xxx.ini
                if "\\" in download_file:
                    download_file = download_file.replace("\\", "/")
                    download_file = "/" + download_file
                download_To_local = settings.Salt_File_Transfer_Download_Abs_Path + bind_host.host.ip_addr + "/files" + download_file
                handle_result = utils.salt_handle_download_file(user_name,master_ip,download_To_local,bind_host.host.ip_addr)
                if handle_result:
                    successful_download_files.append(download_file)
            if successful_download_files:
                cmd_result = "successfully download files from %s to [%s]" % (successful_download_files,local_file_path)
                result = "success"
            else:
                cmd_result = "Failed to download files"
                result = "failed"
    except Exception,e:
        print e
        cmd_result = e
        result = "failed"

    # save outputs to db

    log_obj = models.TaskLogDetail.objects.get(child_of_task_id=task_id, bind_host_id=bind_host.id)
    log_obj.event_log = cmd_result
    log_obj.date = timezone.now()
    log_obj.result = result

    log_obj.save()

    audit_log_obj = models.OperationAuditLog(
        task_type=task_type,
        username=user_name,
        hostname=bind_host.host.hostname,
        host_ip=bind_host.host.ip_addr,
        operation_log=cmd_result,
        result = result
    )
    audit_log_obj.save()