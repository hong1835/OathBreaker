#_*_coding:utf-8_*_
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
from assets import models as assets_models
from hosts import models as hosts_models
from django.db.models import Q
from django.db import transaction
import json
from ast import  literal_eval
import datetime
from pytz import timezone
#from jobs.models import *
#sys.path.append(os.path.abspath("/mnt/OathBreaker/jobs"))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'OathBreaker.settings'
#django.setup()

def jobs_template_mgr(request):
    user = request.user.id
    template_list = models.Template.objects.filter((Q(create_user_id=user)  | Q(shared_with=user) & Q(is_delete=False))).distinct()
    page = request.GET.get("page",1)
    paginator = Paginator(template_list,10)
    try:
        templates = paginator.page(page)
    except PageNotAnInteger:
        templates = paginator.page(1)
    except EmptyPage:
        templates = paginator.page(paginator.num_pages)

    return render(request,"jobs/jobs_template_mgr.html", {"template_list":templates})

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

def jobs_history_mgr(request):
    user = request.user.id
    print "user==>",user
    history_list = models.History.objects.filter(template__create_user_id=user)
    print "history_list===>",history_list
    page = request.GET.get("page", 1)
    paginator = Paginator(history_list, 10)
    try:
        historys = paginator.page(page)
    except PageNotAnInteger:
        historys = paginator.page(1)
    except EmptyPage:
        historys = paginator.page(paginator.num_pages)
    return render(request,"jobs/jobs_history_mgr.html",{"history_list":historys})

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
        script_name_withSuffix = utils.addScriptSuffix(script_name,script_type)
        script_content = utils.get_script_content(script_type,script_name_withSuffix)
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


@login_required
def template_add(request):
    if request.method == "GET":
        # template_types_choice = {'template_types_choice': models.Template.template_types_choice}
        # business_unit = {"business_unit": tuple(assets_models.BusinessUnit.objects.all().values_list("name"))}
        context_text={}
        context_text["template_types_choice"] = models.Template.template_types_choice
        context_text["business_unit"] = tuple(assets_models.BusinessUnit.objects.all().values_list("name"))
        #print "template_types_choice===>",template_types_choice
        #print "business_unit===>",business_unit
        return render(request,"jobs/template_add.html",context_text)
    elif request.method == "POST":
        print "request POST===>",request.POST
        template_name = request.POST.get("template_name")
        if models.Template.objects.filter(name=template_name):
            return render(request, "jobs/template_add.html", {
                "template_fail": "Error.Already exists the same template name!"
            })
        else:
            template_type = utils.handle_template_type_choice_to_en(request.POST.get("template_type"))
            business_unit = request.POST.get("business_unit")
            busi_unit_obj = assets_models.BusinessUnit.objects.get(name=business_unit)
            template_comments = request.POST.get("template_comments")
            template_generator = utils.TemplateGen(request)
            res = template_generator.init_create(template_type,busi_unit_obj)
            return render(request,"jobs/template_add.html",{
                "template_success":"Successful!",

            })

def step_add(request):
    return HttpResponse("OK")


