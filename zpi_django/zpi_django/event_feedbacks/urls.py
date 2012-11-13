#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from zpi_django.event_feedbacks.views import show_feedbacks,add_feedback_json

urlpatterns = patterns('',
          url(r'^pokaz/(?P<event_id>[\d{0,5}]+)/$', show_feedbacks),
          url(r'^dodaj_json/$', add_feedback_json),

       )