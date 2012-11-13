#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from zpi_django.calendar.views import calendar, calendar2, join_json

urlpatterns = patterns('',
        url(r'^pokaz/(?P<year>[\d{0,12}]+)/(?P<month>[\d{0,12}]+)/$', calendar),
        url(r'^dolacz/$',  join_json),
        url(r'', calendar2),

       )