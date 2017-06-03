from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      os.environ.get('DJANGO_SETTINGS_FILE', 'dwn.settings'))


app = Celery('dwn')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(CELERY_ACCEPT_CONTENT=['pickle', 'json'])
