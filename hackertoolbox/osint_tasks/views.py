from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import (
    Task,
    GoogleSearch,
    Job,
    ResultFromTask,
    PgpSearch,
    Item,
    AdvancedCrawler,
    CertificateTransparency,
    DnsLookup,
    SimpleCrawler,
    ShodanSearch,
)
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ConfigForm
from .tasks import ct_search, advanced_crawler, pgp_search, google_search, dns_lookup
from django.conf import settings


# view function to handle configuration of modules page (such as api keys ect ...)
def get_config(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ConfigForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            with open(settings.TASKS_CONF_FILE, "w") as file:
                file.write("GOOGLE_API=" + form.cleaned_data["google_api"] + "\n")
                file.write("GOOGLE_CSE_ID=" + form.cleaned_data["google_cse_id"] + "\n")
                file.write(
                    "SHODAN_API_KEY=" + form.cleaned_data["shodan_api_key"] + "\n"
                )
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        with open(settings.TASKS_CONF_FILE, "r") as file:
            for line in file:
                if "GOOGLE_API" in line:
                    google_api = line.replace("GOOGLE_API=", "")
                elif "GOOGLE_CSE_ID" in line:
                    google_cse_id = line.replace("GOOGLE_CSE_ID=", "")
                elif "SHODAN_API_KEY" in line:
                    shodan_api_key = line.replace("SHODAN_API_KEY=", "")
        form = ConfigForm(
            initial={
                "google_api": google_api,
                "google_cse_id": google_cse_id,
                "shodan_api_key": shodan_api_key,
            }
        )

    return render(request, "generic_form.html", {"form": form})


# view to handler the 'run now' functionality, allowing to the user to run a task directly (see the run function in tasks models)
def run_task_view(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.run()
    return render(request, "tasks_list.html", {"all_tasks": Task.objects.all()})


# view to handle task to launch from items gathered
def run_transform(request):
    transform = request.GET.get("transform")
    data = request.GET.get("data")
    if transform == "ct_search":
        print(data)
        ct_search.delay(data)
    elif transform == "advanced_crawler":
        if "http://" != data[0:6] or "https://" != data[0:7]:
            data = "http://" + data
        print(data)
        advanced_crawler.delay(data)
    elif transform == "google_search":
        print(data)
        google_search.delay(data)
    elif transform == "pgp_search":
        print(data)
        pgp_search.delay(data)
    elif transform == "dns_lookup":
        print(data)
        pgp_search.delay(data, type_ALL=True)
    else:
        pass
    return render(request, "items_list.html", {"all_items": Item.objects.all()})


class TasksListView(ListView):
    template_name = "tasks_list.html"
    context_object_name = "all_tasks"

    def get_queryset(self):
        return Task.objects.all()


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy("tasks")
    template_name = "confirm_delete.html"


class JobsListView(ListView):
    template_name = "jobs_list.html"
    context_object_name = "all_jobs"

    def get_queryset(self):
        return Job.objects.all()


class JobCreate(CreateView):
    model = Job
    fields = "__all__"
    template_name = "generic_form.html"


class JobUpdate(UpdateView):
    model = Job
    fields = "__all__"
    template_name = "generic_form.html"


class JobDelete(DeleteView):
    model = Job
    success_url = reverse_lazy("jobs")
    template_name = "confirm_delete.html"


class ResultsListView(ListView):
    template_name = "results_list.html"
    context_object_name = "all_results"

    def get_queryset(
        self
    ):
        return ResultFromTask.objects.all()


class ResultDelete(DeleteView):
    model = ResultFromTask
    success_url = reverse_lazy("results")
    template_name = "confirm_delete.html"


class ResultDetail(DetailView):
    model = ResultFromTask
    template_name = "result_detail.html"


class ItemList(ListView):
    template_name = "items_list.html"
    context_object_name = "all_items"

    def get_queryset(self):
        return Item.objects.all()


# views GOOGLE SEARCH
class GoogleSearchCreate(CreateView):
    model = GoogleSearch
    fields = [
        "name",
        "description",
        "query",
        "num",
        "date_restrict_d",
        "exact_terms",
        "file_type",
        "gl",
        "lr",
        "or_terms",
        "related_site",
        "sort",
        "site_search",
        "search_type",
    ]
    template_name = "generic_form.html"


class GoogleSearchUpdate(UpdateView):
    model = GoogleSearch
    fields = "__all__"
    template_name = "generic_form.html"


## views PGP SEARCH
class PgpSearchCreate(CreateView):
    model = PgpSearch
    template_name = "generic_form.html"
    fields = ["name", "description", "query"]


class PgpSearchUpdate(UpdateView):
    model = PgpSearch
    fields = "__all__"
    template_name = "generic_form.html"


# views ADVANCED CRAWLER
class AdvancedCrawlerCreate(CreateView):
    model = AdvancedCrawler
    template_name = "generic_form.html"
    fields = [
        "name",
        "description",
        "url",
        "depth",
        "mobile_emulation",
        "allow_external",
    ]


class AdvancedCrawlerUpdate(UpdateView):
    model = AdvancedCrawler
    fields = "__all__"
    template_name = "generic_form.html"


# views ADVANCED CRAWLER
class CertificateTransparencyCreate(CreateView):
    model = CertificateTransparency
    template_name = "generic_form.html"
    fields = "__all__"


class CertificateTransparencyUpdate(UpdateView):
    model = CertificateTransparency
    fields = "__all__"
    template_name = "generic_form.html"


# views DNS LOOKUP
class DnsLookupCreate(CreateView):
    model = DnsLookup
    template_name = "generic_form.html"
    fields = "__all__"


class DnsLookupUpdate(UpdateView):
    model = DnsLookup
    fields = "__all__"
    template_name = "generic_form.html"


# views SIMPLE CRAWLER
class SimpleCrawlerCreate(CreateView):
    model = SimpleCrawler
    template_name = "generic_form.html"
    fields = "__all__"


class SimpleCrawlerUpdate(UpdateView):
    model = SimpleCrawler
    fields = "__all__"
    template_name = "generic_form.html"


# views SHODAN SEARCH
class ShodanSearchCreate(CreateView):
    model = ShodanSearch
    template_name = "generic_form.html"
    fields = "__all__"


class ShodanSearchUpdate(UpdateView):
    model = ShodanSearch
    fields = "__all__"
    template_name = "generic_form.html"
