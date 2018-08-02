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
from hosts import models as hosts_models
from django.db.models import Q
import json
from ast import  literal_eval
import datetime
from pytz import timezone
#from jobs.models import *
#sys.path.append(os.path.abspath("/mnt/OathBreaker/jobs"))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'OathBreaker.settings'
#django.setup()

def jobs_instance_mgr(request):
    return render(request,"jobs/jobs_instance_mgr.html")

@login_required
def jobs_script_mgr(request):
    user = request.user.id
    script_list = models.Script.objects.filter((Q(create_user_id=user)  | Q(shared_with=user) & Q(is_delete=False))).distinct()
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
        print "request user id===>",request.user.id
        create_user = list(models.Script.objects.filter(scriptname=script_name).values_list("create_user_id",flat=True))
        if request.user.id != create_user[0]:
            print "You are not the owner of the script, you cannot delete it"
            return HttpResponse("You are not the owner of the script, you cannot delete it")
        else:
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


@login_required
def script_authorized(request):
    selected_scripts = request.POST.getlist("selected_scripts[]")
    all_users = list(hosts_models.UserProfile.objects.all().values_list("id",flat=True))
    all_users.remove(request.user.id)
    print "===>all users",all_users
    result_list = []
    for selected_script in selected_scripts:
        script_info = {}
        script_info["scriptname"] = selected_script
        user_list = []
        authorized_list = []
        for user in all_users:
            username = list(hosts_models.UserProfile.objects.filter(id=user).values_list("name",flat=True))
            username = username[0]
            result_3 = models.Script.objects.filter(scriptname=selected_script,shared_with__name=username)
            print "--->result3:",result_3
            user_list.append(username)
            if result_3:
                authorized_list.append(1)
            else:
                authorized_list.append(0)
        script_info["userinfo"] = user_list
        script_info["authorizedinfo"] = authorized_list
        result_list.append(script_info)
    print "---<",result_list
    return HttpResponse(json.dumps(result_list))


@login_required
def modify_authorized(request):
    print request.POST
    print request.POST.get("result")
    print "getlist===>",request.POST.getlist("result")[0]
    result_list = literal_eval(request.POST.getlist("result")[0])
    for result in result_list:
        print "result===>",result
        print type(result)
        scriptname = result["scriptname"]
        userlist = result["userinfo"]
        authlist = result["authorizedinfo"]
        script_id = list(models.Script.objects.filter(scriptname=scriptname).values_list("id",flat=True))
        print "script_id==>",script_id[0]
        for i in range(len(userlist)):
            user_name = userlist[i]
            user_id = (list(hosts_models.UserProfile.objects.filter(name=user_name).values_list("id",flat=True)))[0]
            auth_id = authlist[i]
            print "user_id====>",user_id
            print "auth_id====>",auth_id
            if auth_id:
                res = models.Script.objects.filter(scriptname=scriptname,shared_with__name=user_name)
                print res
                if models.Script.objects.filter(scriptname=scriptname,shared_with__name=user_name):
                    print "already exists"
                else:
                    script_obj = models.Script.objects.get(id=script_id[0])
                    user_obj = hosts_models.UserProfile.objects.get(id=user_id)
                    script_obj.shared_with.add(user_obj)
            else:
                if models.Script.objects.filter(scriptname=scriptname,shared_with__name=user_name):
                    script_obj = models.Script.objects.get(id=script_id[0])
                    print "script_obj===>", script_obj
                    user_obj = hosts_models.UserProfile.objects.get(id=user_id)
                    print "user_obj===>", user_obj
                    script_obj.shared_with.remove(user_obj)
                else:
                    print "does not exist"


    return HttpResponse("OK")


@login_required
def search_script(request):
    print request.POST
    search_name = request.POST.get("script_manage_name")
    search_user = request.POST.get("script_manage_create_user")
    search_from = request.POST.get("script_manage_created_from")
    search_to = request.POST.get("script_manage_created_to")
    if search_from:
        search_from_obj = datetime.datetime.strptime(search_from,"%Y-%m-%d")
        search_from_obj_utc = search_from_obj.replace(tzinfo=timezone("UTC"))
    else:
        search_from_obj = datetime.datetime.strptime("1970-01-01", "%Y-%m-%d")
        search_from_obj_utc = search_from_obj.replace(tzinfo=timezone("UTC"))

    if search_to:
        search_to_obj = datetime.datetime.strptime(search_to,"%Y-%m-%d")
        search_to_obj_utc = search_to_obj.replace(tzinfo=timezone("UTC"))
    else:
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1))
        tomorrow = tomorrow.strftime("%Y-%m-%d")
        search_to_obj = datetime.datetime.strptime(tomorrow, "%Y-%m-%d")
        search_to_obj_utc = search_to_obj.replace(tzinfo=timezone("UTC"))
    script_list =  models.Script.objects.filter( Q(scriptname__icontains=search_name) & Q(create_user__name__icontains=search_user) & Q(create_date__gte=search_from_obj_utc) & Q(create_date__lte=search_to_obj_utc) & Q(is_delete=0))
    print "script_list===>",script_list
    page = request.GET.get('page', 1)
    paginator = Paginator(script_list, 10)
    try:
        scripts = paginator.page(page)
    except PageNotAnInteger:
        scripts = paginator.page(1)
    except EmptyPage:
        scripts = paginator.page(paginator.num_pages)
    return render(request, 'jobs/jobs_script_mgr.html', {"script_list": scripts})





