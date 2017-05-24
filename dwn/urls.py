"""dwn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^api/auth/', include('authentication.urls', namespace='auth')),
    url(r'^api/accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^api/accounts/', include('calls.urls', namespace='calls')),
    url(r'^api/accounts/', include('users.urls', namespace='users')),
    url(r'^api/accounts/', include('ctm_numbers.urls', namespace='numbers')),
    url(r'^api/reports/', include('reports.urls', namespace='reports')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
