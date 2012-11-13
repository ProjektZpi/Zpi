#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


# PANEL ADMINA
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

# URL: GRAFIKA STATYCZNA
import os.path
urlpatterns += patterns('',
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}),
    (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
    )

# PODSTRONY NASZE APLIKACJE TYLKO INCLUDOWA� URL'E Z APLIKACJI !
from view import main_page

urlpatterns += patterns('',
    ('^$',main_page),
	url(r'^wydarzenia/', include('zpi_django.events.urls')),
    url(r'^komentarze/', include('zpi_django.event_comments.urls')),
    url(r'^autoryzacja/', include('zpi_django.auth.urls')),
    ('^miejsce/',include('zpi_django.place.urls')),
    ('^ocena/',include('zpi_django.event_feedbacks.urls')),
    ('^kalendarz/',include('zpi_django.calendar.urls')),
    ('^profil/',include('zpi_django.user_profile.urls')),
#<<<<<<< HEAD
    ('^statystyki/',include('zpi_django.statistics.urls')),
#=======
    ('^uzytkownik/',include('zpi_django.friends.urls')),
#>>>>>>> c73c6594aa595d94e8564b63489afa8ddd12441c
    
)

