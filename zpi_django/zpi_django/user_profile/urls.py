#-*- coding: utf-8 -*-

from django.conf.urls import patterns

from views import my_profile,  edit_profile

urlpatterns = patterns('',
    ('^moj_profil/', my_profile),
    ('^zmien_dane/(?P<form_id>[\d{0,5}]+)/$',edit_profile),
)