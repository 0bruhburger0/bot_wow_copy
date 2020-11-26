from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    path('^polls/', include('main.urls')),
    path('admin/', admin.site.urls),
]
