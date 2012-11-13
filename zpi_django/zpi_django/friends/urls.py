#-*- coding: utf-8 -*-

from django.conf.urls import patterns
from views import profile_information, remove_from_friend, add_to_friend

urlpatterns = patterns('',
    ('^pokaz/(?P<user_id>[\d{0,5}]+)/$', profile_information),
    ('^pokaz/usun_znajomego/(?P<user_id>[\d{0,5}]+)/$',remove_from_friend),
    ('^pokaz/dodaj_znajomego/(?P<user_id>[\d{0,5}]+)/$',add_to_friend),
)