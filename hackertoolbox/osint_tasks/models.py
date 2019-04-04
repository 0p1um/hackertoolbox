from datetime import datetime
from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel
from .constants import GL_CHOICES, FILE_TYPE_CHOICES, LR_CHOICES, SORT_CHOICES, SEARCH_CHOICES
from django.utils.timezone import now
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from datetime import datetime
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django_celery_results.models import TaskResult
from .tasks import google_search, pgp_search, advanced_crawler, ct_search, dns_lookup, simple_crawler, shodan_search
import json
import ast



crontab_validator = RegexValidator(r"([0-9]+-[0-9]+|[\*]+\/[0-9]+|[\*])", "Please enter a valid crontab style entrie")
# reg_M = (^([0-5][0-9]?[-,][0-5][0-9]?[-,]?)+([0-5][0-9]?)?)|^([0-5][0-9]?)|(^(\*/[0-5]?[0-9]?))|(^([*]?[,]?)+)
# reg_H = (^((2[0-3]|[0-1]?[0-9])[-,](2[0-3]|[0-1]?[0-9])[-,]?)+(2[0-3]|[0-1]?[0-9])?)|^(2[0-3]|[0-1]?[0-9])|(^(\*/(2[0-3]|[0-1]?[0-9])))|(^([*]?[,]?)+)
# reg_DofM = (^((3[0-1]|[1-2]?[0-9]|[1-9])[-,](3[0-1]|[1-2]?[0-9]|[1-9])[-,]?)+(3[0-1]|[1-2]?[0-9]|[1-9])?)|^(3[0-1]|[1-2]?[0-9]|[1-9])|(^(\*/(3[0-1]|[1-2]?[0-9]|[1-9])))|(^([*]?[,]?)+)
# reg_M = (^((1[0-2]|[1-9])[-,](1[0-2]|[1-9])[-,]?)+(1[0-2]|[1-9])?)|^(1[0-2]|[1-9])|(^(\*/(1[0-2]|[1-9])))|(^([*]?[,]?)+) 
# reg_DofW = (^(([1-7])[-,]([1-7])[-,]?)+([1-7])?)|^([1-7])|(^(\*/([1-7])))|(^([*]?[,]?)+)


###################### PARENTS CLASSES ################
class Task(PolymorphicModel):

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=500, blank=True, verbose_name='Description of the job (optional)')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tasks')

class Job(PolymorphicModel):

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=500, blank=True, verbose_name='Description of the job (optional)')
    minute = models.CharField(max_length=6,default='*', verbose_name="The minute(s) at which the command will be executed. (0-59, ranges, or divided, *=all)",\
    validators=[crontab_validator])
    hour = models.CharField(max_length=6,default='*', verbose_name="The hour(s) at which the command will be executed. (0-23, ranges, or divided, *=all)",\
    validators=[crontab_validator])
    day_of_the_month = models.CharField(max_length=6,default='*', verbose_name="The day(s) of the month on which the command will be executed. (1-31, ranges, or divided, *=all)"\
    ,validators=[crontab_validator])
    month_of_the_year = models.CharField(max_length=6,default='*', verbose_name="The month(s) of the year during which the command will be executed. (1-12, ranges, or divided, *=all)"\
    ,validators=[crontab_validator])
    day_of_the_week = models.CharField(max_length=6,default='*', verbose_name="The day(s) of the week on which the command will be executed. (0-7, 7=Sun or use names, ranges, or divided, *=all)"\
    ,validators=[crontab_validator])
    tasks = models.ManyToManyField(Task)
    is_active = models.BooleanField(default=1)

    def create_periodic_task(self):
        if self.is_active:
            schedule, _ = CrontabSchedule.objects.get_or_create(minute=self.minute,hour=self.hour,day_of_week=self.day_of_the_week,\
            day_of_month=self.day_of_the_month,month_of_year=self.month_of_the_year)
            for task in self.tasks.all():
                PeriodicTask.objects.get_or_create(crontab=schedule,name=self.name+'-'+task.name, task=task.task_path, args=task.args)

    def get_absolute_url(self):
        return reverse('jobs')
    
    def __str__(self):
        return self.name

class ResultFromTask(PolymorphicModel):
    
    content_type = models.CharField(null=True, max_length=128)
    content_encoding = models.CharField(null=True, max_length=64)
    task_id = models.CharField(max_length=255, unique=True)
    task_name = models.CharField(null=True, max_length=255)
    task_args = models.TextField(null=True)
    task_kwargs = models.TextField(null=True)
    result = models.TextField(null=True, default=None, editable=False)
    status = models.CharField(max_length=50)
    date_done = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('results_detail')

    def __str__(self):
        return self.task_name

