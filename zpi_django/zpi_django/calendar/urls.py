#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from zpi_django.calendar.views import join_json, calendar_json

urlpatterns = patterns('',

        url(r'^dolacz/$',  join_json),
        url(r'^aktualizuj/$',  calendar_json),


       )