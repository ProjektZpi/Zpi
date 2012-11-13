#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
from geopy.geocoders.google import Google
from geopy.geocoders.google import GQueryError
from zpi_django.cities.models import City
from zpi_django.stdimage.fields import StdImageField

# Kategorie wydarzeń
class Place(models.Model):
    address = models.CharField(max_length=100)
    city = models.ForeignKey(City, verbose_name="miasto")
    location=gis_models.PointField(u"longitude/latitude",geography=True,blank=True,null=True)
    gis=gis_models.GeoManager()
    objects=models.Manager()
    
    
    def __unicode__(self):
        return '%s' % (self.address)
    
    def save(self,**kwargs):
        if not self.location:
            address = u'%s %s' % (self.city, self.address)
            address=address.encode("utf-8")
            geocoder=Google()
            try:
                _, latlon = geocoder.geocode(address)
            except ("Geocodowanie blad", GQueryError, ValueError):
                pass
            else:
                point = "POINT(%s %s)" % (latlon[1], latlon[0])
                self.location = geos.fromstr(point)
        super(Place, self).save()
    