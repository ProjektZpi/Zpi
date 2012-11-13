#-*- coding: utf-8 -*-

from django.conf.urls import patterns

from views import login_view, logout_view, register_view, login_form_alternative

urlpatterns = patterns('',
    ('^zaloguj/', login_view),
    ('^wyloguj/', logout_view),
    ('^rejestracja/', register_view),
    ('^panel_logowania/',login_form_alternative),
)