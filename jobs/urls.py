from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^jobs_template_mgr/$',views.jobs_template_mgr,name="jobs_template_mgr"),
    url(r'^jobs_script_mgr/$',views.jobs_script_mgr,name="jobs_script_mgr"),
    url(r'^jobs_schedule_mgr/$',views.jobs_schedule_mgr,name="jobs_schedule_mgr"),
    url(r'^jobs_history_mgr/$',views.jobs_history_mgr,name="jobs_history_mgr"),
    url(r'^script_add/$',views.script_add,name="script_add"),
    url(r'^script_delete/$',views.script_delete,name="script_delete"),
    url(r'^script_edit/(\d+)/$',views.script_edit,name="script_edit"),
    url(r'^script_authorized/$',views.script_authorized,name="script_authorized"),
    url(r'^modify_authorized/$',views.modify_authorized,name="modify_authorized"),
    url(r'^search_script/$',views.search_script,name="search_script"),
    url(r'^template_add/$',views.template_add,name="template_add"),
    url(r'^step_add/$',views.step_add,name="step_add"),
    url(r'^add_template_script/(\d+)/$',views.add_template_script,name="add_template_script"),
    #url(r'^add_template_script/$',views.add_template_script,name="add_template_script"),
    url(r'^add_template_text/(\d+)/$',views.add_template_text,name="add_template_text"),
    url(r'^template_get_script/$',views.template_get_script,name="template_get_script"),
    url(r'^template_edit/(\d+)/$',views.template_edit,name="template_edit"),
    url(r'^template_step_add/$',views.template_step_add,name="template_step_add"),
    #url(r'^template_script_edit/$',views.template_script_edit,name="template_script_edit"),
    url(r'^step_delete/$',views.step_delete,name="step_delete"),
    url(r'^global_settings/(\d+)/$',views.global_settings,name="global_settings"),
    url(r'^get_iplist/$',views.get_iplist,name="get_iplist"),
    url(r'^template_globalsettings/(\d+)/$',views.template_globalsettings,name="template_globalsettings"),
    url(r'^clear_settings/$',views.clear_settings,name="clear_settings"),
    url(r'^prepare_job/(\d+)/$',views.prepare_job,name="prepare_job"),
    url(r'^show_history/(\d+)/(\d+)/$',views.show_history,name="show_history"),
    url(r'^history_step_execute/$',views.history_step_execute,name="history_step_execute"),
    url(r'^submit_Job/$',views.submit_Job,name="submit_Job"),
    url(r'^show_result/(\d+)/$',views.show_result,name="show_result")
]

