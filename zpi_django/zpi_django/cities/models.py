#-*- coding: utf-8 -*-
from django.db import models

# Lista miast
class City(models.Model):
    name = models.CharField(max_length="50", verbose_name="nazwa")
    
    def __unicode__(self):
        return '%s' % (self.name)
    
    class Meta:
        verbose_name = "miasto"
        verbose_name_plural = "miasta"
