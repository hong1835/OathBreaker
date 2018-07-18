from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


def jobs_script_mgr(request):
    # print "mgr request===>",request
    # print "mgr user id===>",request.user.id
    # user = request.user.id
    # script_list = models.Script.objects.filter(create_user_id=user)
    # return render(request, "jobs/jobs_script_mgr.html", {"script_list": script_list})

    user = request.user.id
    script_list = models.Script.objects.filter(create_user_id=user)
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




