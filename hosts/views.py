#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import models
import task,utils
import json
from assets import tables
from hosts import admin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


@login_required
def hosts_index(request):
    return render(request,"hosts/dashboard.html")


@login_required
def hosts_mgr(request):
    selected_gid = request.GET.get("selected_gid")
    if selected_gid:
        host_list = models.BindHostToUser.objects.filter(host_groups__id=selected_gid)
    else:
        host_list = request.user.bind_hosts.select_related()
    return render(request,"hosts/hosts_mgr.html",{"host_list":host_list})

@login_required
def multi_cmd(request):
    return render(request, "hosts/multi_cmd.html")

@login_required
def multi_script(request):
    return render(request,"hosts/multi_scripts.html")

@login_required
def multi_file_transfer(request):
    return render(request,"hosts/multi_file_transfer.html")

@csrf_exempt
@login_required
def file_upload(request):
    filename = request.FILES.get("filename")
    print "--->",request.POST,"--->",filename,"---->",filename.name
    file_path = utils.handle_upload_file(request,filename)

    return HttpResponse(json.dumps({"uploaded_file_path":file_path}))

@login_required
def submit_task(request):
    print "--submit task---",request.POST
    task_obj = task.Task(request)
    res = task_obj.handle()
    return HttpResponse(json.dumps(res))

@login_required
def get_task_result(request):
    task_obj = task.Task(request)
    res = task_obj.get_task_result()
    print "res---task---",res
    return HttpResponse(json.dumps(res,default=utils.json_date_handle))

# @login_required
# def get_operation_audit(request):
#     task_obj = task.Task(request)
#     res = task_obj.get_operation_audit()
#     print "res---task---",res
#     return HttpResponse(json.dumps(res,default=utils.json_date_handle))


# @login_required
# def operation_audit(request):
#     return render(request,"hosts/operation_audit.html")


@login_required
def operation_audit(request):
    '''行为审计'''

    auditlog_objs = tables.table_filter(request, admin.OperationAuditLogAdmin, models.OperationAuditLog)
    # asset_obj_list = models.Asset.objects.all()
    #print("asset_obj_list:", asset_obj_list)
    order_res = tables.get_orderby(request, auditlog_objs, admin.OperationAuditLogAdmin)
    # print('----->',order_res)
    paginator = Paginator(order_res[0], admin.OperationAuditLogAdmin.list_per_page)


    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    table_obj = tables.TableHandler(request,
                                    models.OperationAuditLog,
                                    admin.OperationAuditLogAdmin,
                                    objs,
                                    order_res
                                    )


    return render(request,'hosts/operation_audit.html',{'table_obj': table_obj,
                                                  'paginator': paginator})


def submit_ips(request):
    print "---ip list---",request.POST
    task_obj = task.Task(request)
    res = task_obj.handle()
    return HttpResponse(json.dumps(res))
