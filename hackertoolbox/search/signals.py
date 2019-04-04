from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Search, Result, Item, Dataset
from django_celery_results.models import TaskResult
import json


@receiver([post_save], sender=Search)
def search_save_handler(sender, instance, created, update_fields, **kwargs):
    print(instance.query)
    instance.run()

@receiver([post_save], sender=TaskResult)
def search_dataset_result(sender, instance, **kwargs):
    print(instance.result)
    print(instance.task_name)
    if 'search_in_dataset' not in instance.task_name:
        return
    print(instance.task_args[0])
    search = Search.objects.filter(query=instance.task_args[0]).latest('query')
    try:
        result = Result.objects.latest(search=search)
    except:
        result = Result(search=search)
        result.save()
    rows = json.loads(instance.result)
    dataset = Dataset.objects.filter(path=instance.task_args[1]).latest('path')
    for row in rows:
        item = Item(row=row, result=result, dataset=dataset)
        item.save()

