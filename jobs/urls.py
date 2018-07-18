from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^jobs_instance_mgr/$',views.jobs_instance_mgr,name="jobs_instance_mgr"),
    url(r'^jobs_script_mgr/$',views.jobs_script_mgr,name="jobs_script_mgr"),
    url(r'^jobs_schedule_mgr/$',views.jobs_schedule_mgr,name="jobs_schedule_mgr"),
    url(r'^script_add/$',views.script_add,name="script_add"),
]

