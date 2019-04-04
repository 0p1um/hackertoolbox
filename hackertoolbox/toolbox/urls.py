from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='toolbox_home'),
    path('admin/', admin.site.urls),
    path('osint/', include('osint_tasks.urls')),
    path('search/', include('search.urls')),
]

