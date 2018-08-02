from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^jobs_instance_mgr/$',views.jobs_instance_mgr,name="jobs_instance_mgr"),
    url(r'^jobs_script_mgr/$',views.jobs_script_mgr,name="jobs_script_mgr"),
    url(r'^jobs_schedule_mgr/$',views.jobs_schedule_mgr,name="jobs_schedule_mgr"),
    url(r'^script_add/$',views.script_add,name="script_add"),
    url(r'^script_delete/$',views.script_delete,name="script_delete"),
    url(r'^script_edit/(\d+)/$',views.script_edit,name="script_edit"),
    url(r'^script_authorized/$',views.script_authorized,name="script_authorized"),
    url(r'^modify_authorized/$',views.modify_authorized,name="modify_authorized"),
    url(r'^search_script/$',views.search_script,name="search_script")
]