def add_template_script(request,templatestep_id):
    if request.method == "GET":
        user = request.user.id
        print "templatestep_id=++==>",templatestep_id
        script_list = models.Script.objects.filter(
            (Q(create_user_id=user) | Q(shared_with=user) & Q(is_delete=False))).distinct()

        if models.TemplateStep.objects.filter(id=templatestep_id) and models.TemplateStepScript.objects.filter(step_id=templatestep_id):
            TemplateStep_obj = models.TemplateStep.objects.get(id=templatestep_id)
            TemplateStepScript_obj = models.TemplateStepScript.objects.get(step_id=templatestep_id)
            script_name = (models.Script.objects.get(id=TemplateStepScript_obj.script_id)).scriptname
            script_type = (models.Script.objects.get(id=TemplateStepScript_obj.script_id)).script_type
            script_name_withSuffix = utils.addScriptSuffix(script_name, script_type)
            script_content = utils.get_script_content(script_type, script_name_withSuffix)
            parameters = TemplateStepScript_obj.parameter
            private_setting = TemplateStep_obj.private_setting
            target_machine_ids = str(TemplateStep_obj.target)
            print "target_machine_ids===>",target_machine_ids,type(target_machine_ids)
            target_machine_iplist = []
            if target_machine_ids not in ["NULL","None"]:
            #if target_machine_ids is not None:
                for host_id in literal_eval(target_machine_ids):
                    #print "host_id===>",host_id,type(host_id)
                    ip_addr = list(assets_models.Server.objects.filter(id=host_id).values_list("ip_addr", flat=True))
                    target_machine_iplist.append(ip_addr[0] + '\n')

            print "target_machine===>",target_machine_iplist
            return render(request,"jobs/template_script_edit.html",{"templatestep":TemplateStep_obj,
                                                                    "script_list":script_list,
                                                                    "parameter":parameters,
                                                                    "script_name":script_name,
                                                                    "script_content":script_content,
                                                                    "target_machine":target_machine_iplist})
        else:
            return render(request,"jobs/template_script_add.html", {"script_list": script_list,
                                                                        "templatestep_id":templatestep_id})

    elif request.method == "POST":
        print "add_template_script===>",request.POST
        print "templatestep_id==>",request.POST.get("templatestep_id")
        templatestep_obj = models.TemplateStep.objects.get(id=request.POST.get("templatestep_id"))
        template_id = templatestep_obj.template_id
        templatestep_obj.name = request.POST.get("step_script_name")
        templatestep_obj.description = request.POST.get("step_script_description")
        if(request.POST.getlist("target_machine[]")):
            templatestep_obj.private_setting = True
            templatestep_obj.target = request.POST.getlist("target_machine[]")
        templatestep_obj.save()

        if(models.TemplateStepScript.objects.filter(step_id=templatestep_id)):
            templatestepscript_obj = models.TemplateStepScript.objects.get(step_id=templatestep_id)
            templatestepscript_obj.parameter = request.POST.get("parameter")
            templatestepscript_obj.script_id = list(models.Script.objects.filter(scriptname=request.POST.get("selected_script")).values_list("id",flat=True))[0]
            templatestepscript_obj.save()
        else:
            templatestepscript_obj = models.TemplateStepScript(
                step_id = request.POST.get("templatestep_id"),
                parameter = request.POST.get("parameter"),
                script_id = list(models.Script.objects.filter(scriptname=request.POST.get("selected_script")).values_list("id",flat=True))[0]
            )
            templatestepscript_obj.save()
        html_ele = '''
                        Your step <<a href="/jobs/template_edit/%s/">%s</a>> has been updated successfully''' % (
            template_id, templatestep_obj.name)
        return HttpResponse(html_ele)



def add_template_text(request,templatestep_id):
    if request.method == "GET":
        print "templatestep_id===>",templatestep_id
        TemplateStep_obj = models.TemplateStep.objects.get(id=templatestep_id)
        if models.TemplateStep.objects.filter(id=templatestep_id) and models.TemplateStepText.objects.filter(step_id=templatestep_id):
            print "templatestep_name",TemplateStep_obj.name
            TemplateStepText_obj = models.TemplateStepText.objects.get(step_id=templatestep_id)
            print "templatesteptext_desc",TemplateStepText_obj.description
            return render(request,"jobs/template_text_edit.html",{"templatestep_obj":TemplateStep_obj,
                                                                 "templatesteptext_obj":TemplateStepText_obj})
        else:
            return render(request,"jobs/template_text_edit.html",{"templatestep_obj":TemplateStep_obj})

    elif request.method == "POST":
        print "edit_templatesteptext===>",request.POST
        step_text_name = request.POST.get("step_text_name")
        step_text_description = request.POST.get("step_text_description")
        templatestep_obj = models.TemplateStep.objects.get(id=request.POST.get("templatestep_id"))
        template_id = templatestep_obj.template_id
        templatestep_obj.name = request.POST.get("step_text_name")
        templatestep_obj.save()
        if(models.TemplateStepText.objects.filter(step_id=templatestep_id)):
            templatesteptext_obj = models.TemplateStepText.objects.get(step_id=templatestep_id)
            templatesteptext_obj.description = request.POST.get("step_text_description")
            templatesteptext_obj.save()
        else:
            templatesteptext_obj = models.TemplateStepText(
                step_id = request.POST.get("templatestep_id"),
                description = request.POST.get("step_text_description")
            )
            templatesteptext_obj.save()
        html_ele = '''
                        Your step <<a href="/jobs/template_edit/%s/">%s</a>> has been updated successfully''' % (
            template_id, templatestep_obj.name)
        return HttpResponse(html_ele)


