# Generated by Django 2.1.5 on 2019-02-16 16:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='Description of the job (optional)')),
                ('minute', models.CharField(default='*', max_length=6, validators=[django.core.validators.RegexValidator('([0-9]+-[0-9]+|[\\*]+\\/[0-9]+|[\\*])', 'Please enter a valid crontab style entrie')], verbose_name='The minute(s) at which the command will be executed. (0-59, ranges, or divided, *=all)')),
                ('hour', models.CharField(default='*', max_length=6, validators=[django.core.validators.RegexValidator('([0-9]+-[0-9]+|[\\*]+\\/[0-9]+|[\\*])', 'Please enter a valid crontab style entrie')], verbose_name='The hour(s) at which the command will be executed. (0-23, ranges, or divided, *=all)')),
                ('day_of_the_month', models.CharField(default='*', max_length=6, validators=[django.core.validators.RegexValidator('([0-9]+-[0-9]+|[\\*]+\\/[0-9]+|[\\*])', 'Please enter a valid crontab style entrie')], verbose_name='The day(s) of the month on which the command will be executed. (1-31, ranges, or divided, *=all)')),
                ('month_of_the_year', models.CharField(default='*', max_length=6, validators=[django.core.validators.RegexValidator('([0-9]+-[0-9]+|[\\*]+\\/[0-9]+|[\\*])', 'Please enter a valid crontab style entrie')], verbose_name='The month(s) of the year during which the command will be executed. (1-12, ranges, or divided, *=all)')),
                ('day_of_the_week', models.CharField(default='*', max_length=6, validators=[django.core.validators.RegexValidator('([0-9]+-[0-9]+|[\\*]+\\/[0-9]+|[\\*])', 'Please enter a valid crontab style entrie')], verbose_name='The day(s) of the week on which the command will be executed. (0-7, 7=Sun or use names, ranges, or divided, *=all)')),
                ('is_active', models.BooleanField(default=1)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_osint_tasks.job_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='ResultFromTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(max_length=128, null=True)),
                ('content_encoding', models.CharField(max_length=64, null=True)),
                ('task_id', models.CharField(max_length=255, unique=True)),
                ('task_name', models.CharField(max_length=255, null=True)),
                ('task_args', models.TextField(null=True)),
                ('task_kwargs', models.TextField(null=True)),
                ('result', models.TextField(default=None, editable=False, null=True)),
                ('status', models.CharField(max_length=50)),
                ('date_done', models.DateTimeField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='Description of the job (optional)')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='AdvancedCrawler',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Task')),
                ('url', models.URLField()),
                ('mobile_emulation', models.BooleanField(default=False, verbose_name='Enable emulation of mobile to gather mobile version website ( emulated device is Nexus5 )')),
                ('depth', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(1)], verbose_name='Depth of the crawling')),
                ('allow_external', models.BooleanField(default=False, verbose_name='Allow the crawler to crawl external website referenced (urls in other domain that the url field)')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.task',),
        ),
        migrations.CreateModel(
            name='CertificateTransparency',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Task')),
                ('query', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.task',),
        ),
        migrations.CreateModel(
            name='DnsLookup',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Task')),
                ('query', models.CharField(max_length=255)),
                ('type_A', models.BooleanField(default=True, verbose_name='A records lookup')),
                ('type_AAAA', models.BooleanField(default=False, verbose_name='AAAA records lookup')),
                ('type_CNAME', models.BooleanField(default=False, verbose_name='CNAME records lookup (recursive, will include all redirection)')),
                ('type_NS', models.BooleanField(default=False, verbose_name='NS records lookup')),
                ('type_MX', models.BooleanField(default=False, verbose_name='MX records lookup')),
                ('type_TXT', models.BooleanField(default=False, verbose_name='TXT records lookup')),
                ('type_ALL', models.BooleanField(default=False, verbose_name='All types of records lookup, require a good understanding of dns records')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.task',),
        ),
        migrations.CreateModel(
            name='GoogleSearch',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Task')),
                ('query', models.CharField(max_length=1000, verbose_name='Query')),
                ('num', models.PositiveIntegerField(blank=True, null=True, verbose_name='Number of result to keep')),
                ('date_restrict_d', models.PositiveIntegerField(blank=True, null=True, verbose_name='Date restriction: number of days old maximum for results')),
                ('exact_terms', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Exact terms to include in the search')),
                ('file_type', models.CharField(blank=True, choices=[('', 'None'), ('swf', 'Adobe Flash (.swf)'), ('pdf', 'Adobe Portable Document Format (.pdf)'), ('ps', 'Adobe PostScript (.ps)'), ('dwf', 'Autodesk Design Web Format (.dwf)'), ('kml', 'Google Earth (.kml, .kmz)'), ('gpx', 'GPS eXchange Format (.gpx)'), ('hwp', 'Hancom Hanword (.hwp)'), ('htm', 'HTML (.htm, .html)'), ('xls', 'Microsoft Exel (.xls, .xlsx)'), ('ppt', 'Microsoft PowerPoint (.ppt, .pptx)'), ('doc', 'Microsoft Word (.doc, .docx)'), ('odp', 'OpenOffice presentation (.odp)'), ('ods', 'OpenOffice spreadsheet (.ods)'), ('odt', 'OpenOffice text (.odt)'), ('rtf', 'Rich Text Format (.rtf)'), ('svg', 'Scalable Vector Graphics (.svg)'), ('tex', 'Tex/LaTeX (.tex)'), ('txt', 'Text (.txt, .text, including source code extentions in common programming language)'), ('bas', 'Basic source code (.bas)'), ('c', 'C/C++ source code (.c, .cc, .cpp, .cxx, .h, .hpp)'), ('cs', 'C# source code (.cs)'), ('java', 'Java source code (.java)'), ('pl', 'Perl source code (.pl)'), ('py', 'Python souce code (.py)'), ('wml', 'Wireless Markup Language (.wml, .wap)'), ('xml', 'XML (.xml)')], max_length=4, null=True, verbose_name='File type searched')),
                ('gl', models.CharField(blank=True, choices=[('', 'None'), ('af', 'Afghanistan '), ('al', 'Albania '), ('dz', 'Algeria '), ('as', 'American Samoa '), ('ad', 'Andorra '), ('ao', 'Angola '), ('ai', 'Anguilla '), ('aq', 'Antarctica '), ('ag', 'Antigua and Barbuda '), ('ar', 'Argentina '), ('am', 'Armenia '), ('aw', 'Aruba '), ('au', 'Australia '), ('at', 'Austria '), ('az', 'Azerbaijan '), ('bs', 'Bahamas '), ('bh', 'Bahrain '), ('bd', 'Bangladesh '), ('bb', 'Barbados '), ('by', 'Belarus '), ('be', 'Belgium '), ('bz', 'Belize '), ('bj', 'Benin '), ('bm', 'Bermuda '), ('bt', 'Bhutan '), ('bo', 'Bolivia '), ('ba', 'Bosnia and Herzegovina '), ('bw', 'Botswana '), ('bv', 'Bouvet Island '), ('br', 'Brazil '), ('io', 'British Indian Ocean Territory '), ('bn', 'Brunei Darussalam '), ('bg', 'Bulgaria '), ('bf', 'Burkina Faso '), ('bi', 'Burundi '), ('kh', 'Cambodia '), ('cm', 'Cameroon '), ('ca', 'Canada '), ('cv', 'Cape Verde '), ('ky', 'Cayman Islands '), ('cf', 'Central African Republic '), ('td', 'Chad '), ('cl', 'Chile '), ('cn', 'China '), ('cx', 'Christmas Island '), ('cc', 'Cocos (Keeling) Islands '), ('co', 'Colombia '), ('km', 'Comoros '), ('cg', 'Congo '), ('cd', 'Congo, the Democratic Republic of the '), ('ck', 'Cook Islands '), ('cr', 'Costa Rica '), ('ci', "Cote D'ivoire "), ('hr', 'Croatia '), ('cu', 'Cuba '), ('cy', 'Cyprus '), ('cz', 'Czech Republic '), ('dk', 'Denmark '), ('dj', 'Djibouti '), ('dm', 'Dominica '), ('do', 'Dominican Republic '), ('ec', 'Ecuador '), ('eg', 'Egypt '), ('sv', 'El Salvador '), ('gq', 'Equatorial Guinea '), ('er', 'Eritrea '), ('ee', 'Estonia '), ('et', 'Ethiopia '), ('fk', 'Falkland Islands (Malvinas) '), ('fo', 'Faroe Islands '), ('fj', 'Fiji '), ('fi', 'Finland '), ('fr', 'France '), ('gf', 'French Guiana '), ('pf', 'French Polynesia '), ('tf', 'French Southern Territories '), ('ga', 'Gabon '), ('gm', 'Gambia '), ('ge', 'Georgia '), ('de', 'Germany '), ('gh', 'Ghana '), ('gi', 'Gibraltar '), ('gr', 'Greece '), ('gl', 'Greenland '), ('gd', 'Grenada '), ('gp', 'Guadeloupe '), ('gu', 'Guam '), ('gt', 'Guatemala '), ('gn', 'Guinea '), ('gw', 'Guinea-Bissau '), ('gy', 'Guyana '), ('ht', 'Haiti '), ('hm', 'Heard Island and Mcdonald Islands '), ('va', 'Holy See (Vatican City State) '), ('hn', 'Honduras '), ('hk', 'Hong Kong '), ('hu', 'Hungary '), ('is', 'Iceland '), ('in', 'India '), ('id', 'Indonesia '), ('ir', 'Iran, Islamic Republic of '), ('iq', 'Iraq '), ('ie', 'Ireland '), ('il', 'Israel '), ('it', 'Italy '), ('jm', 'Jamaica '), ('jp', 'Japan '), ('jo', 'Jordan '), ('kz', 'Kazakhstan '), ('ke', 'Kenya '), ('ki', 'Kiribati '), ('kp', "Korea, Democratic People's Republic of "), ('kr', 'Korea, Republic of '), ('kw', 'Kuwait '), ('kg', 'Kyrgyzstan '), ('la', "Lao People's Democratic Republic "), ('lv', 'Latvia '), ('lb', 'Lebanon '), ('ls', 'Lesotho '), ('lr', 'Liberia '), ('ly', 'Libyan Arab Jamahiriya '), ('li', 'Liechtenstein '), ('lt', 'Lithuania '), ('lu', 'Luxembourg '), ('mo', 'Macao '), ('mk', 'Macedonia, the Former Yugosalv Republic of '), ('mg', 'Madagascar '), ('mw', 'Malawi '), ('my', 'Malaysia '), ('mv', 'Maldives '), ('ml', 'Mali '), ('mt', 'Malta '), ('mh', 'Marshall Islands '), ('mq', 'Martinique '), ('mr', 'Mauritania '), ('mu', 'Mauritius '), ('yt', 'Mayotte '), ('mx', 'Mexico '), ('fm', 'Micronesia, Federated States of '), ('md', 'Moldova, Republic of '), ('mc', 'Monaco '), ('mn', 'Mongolia '), ('ms', 'Montserrat '), ('ma', 'Morocco '), ('mz', 'Mozambique '), ('mm', 'Myanmar '), ('na', 'Namibia '), ('nr', 'Nauru '), ('np', 'Nepal '), ('nl', 'Netherlands '), ('an', 'Netherlands Antilles '), ('nc', 'New Caledonia '), ('nz', 'New Zealand '), ('ni', 'Nicaragua '), ('ne', 'Niger '), ('ng', 'Nigeria '), ('nu', 'Niue '), ('nf', 'Norfolk Island '), ('mp', 'Northern Mariana Islands '), ('no', 'Norway '), ('om', 'Oman '), ('pk', 'Pakistan '), ('pw', 'Palau '), ('ps', 'Palestinian Territory, Occupied '), ('pa', 'Panama '), ('pg', 'Papua New Guinea '), ('py', 'Paraguay '), ('pe', 'Peru '), ('ph', 'Philippines '), ('pn', 'Pitcairn '), ('pl', 'Poland '), ('pt', 'Portugal '), ('pr', 'Puerto Rico '), ('qa', 'Qatar '), ('re', 'Reunion '), ('ro', 'Romania '), ('ru', 'Russian Federation '), ('rw', 'Rwanda '), ('sh', 'Saint Helena '), ('kn', 'Saint Kitts and Nevis '), ('lc', 'Saint Lucia '), ('pm', 'Saint Pierre and Miquelon '), ('vc', 'Saint Vincent and the Grenadines '), ('ws', 'Samoa '), ('sm', 'San Marino '), ('st', 'Sao Tome and Principe '), ('sa', 'Saudi Arabia '), ('sn', 'Senegal '), ('cs', 'Serbia and Montenegro '), ('sc', 'Seychelles '), ('sl', 'Sierra Leone '), ('sg', 'Singapore '), ('sk', 'Slovakia '), ('si', 'Slovenia '), ('sb', 'Solomon Islands '), ('so', 'Somalia '), ('za', 'South Africa '), ('gs', 'South Georgia and the South Sandwich Islands '), ('es', 'Spain '), ('lk', 'Sri Lanka '), ('sd', 'Sudan '), ('sr', 'Suriname '), ('sj', 'Svalbard and Jan Mayen '), ('sz', 'Swaziland '), ('se', 'Sweden '), ('ch', 'Switzerland '), ('sy', 'Syrian Arab Republic '), ('tw', 'Taiwan, Province of China '), ('tj', 'Tajikistan '), ('tz', 'Tanzania, United Republic of '), ('th', 'Thailand '), ('tl', 'Timor-Leste '), ('tg', 'Togo '), ('tk', 'Tokelau '), ('to', 'Tonga '), ('tt', 'Trinidad and Tobago '), ('tn', 'Tunisia '), ('tr', 'Turkey '), ('tm', 'Turkmenistan '), ('tc', 'Turks and Caicos Islands '), ('tv', 'Tuvalu '), ('ug', 'Uganda '), ('ua', 'Ukraine '), ('ae', 'United Arab Emirates '), ('uk', 'United Kingdom '), ('us', 'United States '), ('um', 'United States Minor Outlying Islands '), ('uy', 'Uruguay '), ('uz', 'Uzbekistan '), ('vu', 'Vanuatu '), ('ve', 'Venezuela '), ('vn', 'Viet Nam '), ('vg', 'Virgin Island, British '), ('vi', 'Virgin Islands, US '), ('wf', 'Wallis and Futuna '), ('eh', 'Western Sahara '), ('ye', 'Yemen '), ('zm', 'Zambia '), ('zw', 'Zimbabwe ')], max_length=2, null=True, verbose_name='Geo location of the search request')),
                ('link_site', models.URLField(blank=True, max_length=2000, null=True, verbose_name='Link that must be in the search results')),
                ('lr', models.CharField(blank=True, choices=[('lang_ar', 'Arabic'), ('lang_bg', 'Bulgarian '), ('lang_ca', 'Catalan '), ('lang_zh-CN', 'Chinese (Simplified) '), ('lang_zh-TW', 'Chinese (Traditional) '), ('lang_hr', 'Croatian '), ('lang_cs', 'Czech '), ('lang_da', 'Danish '), ('lang_nl', 'Dutch '), ('lang_en', 'English '), ('lang_et', 'Estonian '), ('lang_fi', 'Finnish '), ('lang_fr', 'French '), ('lang_de', 'German '), ('lang_el', 'Greek '), ('lang_iw', 'Hebrew '), ('lang_hu', 'Hungarian '), ('lang_is', 'Icelandic '), ('lang_id', 'Indonesian '), ('lang_it', 'Italian '), ('lang_ja', 'Japanese '), ('lang_ko', 'Korean '), ('lang_lv', 'Latvian '), ('lang_lt', 'Lithuanian '), ('lang_no', 'Norwegian '), ('lang_pl', 'Polish '), ('lang_pt', 'Portuguese '), ('lang_ro', 'Romanian '), ('lang_ru', 'Russian '), ('lang_sr', 'Serbian '), ('lang_sk', 'Slovak '), ('lang_sl', 'Slovenian '), ('lang_es', 'Spanish '), ('lang_sv', 'Swedish '), ('lang_tr', 'Turkish ')], max_length=10, null=True, verbose_name='Language restriction: results must be in that language')),
                ('or_terms', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Additional query field with OR operator')),
                ('related_site', models.URLField(blank=True, max_length=2000, null=True, verbose_name='URL, results must be related to it.')),
                ('sort', models.CharField(blank=True, choices=[('', 'None'), ('date', 'Sort by date')], max_length=4, null=True, verbose_name='Results are sort by it')),
                ('site_search', models.CharField(blank=True, max_length=255, null=True, verbose_name='Particular domain, results must be from this domain')),
                ('search_type', models.CharField(blank=True, choices=[('', 'Search the webpages'), ('image', 'Search images')], max_length=5, null=True, verbose_name='Search type: Webpage or Images')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.task',),
        ),
        migrations.CreateModel(
            name='ItemAdvancedCrawler',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Item')),
                ('url', models.URLField()),
                ('source_code', models.TextField()),
                ('links_list', models.TextField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.item',),
        ),
        migrations.CreateModel(
            name='ItemCertificateTransparency',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Item')),
                ('domain', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.item',),
        ),
        migrations.CreateModel(
            name='ItemDnsLookup',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Item')),
                ('query', models.CharField(max_length=255)),
                ('record_type', models.CharField(max_length=10)),
                ('result', models.TextField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.item',),
        ),
        migrations.CreateModel(
            name='ItemGoogleSearch',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Item')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('snippet', models.TextField(blank=True, max_length=2000, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.item',),
        ),
        migrations.CreateModel(
            name='ItemPgpSearch',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Item')),
                ('name', models.CharField(max_length=255)),
                ('public_key_fingerprint', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.item',),
        ),
        migrations.CreateModel(
            name='ItemShodanSearch',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Item')),
                ('ip', models.GenericIPAddressField()),
                ('hostnames', models.TextField()),
                ('domains', models.TextField()),
                ('shodan_id', models.CharField(max_length=255)),
                ('location', models.TextField()),
                ('port', models.PositiveIntegerField()),
                ('banner', models.TextField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.item',),
        ),
        migrations.CreateModel(
            name='ItemSimpleCrawler',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Item')),
                ('url', models.URLField()),
                ('source_code', models.TextField()),
                ('links_list', models.TextField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.item',),
        ),
        migrations.CreateModel(
            name='PgpSearch',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Task')),
                ('query', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.task',),
        ),
        migrations.CreateModel(
            name='ResultAdvancedCrawler',
            fields=[
                ('resultfromtask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.ResultFromTask')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.resultfromtask',),
        ),
        migrations.CreateModel(
            name='ResultCertificateTransparency',
            fields=[
                ('resultfromtask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.ResultFromTask')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.resultfromtask',),
        ),
        migrations.CreateModel(
            name='ResultDnsLookup',
            fields=[
                ('resultfromtask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.ResultFromTask')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.resultfromtask',),
        ),
        migrations.CreateModel(
            name='ResultGoogleSearch',
            fields=[
                ('resultfromtask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.ResultFromTask')),
                ('search_time', models.FloatField(blank=True, null=True)),
                ('total_results', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.resultfromtask',),
        ),
        migrations.CreateModel(
            name='ResultPgpSearch',
            fields=[
                ('resultfromtask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.ResultFromTask')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.resultfromtask',),
        ),
        migrations.CreateModel(
            name='ResultShodanSearch',
            fields=[
                ('resultfromtask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.ResultFromTask')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.resultfromtask',),
        ),
        migrations.CreateModel(
            name='ResultSimpleCrawler',
            fields=[
                ('resultfromtask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.ResultFromTask')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.resultfromtask',),
        ),
        migrations.CreateModel(
            name='ShodanSearch',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Task')),
                ('query', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.task',),
        ),
        migrations.CreateModel(
            name='SimpleCrawler',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='osint_tasks.Task')),
                ('url', models.URLField()),
                ('depth', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(1)], verbose_name='Depth of the crawling')),
                ('allow_external', models.BooleanField(default=False, verbose_name='Allow the crawler to crawl external website referenced (urls in other domain that the url field)')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('osint_tasks.task',),
        ),
        migrations.AddField(
            model_name='task',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_osint_tasks.task_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='resultfromtask',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_osint_tasks.resultfromtask_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='job',
            name='tasks',
            field=models.ManyToManyField(to='osint_tasks.Task'),
        ),
        migrations.AddField(
            model_name='item',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_osint_tasks.item_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='itemsimplecrawler',
            name='result_sc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osint_tasks.ResultSimpleCrawler'),
        ),
        migrations.AddField(
            model_name='itemshodansearch',
            name='result_ss',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osint_tasks.ResultShodanSearch'),
        ),
        migrations.AddField(
            model_name='itempgpsearch',
            name='result_pgps',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osint_tasks.ResultPgpSearch'),
        ),
        migrations.AddField(
            model_name='itemgooglesearch',
            name='result_gs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osint_tasks.ResultGoogleSearch'),
        ),
        migrations.AddField(
            model_name='itemdnslookup',
            name='result_dl',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osint_tasks.ResultDnsLookup'),
        ),
        migrations.AddField(
            model_name='itemcertificatetransparency',
            name='result_cts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osint_tasks.ResultCertificateTransparency'),
        ),
        migrations.AddField(
            model_name='itemadvancedcrawler',
            name='result_ac',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osint_tasks.ResultAdvancedCrawler'),
        ),
    ]
