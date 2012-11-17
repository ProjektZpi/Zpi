#-*- coding: utf-8 -*-
from django.db import models

from zpi_django.events.models import Event

# Lista tagów
class EventTag(models.Model):
    name = models.CharField(max_length="50", verbose_name="nazwa")
    event = models.ManyToManyField(Event)
    
    def __unicode__(self):
        return '%s' % (self.name)
    
    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tagi"
