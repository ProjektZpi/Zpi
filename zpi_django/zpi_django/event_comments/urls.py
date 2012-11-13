#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from zpi_django.event_comments.views import add_comment_json

urlpatterns = patterns('',
          url(r'^dodaj_json/$', add_comment_json),

       )