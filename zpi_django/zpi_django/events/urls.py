#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from zpi_django.events.views import add_event, show_events, event_detail,modify_event
from zpi_django.events.events_forms import AddEventForm,AddPhotoForm

urlpatterns = patterns('',
          url(r'^dodaj/$', add_event,name="add_event"),        
          url(r'^pokaz/$', show_events),
          url(r'^informacje/(?P<event_id>[\d{0,5}]+)/$', event_detail),
          url(r'^edytuj/(?P<event_id>[\d{0,5}]+)/$', modify_event),
  #        url(r'^success/', success),
          

       )