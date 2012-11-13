#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import datetime

from zpi_django.events.models import Event

# Oceny do poszczególnych wydarzeń 
class EventFeedback(models.Model):
    user = models.ForeignKey(User, verbose_name="użytkownik")
    event = models.ForeignKey(Event, verbose_name="wydarzenie")
    atmosphere = models.IntegerField(verbose_name="atmosfera wydarzenia")
    organisation = models.IntegerField(verbose_name="organizacja wydarzenia")
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name = "data dodania")
    
    def __unicode__(self):
        return '%s do wydarzenia: %s' % (self.user.username, self.event.name)
    
    class Meta:
        verbose_name = "Ocena wydarzenia"
        verbose_name_plural = "Oceny do wydarzenia"
    