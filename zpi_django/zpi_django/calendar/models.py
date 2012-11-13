#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from zpi_django.events.models import Event
from django.db.models import datetime

# Kalendarz wydarzen uzytkownika
class Calendar(models.Model):
    user = models.ForeignKey(User, verbose_name="użytkownik")
    event = models.ForeignKey(Event, verbose_name="wydarzenie")



     
    
    def __unicode__(self):
        return '%s do wydarzenia: %s' % (self.user.username, self.event.name)
    
    class Meta:
        verbose_name = "Kalendarz uzytkownika"
        verbose_name_plural = "Kalendarze uzytkownikow"
    