class Item(PolymorphicModel):
    pass

######### CLASSES FOR GOOGLE SEARCH MODULE
class GoogleSearch(Task):

    query = models.CharField(max_length=1000, verbose_name='Query')
    num = models.PositiveIntegerField(blank=True, null=True, verbose_name='Number of result to keep')
    date_restrict_d = models.PositiveIntegerField(blank=True, null=True, verbose_name='Date restriction: number of days old maximum for results')
    exact_terms = models.CharField(null=True, max_length=1000, blank=True, verbose_name='Exact terms to include in the search')
    file_type = models.CharField(null=True,max_length=4, choices=FILE_TYPE_CHOICES, blank=True, verbose_name='File type searched')
    gl = models.CharField(null=True, max_length=2, choices=GL_CHOICES, blank=True, verbose_name='Geo location of the search request')
    link_site = models.URLField(null=True, max_length=2000, blank=True, verbose_name='Link that must be in the search results')
    lr = models.CharField(null=True, max_length=10, choices=LR_CHOICES, blank=True, verbose_name='Language restriction: results must be in that language')
    or_terms = models.CharField(null=True, max_length=1000,blank=True, verbose_name='Additional query field with OR operator')
    related_site = models.URLField(null=True, max_length=2000, blank=True, verbose_name='URL, results must be related to it.')
    sort = models.CharField(null=True, max_length=4, choices=SORT_CHOICES, blank=True, verbose_name='Results are sort by it')
    site_search = models.CharField(null=True, max_length=255, blank=True, verbose_name='Particular domain, results must be from this domain')
    search_type = models.CharField(null=True, max_length=5, choices=SEARCH_CHOICES, blank=True, verbose_name='Search type: Webpage or Images')

    @property
    def task_path(self):
        return 'google_search'

    @property
    def args(self):
        return json.dumps([self.query, self.num, self.date_restrict_d, self.exact_terms, self.file_type, self.gl, self.link_site, self.lr, self.or_terms,\
         self.related_site, self.sort, self.site_search, self.search_type])

    def run(self):
        google_search.delay(self.query, self.num, self.date_restrict_d, self.exact_terms, self.file_type, self.gl, self.link_site, self.lr, self.or_terms,\
         self.related_site, self.sort, self.site_search, self.search_type)


class ResultGoogleSearch(ResultFromTask):

    search_time = models.FloatField(null=True, blank=True)
    total_results = models.PositiveIntegerField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('result')

class ItemGoogleSearch(Item):

    title = models.CharField(null=True, blank=True, max_length=255)
    link = models.URLField(null=True, blank=True)
    snippet = models.TextField(null=True, blank=True, max_length=2000)
    result_gs = models.ForeignKey(ResultGoogleSearch, on_delete=models.CASCADE)

    @property
    def list_of_subitems(self):
        list_of_subitems=[{'date':self.result_gs.date_done, 'type':'Google Search link', 'abstract_type': 'url', 'data':self.link, \
        'transform':['advanced_crawler', 'ct_search', 'pgp_search']}, \
        {'date':self.result_gs.date_done, 'type':'Google Search snipet', 'abstract_type':'text', 'data':self.snippet,\
        'transform':['google_search']}, \
        {'date':self.result_gs.date_done, 'type':'Google Search title', 'abstract_type':'text', 'data':self.title, 'transform':['google_search']}]
        return list_of_subitems

#####CLASSES PGP MODULE
class PgpSearch(Task):

    query = models.CharField(max_length=255)

    @property
    def task_path(self):
        return 'pgp_search'

    @property
    def args(self):
        return json.dumps([self.query])
    
    def run(self):
        pgp_search.delay(self.args)

class ResultPgpSearch(ResultFromTask):

    def get_absolute_url(self):
        return reverse('result')

class ItemPgpSearch(Item):

    name = models.CharField(max_length=255)
    public_key_fingerprint = models.CharField(max_length=20)
    email = models.EmailField()
    result_pgps = models.ForeignKey(ResultPgpSearch, on_delete=models.CASCADE)

    @property
    def list_of_subitems(self):
        list_of_subitems=[{'date':self.result_pgps.date_done, 'type':'pgp search mail', 'abstract_type':'email', 'data':self.email, 'transform':['google_search']},
        {'date':self.result_pgps.date_done, 'type':'pgp search name', 'abstract_type':'text', 'data':self.name, 'transform':['google_search']},
        {'date':self.result_pgps.date_done, 'type':'pgp search pub key fingerprint', 'abstract_type':'name', 'data':self.public_key_fingerprint, 'transform':['google_search']}]
        return list_of_subitems


