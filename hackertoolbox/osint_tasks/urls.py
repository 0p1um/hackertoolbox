from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import GoogleSearchCreate, TasksListView, JobsListView, JobCreate, JobUpdate, JobDelete\
, ResultsListView, ResultDelete, ResultDetail, TaskDelete, PgpSearchCreate, AdvancedCrawlerCreate, ItemList, get_config, run_task_view,\
 GoogleSearchUpdate, AdvancedCrawlerUpdate, PgpSearchUpdate, CertificateTransparencyCreate, CertificateTransparencyUpdate, run_transform, \
 DnsLookupCreate, DnsLookupUpdate, SimpleCrawlerCreate, SimpleCrawlerUpdate, ShodanSearchCreate, ShodanSearchUpdate


urlpatterns = [
    path('', TemplateView.as_view(template_name="index_osint.html"), name='osint_home'),
    path('config/', get_config, name='config'),
    #jobs urls   
    path('jobs/', JobsListView.as_view(), name='jobs'),
    path('jobs/job_create/', JobCreate.as_view(), name='job_create'),
    path('jobs/<int:pk>/update/', JobUpdate.as_view(), name='job_update'), 
    path('jobs/<int:pk>/delete/', JobDelete.as_view(), name='job_delete'), 
    # items url
    path('items/', ItemList.as_view(), name='items'),
    path('items/transform/', run_transform, name='run_transform'),
    # results urls
    path('results/', ResultsListView.as_view(), name='results'),
    path('results/<int:pk>/delete/', ResultDelete.as_view(), name='osint_tasks_result_delete'), 
    path('results/<int:pk>/', ResultDetail.as_view(), name='osint_tasks_result_detail'), 
    # general tasks urls
    path('tasks/', TasksListView.as_view(), name='tasks'),
    path('tasks/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'), 
    path('tasks/<int:pk>/run_task/', run_task_view, name='run_task'),
    #google search tasks urls
    path('tasks/gs_create/', GoogleSearchCreate.as_view(), name='google_search_create'),
    path('tasks/<int:pk>/gs_update/', GoogleSearchUpdate.as_view(), name='google_search_update'), 
    # pgp tasks urls
    path('tasks/pgps_create/', PgpSearchCreate.as_view(), name='pgp_search_create'),
    path('tasks/<int:pk>/pgps_update/', PgpSearchUpdate.as_view(), name='pgp_search_update'), 
    # advanced crawler url
    path('tasks/advanced_crawler_create/', AdvancedCrawlerCreate.as_view(), name='advanced_crawler_create'),
    path('tasks/<int:pk>/ac_update/', AdvancedCrawlerUpdate.as_view(), name='advanced_crawler_update'), 
    # advanced crawler url
    path('tasks/ct_search_create/', CertificateTransparencyCreate.as_view(), name='certificate_transparency_create'),
    path('tasks/<int:pk>/ct_search_update/', CertificateTransparencyUpdate.as_view(), name='certificate_transparency_update'),     
    # dns lookup url
    path('tasks/dns_lookup_create/', DnsLookupCreate.as_view(), name='dns_lookup_create'),
    path('tasks/<int:pk>/dns_lookup_update/', DnsLookupUpdate.as_view(), name='dns_lookup_update'),     
    # simple crawler url
    path('tasks/simple_crawler_create/', SimpleCrawlerCreate.as_view(), name='simple_crawler_create'),
    path('tasks/<int:pk>/simple_crawler_update/', SimpleCrawlerUpdate.as_view(), name='simple_crawler_update'), 
    # shodan search url
    path('tasks/shodan_search_create/', ShodanSearchCreate.as_view(), name='shodan_search_create'),
    path('tasks/<int:pk>/shodan_search_update/', ShodanSearchUpdate.as_view(), name='shodan_search_update'), 
]
