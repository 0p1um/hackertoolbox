from django.db import models
from django.conf import settings
from django.urls import reverse
import subprocess
from .tasks import search_in_dataset


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    date = models.CharField(max_length=15)
    cipher_format = models.CharField(max_length=255)
    compromised_data = models.TextField()
    description = models.TextField()
    path = models.FilePathField(allow_folders=True)

    def __str__(self):
        return self.name


class Search(models.Model):
    query = models.TextField()
    now = models.DateTimeField(auto_now=True)
    datasets = models.ManyToManyField(Dataset)
    all_datasets = models.BooleanField(default=False)

    def run(self):
        if self.all_datasets:
            for dataset in Dataset.objects.all():
                query = self.query
                dataset_path = dataset.path
                search_in_dataset.delay(query, dataset_path)
        else:
            for dataset in self.datasets.all():
                query = self.query
                dataset_path = dataset.path
                search_in_dataset.delay(query, dataset_path)

    def __str__(self):
        return str(self.now) + " - " + self.query

    def get_absolute_url(self):
        return reverse("search_home")


class Result(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)

    def __str__(self):
        return "Result: " + str(self.search)


class Item(models.Model):
    row = models.TextField()
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    def __str__(self):
        return self.row
