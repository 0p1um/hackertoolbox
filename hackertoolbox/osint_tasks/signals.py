from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from django_celery_results.models import TaskResult
from .models import (
    Job,
    ResultFromTask,
    Task,
    ResultGoogleSearch,
    ItemGoogleSearch,
    ResultPgpSearch,
    ItemPgpSearch,
    ResultAdvancedCrawler,
    ItemAdvancedCrawler,
    ResultCertificateTransparency,
    ItemCertificateTransparency,
    ResultDnsLookup,
    ItemDnsLookup,
    ResultSimpleCrawler,
    ItemSimpleCrawler,
    ResultShodanSearch,
    ItemShodanSearch,
)
from django_celery_beat.models import PeriodicTask
import json


# function to receive signals when new tasks are created and start tasks to do in celery daemon
@receiver([m2m_changed], sender=Job.tasks.through)
def job_save_handler(sender, instance, action, **kwargs):
    if action == "post_add":
        for task in instance.tasks.all():
            PeriodicTask.objects.filter(name=instance.name + "-" + task.name).delete()
        instance.create_periodic_task()


@receiver([pre_delete], sender=Job)
def job_del_handler(sender, instance, **kwargs):
    for task in instance.tasks.all():
        PeriodicTask.objects.filter(name=instance.name + "-" + task.name).delete()


# function to receive signals when result of task are created in database, in order to process them and creates results objects
@receiver([post_save], sender=TaskResult)
def taskresult_save_handler(sender, instance, **kwargs):
    content_type = instance.content_type
    content_encoding = instance.content_encoding
    task_id = instance.task_id
    task_name = instance.task_name
    task_args = instance.task_args
    task_kwargs = instance.task_kwargs
    result = instance.result
    status = instance.status
    date_done = instance.date_done
    # create specific task result, bellow for google_search
    if task_name == "google_search":
        result_json = json.loads(result)
        search_time = result_json["searchInformation"]["searchTime"]
        total_results = result_json["searchInformation"]["totalResults"]
        new_result = ResultGoogleSearch(
            content_type=content_type,
            content_encoding=content_encoding,
            task_id=task_id,
            task_name=task_name,
            task_args=task_args,
            task_kwargs=task_kwargs,
            result=result,
            status=status,
            date_done=date_done,
            search_time=search_time,
            total_results=total_results,
        )
        new_result.save()

        for item in result_json["items"]:
            gs_title = item["title"]
            gs_link = item["link"]
            gs_snippet = item["snippet"]
            new_item = ItemGoogleSearch(
                title=gs_title, link=gs_link, snippet=gs_snippet, result_gs=new_result
            )
            new_item.save()
    elif task_name == "pgp_search":
        result_json = json.loads(result)
        new_result = ResultPgpSearch(
            content_type=content_type,
            content_encoding=content_encoding,
            task_id=task_id,
            task_name=task_name,
            task_args=task_args,
            task_kwargs=task_kwargs,
            result=result,
            status=status,
            date_done=date_done,
        )
        new_result.save()
        for item in result_json["data"]:
            new_item = ItemPgpSearch(
                name=item["name"],
                email=item["email"],
                public_key_fingerprint=item["public_key_fingerprint"],
                result_pgps=new_result,
            )
            new_item.save()
    elif task_name == "advanced_crawler":
        result_json = json.loads(result)
        new_result = ResultAdvancedCrawler(
            content_type=content_type,
            content_encoding=content_encoding,
            task_id=task_id,
            task_name=task_name,
            task_args=task_args,
            task_kwargs=task_kwargs,
            result=result,
            status=status,
            date_done=date_done,
        )
        new_result.save()
        for item in result_json["data"]:
            url = item["url"]
            source_code = item["source_code"]
            links_list = item["links"]
            new_item = ItemAdvancedCrawler(
                url=url,
                source_code=source_code,
                links_list=links_list,
                result_ac=new_result,
            )
            new_item.save()
    elif task_name == "ct_search":
        result_json = json.loads(result)
        new_result = ResultCertificateTransparency(
            content_type=content_type,
            content_encoding=content_encoding,
            task_id=task_id,
            task_name=task_name,
            task_args=task_args,
            task_kwargs=task_kwargs,
            result=result,
            status=status,
            date_done=date_done,
        )
        new_result.save()
        for item in result_json["domains"]:
            new_item = ItemCertificateTransparency(domain=item, result_cts=new_result)
            new_item.save()
    elif task_name == "dns_lookup":
        result_json = json.loads(result)
        new_result = ResultDnsLookup(
            content_type=content_type,
            content_encoding=content_encoding,
            task_id=task_id,
            task_name=task_name,
            task_args=task_args,
            task_kwargs=task_kwargs,
            result=result,
            status=status,
            date_done=date_done,
        )
        new_result.save()
        for item in result_json["data"]:
            new_item = ItemDnsLookup(
                query=item["query"],
                record_type=item["record_type"],
                result=item["result"],
                result_dl=new_result,
            )
            new_item.save()
    elif task_name == "simple_crawler":
        result_json = json.loads(result)
        new_result = ResultSimpleCrawler(
            content_type=content_type,
            content_encoding=content_encoding,
            task_id=task_id,
            task_name=task_name,
            task_args=task_args,
            task_kwargs=task_kwargs,
            result=result,
            status=status,
            date_done=date_done,
        )
        new_result.save()
        for item in result_json["data"]:
            url = item["url"]
            source_code = item["source_code"]
            links_list = item["links"]
            new_item = ItemSimpleCrawler(
                url=url,
                source_code=source_code,
                links_list=links_list,
                result_sc=new_result,
            )
            new_item.save()
    elif task_name == "shodan_search":
        result_json = json.loads(result)
        new_result = ResultShodanSearch(
            content_type=content_type,
            content_encoding=content_encoding,
            task_id=task_id,
            task_name=task_name,
            task_args=task_args,
            task_kwargs=task_kwargs,
            result=result,
            status=status,
            date_done=date_done,
        )
        new_result.save()
        for item in result_json["res"]:
            ip = item["ip"]
            hostnames = item["hostnames"]
            domains = item["domains"]
            shodan_id = item["shodan_id"]
            location = item["location"]
            port = item["port"]
            banner = item["banner"]
            new_item = ItemShodanSearch(
                ip=ip,
                hostnames=hostnames,
                domains=domains,
                shodan_id=shodan_id,
                location=location,
                port=port,
                banner=banner,
                result_ss=new_result,
            )
            new_item.save()
    print("finish")
