#-*- coding: utf-8 -*-
from django.db import models

from zpi_django.stdimage.fields import StdImageField
from zpi_django.place.models import Place
from django.contrib.auth.models import User

# Kategorie wydarzeń
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="nazwa")

    def __unicode__(self):
        return '%s' % (self.name)
    
    class Meta:
        verbose_name = "kategoria"
        verbose_name_plural = "kategorie"
    

class Event(models.Model):
    
    PERIOD_CHOICES = (
        ('0', 'jednorazowo'),
        ('1', 'co tydzień'),
        ('2', 'co miesiąc'),
        ('3', 'co rok'),
    )

    name = models.CharField(max_length=200, verbose_name="nazwa *")
    user = models.ForeignKey(User, verbose_name="użytkownik")
    category = models.ForeignKey(Category, verbose_name="kategoria *")
    miniature = StdImageField(upload_to="uploaded/events_poster", blank=True, verbose_name="miniatura", help_text="Miniatura (logo) wydarzenia, które będzie wyświetlane w wyszukiwarce. Jeżeli nie dodasz żadnego ustawimy automatycznie za Ciebie")
    start_date = models.DateTimeField(verbose_name="data rozpoczęcia *")
    end_date = models.DateTimeField(verbose_name="data zakończenia *")
    place = models.ForeignKey(Place, verbose_name="miejsce *")
    tickets = models.TextField(verbose_name="bilety *")
    introduction = models.TextField(verbose_name="krótki opis wydarzenia *")
    description = models.TextField(verbose_name="pełny opis wydarzenia *")
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default=0, verbose_name="Cykliczność *", help_text="Jeżeli wydarzenie jest cykliczne to wybierz co ile, będziemy, je za Ciebie odnawiać")
    own_page = models.URLField(verbose_name="strona internetowa", blank=True)
    
    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = "wydarzenie"
        verbose_name_plural = "wydarzenia"
        

    

class EventPhoto(models.Model):
    event = models.OneToOneField(Event)
    photo = StdImageField(upload_to="uploaded/events_photos",blank=True, verbose_name="zdjęcie do wydarzenia")
    description_photo = models.CharField(max_length=50, blank=True, verbose_name="opis zdjęcia")
    photo2 = StdImageField(upload_to="uploaded/events_photos",blank=True, verbose_name="zdjęcie do wydarzenia")
    description_photo2 = models.CharField(max_length=50, blank=True, verbose_name="opis zdjęcia")
    photo3 = StdImageField(upload_to="uploaded/events_photos",blank=True, verbose_name="zdjęcie do wydarzenia")
    description_photo3 = models.CharField(max_length=50, blank=True, verbose_name="opis zdjęcia")
    photo4 = StdImageField(upload_to="uploaded/events_photos",blank=True, verbose_name="zdjęcie do wydarzenia")
    description_photo4 = models.CharField(max_length=50, blank=True, verbose_name="opis zdjęcia")
    
    
    class Meta:
        verbose_name = "zdjęcie wydarzenia"
        verbose_name_plural = "zdjęcia wydarzenia"
    

