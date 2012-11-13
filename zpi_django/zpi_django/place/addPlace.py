from zpi_django.place.models import Place
from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets



class addPlace (ModelForm):

    class Meta:
        model = Place

