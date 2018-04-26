from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$',views.hosts_index,name="hosts"),
    url(r'^hosts_mgr/$',views.hosts_mgr,name="hosts_mgr"),
    url(r'^multi_cmd/$',views.multi_cmd,name="multi_cmd"),
    url(r'^submit_task/$',views.submit_task,name="submit_task"),
    url(r'^get_task_result/$',views.get_task_result,name="get_task_result"),
    url(r'^multi_file_transfer/$',views.multi_file_transfer,name="multi_file_transfer"),
    url(r'^file_upload/$',views.file_upload,name="file_upload"),
    url(r'^operation_audit/$',views.operation_audit,name="operation_audit"),
    url(r'^get_operation_audit/$',views.get_operation_audit,name="get_operation_audit"),
]
