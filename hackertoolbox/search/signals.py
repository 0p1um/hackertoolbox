from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Search, Result, Item, Dataset
from django_celery_results.models import TaskResult
import json


#function to receive signals when new tasks are created and start tasks to do in celery daemon
@receiver([m2m_changed], sender=Search.datasets.through)
def search_save_handler(sender, instance, action, **kwargs):
    if action == 'post_add':
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