##### CLASSES ADVANCED CRAWLER MODULE
class AdvancedCrawler(Task):

    url = models.URLField()
    mobile_emulation = models.BooleanField(default=False, verbose_name='Enable emulation of mobile to gather mobile version website ( emulated device is Nexus5 )')
    depth = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(50),MinValueValidator(1)], verbose_name='Depth of the crawling')
    allow_external = models.BooleanField(default=False, verbose_name='Allow the crawler to crawl external website referenced (urls in other domain that the url field)')

    @property
    def task_path(self):
        return 'advanced_crawler'

    @property
    def args(self):
        return json.dumps([self.url, self.depth, self.mobile_emulation, self.allow_external])
    
    def run(self):
        advanced_crawler.delay(self.url, self.depth, self.mobile_emulation, self.allow_external)

class ResultAdvancedCrawler(ResultFromTask):

    def get_absolute_url(self):
        return reverse('result')

class ItemAdvancedCrawler(Item):

    url = models.URLField()
    source_code = models.TextField()
    links_list = models.TextField()
    result_ac = models.ForeignKey(ResultAdvancedCrawler, on_delete=models.CASCADE)

    @property
    def list_of_subitems(self):
        list_of_subitems=[{'date':self.result_ac.date_done, 'type':'advanced crawler source code', 'abstract_type':'text', 'data':self.source_code}, \
        {'date':self.result_ac.date_done,'type':'advanced crawler url', 'abstract_type':'url', 'data':self.url }]
        for link in ast.literal_eval(self.links_list):
            list_of_subitems.append({'date':self.result_ac.date_done,'type':'advanced crawler url', 'abstract_type':'url', 'data':link, \
            'transform':['advanced_crawler', 'ct_search', 'google_search', 'pgp_search'] })
        return list_of_subitems

##### CLASS CERTIFICATE TRANSPARENCY MODULE
class CertificateTransparency(Task):
    query = models.CharField(max_length=255)

    @property
    def task_path(self):
        return 'ct_search'

    @property
    def args(self):
        return json.dumps([self.query])
    
    def run(self):
        ct_search.delay(self.query)

class ResultCertificateTransparency(ResultFromTask):

    def get_absolute_url(self):
        return reverse('result')

class ItemCertificateTransparency(Item):
    
    domain = models.CharField(max_length=255)
    result_cts = models.ForeignKey(ResultCertificateTransparency, on_delete=models.CASCADE)

    @property
    def list_of_subitems(self):
        list_of_subitems=[{'date':self.result_cts.date_done, 'type':'Certificate transparency domain', 'abstract_type':'domain', 'data':self.domain,\
         'transform':['advanced_crawler', 'ct_search', 'google_search', 'pgp_search']}]
        return list_of_subitems

##### CLASS DNS LOOKUP MODULE
class DnsLookup(Task):

    query = models.CharField(max_length=255)
    type_A = models.BooleanField(default=True, verbose_name='A records lookup')
    type_AAAA = models.BooleanField(default=False, verbose_name='AAAA records lookup')
    type_CNAME = models.BooleanField(default=False, verbose_name='CNAME records lookup (recursive, will include all redirection)')
    type_NS = models.BooleanField(default=False, verbose_name='NS records lookup')
    type_MX = models.BooleanField(default=False, verbose_name='MX records lookup')
    type_TXT = models.BooleanField(default=False, verbose_name='TXT records lookup')
    type_ALL = models.BooleanField(default=False, verbose_name='All types of records lookup, require a good understanding of dns records')

    @property
    def task_path(self):
        return 'dns_lookup'

    @property
    def args(self):
        return json.dumps([self.query, self.type_A, self.type_AAAA, self.type_CNAME, self.type_NS, self.type_MX, self.type_TXT, self.type_ALL])
    
    def run(self):
        dns_lookup.delay(self.query, self.type_A, self.type_AAAA, self.type_CNAME, self.type_NS, self.type_MX, self.type_TXT, self.type_ALL)

class ResultDnsLookup(ResultFromTask):

    def get_absolute_url(self):
        return reverse('result')

