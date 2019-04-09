"""megabase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from search.views import (
    SearchCreate,
    refresh_datasets,
    DatasetList,
    ResultList,
    DatasetDetail,
    ResultDetail,
    SearchList,
)
from django.views.generic import TemplateView


urlpatterns = [
    path("", DatasetList.as_view(), name="search_home"),
    path("search_create/", SearchCreate.as_view(), name="search_create"),
    path("result_list/", ResultList.as_view(), name="search_result_list"),
    path("search_list/", SearchList.as_view(), name="search_list"),
    path("dataset/<int:pk>/", DatasetDetail.as_view(), name="dataset_detail"),
    path("result/<int:pk>/", ResultDetail.as_view(), name="search_result_detail"),
    path("refresh_datasets/", refresh_datasets, name="refresh_datasets"),
]