def template_get_script(request):
    print request.POST
    name = request.POST.get("scriptname")
    script_obj = models.Script.objects.get(scriptname=name)
    script_name = utils.addScriptSuffix(name,script_obj.script_type)
    script_content = utils.get_script_content(script_obj.script_type, script_name)
    return HttpResponse(script_content)


def template_edit(request,template_id):
    err_msg = ""
    try:
        template_obj = models.Template.objects.get(id=template_id)
    except ObjectDoesNotExist,e:
        err_msg = str(e)
    if request.method == "GET":
        template_type = template_obj.template_type
        template_type = utils.handle_template_type_choice_to_cn(template_type)
        business_unit = template_obj.business_unit
        template_steps = models.TemplateStep.objects.filter(Q(template_id=template_id) & Q(is_delete=0)).order_by("order")
        target_machine_ids = str(template_obj.target)
        target_machine_iplist = []
        print "target_machine_ids===>",target_machine_ids
        if target_machine_ids not in ["NULL","None"]:
            for host_id in literal_eval(target_machine_ids):
                print "host_id===>", host_id, type(host_id)
                ip_addr = list(assets_models.Server.objects.filter(id=host_id).values_list("ip_addr", flat=True))
                target_machine_iplist.append(ip_addr[0])
        #print "template_steps===>",template_steps
        return render(request,"jobs/template_edit.html",{"template":template_obj,
                                                       "template_type":template_type,
                                                         "business_unit":business_unit,
                                                         "template_types_choice":models.Template.template_types_choice,
                                                         "b_unit":tuple(assets_models.BusinessUnit.objects.all().values_list("name")),
                                                         "template_steps":template_steps,
                                                         "target_machine":target_machine_iplist})
    elif request.method == "POST":
        script_name = request.POST.get("script_name")
        script_type = request.POST.get("script_type")
        script_content = request.POST.get("script_content_shell")
        print "update script_name===>",script_name
        print "update script_type===>",script_type
        print "update script_content==>",script_content
        script_stored_path = utils.save_script_content_v2(script_name, script_type, script_content)
        script_updater = utils.ScriptGen(request, script_stored_path["abs_path"], script_stored_path["rel_path"])
        res = script_updater.update(template_obj)
        return render(request, "jobs/script_edit.html", {
            "script_success": "Successful!"
        })