class ItemDnsLookup(Item):
    
    query = models.CharField(max_length=255)
    record_type = models.CharField(max_length=10)
    result = models.TextField()
    result_dl = models.ForeignKey(ResultDnsLookup, on_delete=models.CASCADE)

    @property
    def list_of_subitems(self):
        if (self.record_type == 'A' or self.record_type == 'AAAA'):
            list_of_subitems=[{'date':self.result_dl.date_done, 'type':'DNS '+self.record_type, 'abstract_type':'IP', 'data':self.result,\
            'transform':['advanced_crawler']}]
        elif self.record_type == 'CNAME':
            list_of_subitems=[{'date':self.result_dl.date_done, 'type':'DNS '+self.record_type, 'abstract_type':'domain', 'data':self.result,\
            'transform':['dns_lookup', 'google_search']}]
        else:
            list_of_subitems=[{'date':self.result_dl.date_done, 'type':'DNS '+self.record_type, 'abstract_type':'text', 'data':self.result,\
            'transform':[]}]
        return list_of_subitems

##### CLASS SIMPLE CRAWLER MODULE
class SimpleCrawler(Task):

    url = models.URLField()
    depth = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(50),MinValueValidator(1)], verbose_name='Depth of the crawling')
    allow_external = models.BooleanField(default=False, verbose_name='Allow the crawler to crawl external website referenced (urls in other domain that the url field)')

    @property
    def task_path(self):
        return 'simple_crawler'

    @property
    def args(self):
        return json.dumps([self.url, self.depth, self.allow_external])
    
    def run(self):
        simple_crawler.delay(self.url, self.depth, self.allow_external)

class ResultSimpleCrawler(ResultFromTask):

    def get_absolute_url(self):
        return reverse('result')

class ItemSimpleCrawler(Item):
    
    url = models.URLField()
    source_code = models.TextField()
    links_list = models.TextField()
    result_sc = models.ForeignKey(ResultSimpleCrawler, on_delete=models.CASCADE)

    @property
    def list_of_subitems(self):
        list_of_subitems = [{'date':self.result_sc.date_done, 'type':'Simple Crawler url', 'abstract_type':'url', 'data':self.url,\
            'transform':['advanced_crawler','google_search']},\
             {'date':self.result_sc.date_done, 'type':'Simple Crawler source code', 'abstract_type':'text', 'data':self.source_code,\
            'transform':[]}]
        for link in ast.literal_eval(self.links_list):
            list_of_subitems.append({'date':self.result_sc.date_done, 'type':'Simple Crawler url', 'abstract_type':'url', 'data':link,\
        'transform':['advanced_crawler','google_search']})
        return list_of_subitems

##### CLASS SHODAN SEARCH MODULE
class ShodanSearch(Task):

    query = models.CharField(max_length=255)

    @property
    def task_path(self):
        return 'shodan_search'

    @property
    def args(self):
        return json.dumps([self.query])
    
    def run(self):
        shodan_search.delay(self.query)

class ResultShodanSearch(ResultFromTask):

    def get_absolute_url(self):
        return reverse('result')

class ItemShodanSearch(Item):

    ip = models.GenericIPAddressField()
    hostnames = models.TextField()
    domains = models.TextField()
    shodan_id = models.CharField(max_length=255)
    location = models.TextField()
    port = models.PositiveIntegerField()
    banner = models.TextField()
    result_ss = models.ForeignKey(ResultShodanSearch, on_delete=models.CASCADE)

    @property
    def list_of_subitems(self):
        list_of_subitems = [{'date':self.result_ss.date_done, 'type':'Shodan Search IP', 'abstract_type':'IP', 'data':self.ip,\
            'transform':['advanced_crawler','google_search']},\
             {'date':self.result_ss.date_done, 'type':'Shodan Search shodan_id', 'abstract_type':'text', 'data':self.shodan_id,\
            'transform':[]},\
            {'date':self.result_ss.date_done, 'type':'Shodan Search location', 'abstract_type':'location', 'data':self.location,\
            'transform':[]},\
            {'date':self.result_ss.date_done, 'type':'Shodan Search port', 'abstract_type':'port', 'data':self.port,\
            'transform':[]},\
            {'date':self.result_ss.date_done, 'type':'Shodan Search banner', 'abstract_type':'location', 'data':self.banner,\
            'transform':[]}]
        for hostname in ast.literal_eval(self.hostnames):
            list_of_subitems.append({'date':self.result_ss.date_done, 'type':'Shodan Search hostname', 'abstract_type':'domain', 'data':hostname,\
        'transform':['advanced_crawler','google_search', 'dns_lookup']})
        for domain in ast.literal_eval(self.domains):
            list_of_subitems.append({'date':self.result_ss.date_done, 'type':'Shodan Search domain', 'abstract_type':'domain', 'data':domain,\
        'transform':['advanced_crawler','google_search', 'dns_lookup']})
        return list_of_subitems

