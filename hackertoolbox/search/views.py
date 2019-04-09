from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from .models import Search, Result, Dataset
from os import listdir
import json
from django.http import HttpResponseRedirect
from django.conf import settings


class SearchCreate(CreateView):
    model = Search
    template_name = "search_generic_form.html"
    fields = "__all__"


class SearchList(ListView):
    template_name = "search_list.html"
    context_object_name = "all_search"

    def get_queryset(self):
        return Search.objects.all()


class DatasetList(ListView):
    template_name = "dataset_list.html"
    context_object_name = "all_dataset"

    def get_queryset(self):
        return Dataset.objects.all()


class DatasetDetail(DetailView):
    template_name = "dataset_detail.html"
    model = Dataset


class ResultDetail(DetailView):
    template_name = "search_result_detail.html"
    model = Result


class ResultList(ListView):
    template_name = "search_result_list.html"
    context_object_name = "all_result"

    def get_queryset(self):
        return Result.objects.all()


def refresh_datasets(request):
    for dir in listdir(settings.DATASETS_PATH):
        info_file = settings.DATASETS_PATH + "/" + dir + "/" + "info.json"
        dataset_path = settings.DATASETS_PATH + "/" + dir + "/"
        with open(info_file) as info_file:
            print(info_file)
            info = json.load(info_file)
        all_datasets = Dataset.objects.all()
        dataset = Dataset(
            name=info["name"],
            date=info["date"],
            cipher_format=info["format"],
            compromised_data=info["compromised_data"],
            description=info["description"],
            path=dataset_path,
        )
        if dataset.name not in [a.name for a in all_datasets]:
            dataset.save()
        print(info)
    return HttpResponseRedirect("/search/")
