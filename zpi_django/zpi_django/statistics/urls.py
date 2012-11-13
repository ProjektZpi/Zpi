#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from zpi_django.statistics.views import update, gustomierz,recommendedEvents

urlpatterns = patterns('',
          url(r'^aktualizuj/(?P<event_id>[\d{0,5}]+)/$', update),
          url(r'^gustomierz/(?P<user_id>[\d{0,5}]+)/(?P<number_of_tags>[\d{0,5}]+)/$', gustomierz),
          url(r'^polecane/(?P<user_id>[\d{0,5}]+)/$', recommendedEvents),
          

       )