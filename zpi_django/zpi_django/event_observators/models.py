#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


from zpi_django.events.models import Event

# Obserwatorzy poszczególnych wydarzeń 
class EventObservator(models.Model):
    user = models.OneToOneField(User, verbose_name="użytkownik")
    event = models.ForeignKey(Event, verbose_name="wydarzenie")
    
    def __unicode__(self):
        return '%s obserwuje wydarzenie: %s' % (self.user.username, self.event.name)
    
    class Meta:
        verbose_name = "obserwator wydarzenia"
        verbose_name_plural = "obserwatorzy wydarzenia"
    