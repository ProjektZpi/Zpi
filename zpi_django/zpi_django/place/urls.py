from django.conf.urls import patterns, include, url

from zpi_django.place.views import add_Place,maps,modify_place


urlpatterns = patterns('',
    url(r'^dodaj',maps),
    url(r'^success',add_Place,name="add_place"),


)


