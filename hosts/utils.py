import os,random
import sys
sys.path.append("/mnt/OathBreaker")
from OathBreaker import settings
from datetime import datetime

def json_date_handle(obj):
    if hasattr(obj,"isoformat"):
        return obj.strftime("%Y-%m-%d %H:%M:%S")


def handle_upload_file(request,file_obj):
    random_dir = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',10))
    upload_dir = "%s/%s" % (settings.FileUploadDir,request.user.id)
    upload_dir2 = "%s/%s" % (upload_dir,random_dir)

    if not os.path.isdir(settings.FileUploadDir):
	    os.mkdir(settings.FileUploadDir)

    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)
    if not os.path.isdir(upload_dir2):
        os.mkdir(upload_dir2)

    with open("%s/%s" % (upload_dir2,file_obj.name),"wb") as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    return "%s/%s" % (random_dir,file_obj.name)


def salt_handle_upload_file(request,file_obj):
    datetime_dir = datetime.now().strftime("%Y-%m-%d")
    upload_dir = "%s/%s" % (settings.FileUploadDir,datetime_dir)

    master_ip = settings.Salt_API['url'].split('/')[-2].split(':')[0]
    master_upload_path = "%s/%s" % (settings.Salt_File_Transfer_Upload_Abs_Path,datetime_dir)

    if not os.path.isdir(settings.FileUploadDir):
        os.mkdir(settings.FileUploadDir)

    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)

    if not os.path.isdir(settings.Salt_File_Transfer_Upload_Abs_Path):
        os.mkdir(settings.Salt_File_Transfer_Upload_Abs_Path)

    if not os.path.isdir(master_upload_path):
        os.mkdir(master_upload_path)

    with open("%s/%s" % (upload_dir,file_obj.name),"wb") as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    upload_file_abs_path = "%s/%s" % (upload_dir,file_obj.name)
    if os.path.isfile(upload_file_abs_path):
        os.system("scp -P 55210 %s root@%s:%s" % (upload_file_abs_path,master_ip,master_upload_path))

    return "%s/%s" % (datetime_dir,file_obj.name)


def salt_handle_download_file(username,master_ip,master_file_path,minion_ip):
    datetime_dir = datetime.now().strftime("%Y-%m-%d")
    download_dir = settings.Salt_File_Transfer_Download
    download_dir2 = "%s/%s" % (download_dir,username)
    download_dir3 = "%s/%s" % (download_dir2,datetime_dir)
    download_dir4 = "%s/%s" % (download_dir3,minion_ip)

    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)
    if not os.path.isdir(download_dir2):
        os.mkdir(download_dir2)
    if not os.path.isdir(download_dir3):
        os.mkdir(download_dir3)
    if not os.path.isdir(download_dir4):
        os.mkdir(download_dir4)

    result = os.system("scp -P 55210 root@%s:%s %s" % (master_ip,master_file_path,download_dir4))
    if result == 0:
        return True

def save_script_content(script_type,script_content):
    time_prefix = datetime.now().strftime("%Y%m%d%H%M%S")
    script_dir = "%s/%s" % (settings.ScriptUploadDir,script_type)
    master_ip = settings.Salt_API['url'].split('/')[-2].split(':')[0]
    script_root_path = settings.Salt_Script_Path + script_type
    script_relative_path = settings.Salt_Script_Relative_Path + script_type

    if not os.path.isdir(settings.ScriptUploadDir):
        os.mkdir(settings.ScriptUploadDir)

    if not os.path.isdir(script_dir):
        os.mkdir(script_dir)

    if script_type == "shell":
        shell_name = time_prefix + ".sh"
        shell_script_abs_path = "%s/%s" % (script_dir,shell_name)
        save_content2file(shell_script_abs_path,script_content)
        if os.path.isfile(shell_script_abs_path):
            os.system("scp -P 55210 %s root@%s:%s" % (shell_script_abs_path,master_ip,script_root_path))
	    script_salt_relative_path = script_relative_path + "/" + shell_script_abs_path.split("/")[-1]
            return script_salt_relative_path

    elif script_type == "batch":
        batch_name = time_prefix + ".bat"
        batch_script_abs_path = "%s/%s" % (script_dir,batch_name)
        save_content2file(batch_script_abs_path,script_content)
        if os.path.isfile(batch_script_abs_path):
            os.system("scp -P 55210 %s root@%s:%s" % (batch_script_abs_path,master_ip,script_root_path))
            script_salt_relative_path = script_relative_path + "/" + batch_script_abs_path.split("/")[-1]
            return script_salt_relative_path

    elif script_type == "python":
        python_name = time_prefix + ".py"
        python_script_abs_path = "%s/%s" % (script_dir,python_name)
        save_content2file(python_script_abs_path,script_content)
        if os.path.isfile(python_script_abs_path):
            os.system("scp -P 55210 %s root@%s:%s" % (python_script_abs_path,master_ip,script_root_path))
            script_salt_relative_path = script_relative_path + "/" + python_script_abs_path.split("/")[-1]
            return script_salt_relative_path

    elif script_type == "powershell":
        powershell_name = time_prefix + ".ps1"
        powershell_script_abs_path = "%s/%s" % (script_dir,powershell_name)
        save_content2file(powershell_script_abs_path,script_content)
        if os.path.isfile(powershell_script_abs_path):
            os.system("scp -P 55210 %s root@%s:%s" % (powershell_script_abs_path,master_ip,script_root_path))
            script_salt_relative_path = script_relative_path + "/" + powershell_script_abs_path.split("/")[-1]
            return script_salt_relative_path
    else:
        print "Wrong script type"


def save_content2file(file_path,file_content):
    f = file(file_path,"w+")
    f.writelines(file_content)
    f.flush()
    f.close()



def test_upload_file(file_name):
    random_dir = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',10))
    upload_dir = "%s/%s" % (settings.FileUploadDir,1)
    upload_dir2 = "%s/%s" % (upload_dir,random_dir)

    if not os.path.isdir(settings.FileUploadDir):
        os.mkdir(settings.FileUploadDir)

    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)
    if not os.path.isdir(upload_dir2):
        os.mkdir(upload_dir2)



#if __name__ == "__main__":
#    test_upload_file("haha.txt")
