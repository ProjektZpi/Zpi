#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from zpi_django.tags.models import EventTag


# Statystyki użytkowników
class AuthorStatistic(models.Model):
    user = models.ForeignKey(User, verbose_name="użytkownik")
    atmosphere_avg = models.FloatField(verbose_name="atmosfera wydarzenia (średnia)", default=0.0)
    organisation_avg = models.FloatField(verbose_name="organizacja wydarzenia (średnia)", default=0.0)
    overall = models.FloatField(verbose_name="ogólna ocena", default=0.0)
    liked_count = models.IntegerField("łącznie zapisanych na wydarzenia", default=0.0)
    
    def __unicode__(self):
        return 'statystyka dla: %s' % (self.user)
    
    class Meta:
        verbose_name = "statystyka użytkownika"
        verbose_name_plural = "statystyki użytkowników"
  
  
class Gustomierz(models.Model):
    user = models.ForeignKey(User, verbose_name="użytkownik")
    tag = models.CharField(max_length=100, verbose_name="tag")
    tag_number =  models.IntegerField("Numer tagu", default=1) 
    overall_avg= models.FloatField(verbose_name="srednia ocena tagu", default=0.0)
    
    def __unicode__(self):
        return 'gustomierz: %s %s' % (self.user,self.tag )
    
    class Meta:
        verbose_name = "gustomierz"
        verbose_name_plural = "gustomierz"