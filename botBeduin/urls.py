# -*- coding: utf8 -*-

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^beduin/', include('bot.urls', namespace='beduin'))
]
