#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import datetime

from zpi_django.events.models import Event

# Komentarze do poszczególnych wydarzeń 
class EventComment(models.Model):
    user = models.ForeignKey(User, verbose_name="użytkownik")
    event = models.ForeignKey(Event, verbose_name="wydarzenie")
    comment = models.TextField(verbose_name="komentarz")
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name = "data dodania")
     
    
    def __unicode__(self):
        return '%s do wydarzenia: %s' % (self.user.username, self.event.name)
    
    class Meta:
        verbose_name = "komentarz wydarzenia"
        verbose_name_plural = "komentarze do wydarzenia"
    