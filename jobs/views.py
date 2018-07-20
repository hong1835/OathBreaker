from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.
import django
import sys
sys.path.append('/mnt/OathBreaker/jobs')
import utils
import models
#from jobs.models import *
#sys.path.append(os.path.abspath("/mnt/OathBreaker/jobs"))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'OathBreaker.settings'
#django.setup()

def jobs_instance_mgr(request):
    return render(request,"jobs/jobs_instance_mgr.html")

@login_required
def jobs_script_mgr(request):
    # print "mgr request===>",request
    # print "mgr user id===>",request.user.id
    # user = request.user.id
    # script_list = models.Script.objects.filter(create_user_id=user)
    # return render(request, "jobs/jobs_script_mgr.html", {"script_list": script_list})

    user = request.user.id
    script_list = models.Script.objects.filter(create_user_id=user,is_delete=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(script_list, 10)
    try:
        scripts = paginator.page(page)
    except PageNotAnInteger:
        scripts = paginator.page(1)
    except EmptyPage:
        scripts = paginator.page(paginator.num_pages)

    return render(request, 'jobs/jobs_script_mgr.html', {"script_list": scripts})

def jobs_schedule_mgr(request):
    return HttpResponse("job schedule mgr")

@login_required
def script_add(request):
    if request.method == "GET":
        return render(request,"jobs/script_add.html")
    elif request.method == "POST":
        print "request POST===>",request.POST
        script_name = request.POST.get("script_name")
        if models.Script.objects.filter(scriptname=script_name):
            return render(request, "jobs/script_add.html", {
                "script_fail": "Error.Already exists the same script name!"
            })
        else:
            scription_description = request.POST.get("script_description")
            script_type = request.POST.get("script_type")
            script_content = request.POST.get("script_content_shell")
            c_user = request.user.id
            script_stored_path = utils.save_script_content_v2(script_name,script_type,script_content)
            script_generator = utils.ScriptGen(request,script_stored_path["abs_path"],script_stored_path["rel_path"])
            res = script_generator.create()
            return render(request,"jobs/script_add.html",{
                "script_success":"Successful!"
            })

@login_required
def script_delete(request):
    print request.POST
    print request.POST.get("scriptname")
    script_name = request.POST.get("scriptname")
    if models.Script.objects.filter(scriptname=script_name):
        models.Script.objects.filter(scriptname=script_name).update(is_delete=True)
        return HttpResponse("OK")

@login_required
def script_edit(request,script_id):
    err_msg = ""
    try:
        script_obj = models.Script.objects.get(id=script_id)
    except ObjectDoesNotExist,e:
        err_msg = str(e)
    if request.method == "GET":
        script_type = script_obj.script_type
        script_name = script_obj.scriptname
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
        script_content = utils.get_script_content(script_type,script_name)
        return render(request,"jobs/script_edit.html",{"script":script_obj,
                                                       "script_content":script_content})
    elif request.method == "POST":
        script_name = request.POST.get("script_name")
        script_type = request.POST.get("script_type")
        script_content = request.POST.get("script_content_shell")
        print "update script_name===>",script_name
        print "update script_type===>",script_type
        print "update script_content==>",script_content
        script_stored_path = utils.save_script_content_v2(script_name, script_type, script_content)
        script_updater = utils.ScriptGen(request, script_stored_path["abs_path"], script_stored_path["rel_path"])
        res = script_updater.update(script_id)
        return render(request, "jobs/script_edit.html", {
            "script_success": "Successful!"
        })

