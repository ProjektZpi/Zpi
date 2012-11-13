#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from zpi_django.stdimage.fields import StdImageField

import datetime
from django.template.defaultfilters import slugify
def unique_filename(instance, filename):
    now = datetime.datetime.now()
    fname, dot, extension = filename.rpartition('.')
    slug = slugify(instance.user)
    print slug
    return '%s%s/%s%s%s%s.%s' % ('uploaded/avatars/',slug,now.day,now.hour,now.minute,now.second, extension) 
# Profile użytkowników 

class UserProfile(models.Model):
    GENDER_CHOICES = (
            ('M','Mężczyzna'),
            ('K','Kobieta'),
            )
    
    user = models.OneToOneField(User, verbose_name="użytkownik")
    gender = models.CharField(max_length=200, choices = GENDER_CHOICES, verbose_name="płeć", default=0)
    avatar = StdImageField(upload_to=unique_filename, blank=True, size=(190,300))
    city = models.CharField(max_length=50, verbose_name="miasto *")

    def __unicode__(self):
        return '%s' % (self.user.username)
    
    class Meta:
        verbose_name = "profil użytkownika"
        verbose_name_plural = "profile użytkowników"
        
   
    
# Automatyczne tworzenie profilu (rozszerzanie zwykłego usera, przy zakładaniu konta)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
post_save.connect(create_user_profile, sender=User)
    