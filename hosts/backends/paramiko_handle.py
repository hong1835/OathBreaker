import time
import paramiko,json
from hosts import models
from django.utils import timezone
import sys,os
from OathBreaker import settings

def paramiko_ssh(task_id,host_obj,task_content,user_name):
    print "going to run--->",host_obj,task_content
    bind_host = host_obj
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if bind_host.host_user.auth_type == 'ssh-password':
            s.connect(bind_host.host.ip_addr,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      bind_host.host_user.password,
                      timeout=5)
        else:#rsa_key
            pass
            '''
            key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            s.connect(bind_host.host.ip_addr,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      pkey=key,
                      timeout=5)
            '''
        stdin,stdout,stderr = s.exec_command(task_content)
        result = stdout.read(),stderr.read()
        cmd_result = filter(lambda x:len(x)>0,result)[0]
        result = "success"

    except Exception,e:
        print("\033[31;1m%s\033[0m" % e)
        cmd_result = e
        result = 'failed'

    #save outputs to db

    log_obj = models.TaskLogDetail.objects.get(child_of_task_id=task_id,bind_host_id=bind_host.id)
    log_obj.event_log = cmd_result
    log_obj.date = timezone.now()
    log_obj.result = result

    log_obj.save()

    audit_log_obj = models.OperationAuditLog(
        task_type="cmd",
        username=user_name,
        hostname=bind_host.host.hostname,
        host_ip=bind_host.host.ip_addr,
        operation_log=task_content,
        result = result
    )
    audit_log_obj.save()


def paramiko_sftp(task_id,host_obj,task_content,task_type,user_id,user_name):
    bind_host = host_obj

    try:
        t = paramiko.Transport((bind_host.host.ip_addr,int(bind_host.host.port)))
        if bind_host.host_user.auth_type == "ssh-password":

            t.connect(username=bind_host.host_user.username, password=bind_host.host_user.password)
        else:
            pass
            # key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            # t.connect(username=bind_host.host_user.username,pkey=key)

        sftp = paramiko.SFTPClient.from_transport(t)

        task_dic = json.loads(task_content)

        if task_type == "file_send":
            upload_files = task_dic["upload_files"]
            for file_path in upload_files:
                file_abs_path = "%s\\%s\\%s" % (settings.FileUploadDir,user_id,file_path)
                remote_filename = file_path.split("\\")[-1]
                print '---\033[32;1m sending [%s] to [%s]\033[0m' % (remote_filename, task_dic['remote_path'])
                sftp.put(file_abs_path, "%s/%s" % (task_dic['remote_path'], remote_filename))
            cmd_result = "successfully send files %s to remote path [%s]" % (upload_files, task_dic['remote_path'])
            result = 'success'
        elif task_type == "file_get":
            download_files = task_dic["download_files"]
            #print "download_files-->", download_files,type(download_files)
            for download_file in download_files:
                print "--->",download_file
                filename = download_file.split("/")[-1]
                file_abs_path = "%s\\%s\\%s\\%s" % (settings.FileDownloadDir,user_id,bind_host.host.ip_addr,filename)
                print "---\033[32;1m getting [%s] from [%s] to [%s]\033[0m" % (filename,download_file,file_abs_path)
                download_dir = "%s\\%s" % (settings.FileDownloadDir, user_id)
                download_dir2 = "%s\\%s" % (download_dir, bind_host.host.ip_addr)
                if not os.path.isdir(download_dir):
                    os.mkdir(download_dir)
                if not os.path.isdir(download_dir2):
                    os.mkdir(download_dir2)

                sftp.get(download_file,file_abs_path)
            cmd_result = "successfully download files from %s to [%s]" % (download_files,download_dir)
            result = "success"



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