def template_step_add(request):
    step_type_dict = {
        1: "execute_script",
        2: "push_file",
        3: "pull_file",
        4: "text_step"
    }
    print "template_step_add--->",request.POST
    template_id = request.POST.get("template_id")
    templateStep_obj = models.TemplateStep(
        template_id=request.POST.get("template_id"),
        name=utils.handle_step_type_to_cn(step_type_dict[int(request.POST.get("step_type"))]),
        step_type=step_type_dict[int(request.POST.get("step_type"))],
        order=request.POST.get("step_order")
    )
    templateStep_obj.save()

    exist_steps_count = models.TemplateStep.objects.filter(Q(template_id=template_id) & Q(is_delete=0)).count()
    exist_steps_ids = list(models.TemplateStep.objects.filter(Q(template_id=template_id) & Q(is_delete=0)).values_list("id",
                                                                                                                  flat=True))

    #sort
    if request.POST.get("step_order") == exist_steps_count -1:
        for i in range(exist_steps_count):
            templatestep_obj = models.TemplateStep.objects.get(id=exist_steps_ids[i])
            templatestep_obj.order = i
            templatestep_obj.save()

    else:
        new_steps_ids = exist_steps_ids[:len(exist_steps_ids)-1]
        print type(new_steps_ids)
        print "new_steps_ids===>",new_steps_ids
        last_templatestep_id = exist_steps_ids[-1]
        print "list_templatestep_id===>",last_templatestep_id,type(last_templatestep_id)
        insert_index = int(request.POST.get("step_order"))
        print "step_order===>",request.POST.get("step_order"),type(insert_index)

        new_steps_ids.insert(insert_index,last_templatestep_id)
        print "new_steps_ids2===>",new_steps_ids
        for i in range(exist_steps_count):
            print "i===>",i
            print "new_step_id===>",new_steps_ids[i]
            templatestep_obj = models.TemplateStep.objects.get(id=new_steps_ids[i])
            templatestep_obj.order = i
            templatestep_obj.save()
    return HttpResponse("OK")


def step_delete(request):
    print "step_delete===>",request.POST
    step_id = request.POST.get("step_id")
    template_id = request.POST.get("template_id")
    if models.TemplateStep.objects.filter(id=step_id):
        templatestep_obj = models.TemplateStep.objects.get(id=step_id)
        templatestep_obj.is_delete = 1
        templatestep_obj.save()

        exist_steps_count = models.TemplateStep.objects.filter(Q(template_id=template_id) & Q(is_delete=0)).count()
        exist_steps_ids = models.TemplateStep.objects.filter(Q(template_id=template_id) & Q(is_delete=0)).values_list("id",flat=True)
        for i in range(exist_steps_count):
            templatestep_obj = models.TemplateStep.objects.get(id=exist_steps_ids[i])
            templatestep_obj.order = i
            templatestep_obj.save()



        return HttpResponse("OK")
    else:
        return HttpResponse("No")



def global_settings(request,template_id):
    print "template_id--->",template_id
    template_obj = models.Template.objects.get(id=template_id)
    target_machine_ids = str(template_obj.target)
    target_machine_iplist = []
    if target_machine_ids not in ["NULL","None"]:
        for host_id in literal_eval(target_machine_ids):
            print "host_id===>", host_id, type(host_id)
            ip_addr = list(assets_models.Server.objects.filter(id=host_id).values_list("ip_addr", flat=True))
            target_machine_iplist.append(ip_addr[0] + '\n')
    return render(request,"jobs/template_globalsettings.html",{"template_id":template_id,
                                                               "templateobj":template_obj,
                                                               "target_machine":target_machine_iplist})


def get_iplist(request):
    print request.POST
    selected_hosts = request.POST.getlist("selected_hosts[]")
    selected_iplist = []
    for host_id in selected_hosts:
        ip_addr = list(assets_models.Server.objects.filter(id=host_id).values_list("ip_addr",flat=True))
        selected_iplist.append(ip_addr[0]+'\n')
    print selected_iplist
    return HttpResponse(selected_iplist)


def template_globalsettings(request,template_id):
    print "template_id===>",template_id
    print request.POST
    execute_mode = request.POST.get("mode")
    ip_list = request.POST.get("ip_list")
    ip_list = ip_list.strip("\r\n")
    #print "ip_list==>",ip_list,type(ip_list)
    host_id_list = []
    if ip_list:
        ip_list = ip_list.split("\r\n")
        for ip in ip_list:
            host_id = list(assets_models.Server.objects.filter(ip_addr=ip).values_list("id",flat=True))
            print "host_id===>",host_id,type(host_id)
            host_id_list.append(host_id[0])

    template_obj = models.Template.objects.get(id=template_id)
    template_obj.execute_mode = execute_mode
    template_obj.target = host_id_list
    template_obj.save()
    print "host_id_list===>",host_id_list
    return HttpResponseRedirect("/jobs/template_edit/%s" % template_id)


def clear_settings(request):
    print request.POST
    template_id = request.POST.get("template_id")
    template_obj = models.Template.objects.get(id=template_id)
    template_obj.execute_mode = "single"
    template_obj.target = "NULL"
    template_obj.save()
    templatestep_ids = list(models.TemplateStep.objects.filter(Q(template_id=template_id) & Q(is_delete=0)).values_list("id",flat=True))
    print "templatestep_ids===>",templatestep_ids
    for templatestep_id in templatestep_ids:
        print "templatesteps_id==>",templatestep_id
        templatestep_obj = models.TemplateStep.objects.get(id=templatestep_id)
        templatestep_obj.target = "NULL"
        templatestep_obj.private_setting = 0
        templatestep_obj.save()
        print "step_type--->",templatestep_obj.step_type
        if templatestep_obj.step_type == "execute_script":
            templatestepscript_obj = models.TemplateStepScript.objects.get(step_id=templatestep_id)
            templatestepscript_obj.parameter = ""
            templatestepscript_obj.save()
    return HttpResponseRedirect("/jobs/template_edit/%s" % template_id)


def prepare_job(request,template_id):
    print "prepare_job===>",request.method
    print "template_id===>",template_id
    history = models.History(
        run_user_id= request.user.id,
        template_id = template_id
    )
    history.save()
    history_id = history.id
    print "history_id===>",history_id
    history_obj = models.History.objects.get(id=history_id)

    check_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    template_steps = models.TemplateStep.objects.filter(Q(template_id=template_id) & Q(is_delete=0)).order_by("order")

    for template_step in template_steps:
        historystep_obj = models.HistoryStep(
            history_id = history_id,
            templatestep_id = template_step.id
        )
        historystep_obj.save()

    historysteps_obj = models.HistoryStep.objects.filter(Q(history_id=history_id) & Q(templatestep__template_id=template_id))

    return render(request,"jobs/history_ready.html",{"history":history_obj,
                                                     "template_steps":historysteps_obj,
                                                     "check_id":check_id})


def submit_Job(request):
    if request.method == "POST":
        print "submit_Job===>",request.POST
        template_id = request.POST.get("template_id")
        history = models.History(
            run_user_id=request.user.id,
            template_id=template_id
        )
        history.save()
        history_id = history.id
        print "history_id===>", history_id
        history_obj = models.History.objects.get(id=history_id)

        check_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        template_steps = models.TemplateStep.objects.filter(Q(template_id=template_id) & Q(is_delete=0)).order_by("order")

        for template_step in template_steps:
            historystep_obj = models.HistoryStep(
                history_id=history_id,
                templatestep_id=template_step.id
            )
            historystep_obj.save()

        historysteps_obj = models.HistoryStep.objects.filter(
            Q(history_id=history_id) & Q(templatestep__template_id=template_id))

        return render(request,"jobs/history_ready.html",{"history":history_obj,
                                                         "template_steps":historysteps_obj,
                                                         "check_id":check_id})

    else:
        return HttpResponse("OK")

    #return HttpResponse("OK")


def show_history(request,history_id,template_id):
    history_obj = models.History.objects.get(id=history_id)
    #template_steps = models.TemplateStep.objects.filter(Q(template_id=template_id) & Q(is_delete=0)).order_by("order")


    historysteps_obj = models.HistoryStep.objects.filter(Q(history_id=history_id) & Q(templatestep__template_id=template_id))

    targets = history_obj.template.target
    target_list = []
    if targets not in ["NULL","None"]:
        for target in literal_eval(targets):
            target_list.append(target)
    return render(request,"jobs/history_show.html",{"history":history_obj,
                                                    "template_steps":historysteps_obj,
                                                    "target_machine":target_list})



def history_step_execute(request):
    print "history_step_execute===>",request.POST
    history_step_id = request.POST.get("history_step_id")
    jobrun_obj = utils.RunJobStep(request)
    res = jobrun_obj.handle()
    print "----res--->",res

    return HttpResponse(json.dumps(res))