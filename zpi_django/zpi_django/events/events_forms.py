# -*- coding: utf8 -*-
from django.forms import ModelForm
from zpi_django.events.widgets import JqSplitDateTimeWidget
from zpi_django.events.fields import JqSplitDateTimeField
from models import Event, EventPhoto
from django import forms
        
class AddEventForm(ModelForm):
    start_date = JqSplitDateTimeField(widget=JqSplitDateTimeWidget(attrs={'date_class':'datepicker','time_class':'timepicker',}),label=("Rozpoczęcie *"));
    end_date = JqSplitDateTimeField(widget=JqSplitDateTimeWidget(attrs={'date_class':'datepicker','time_class':'timepicker'}),label=("Zakończenie *"));

    class Meta:
        model = Event
        exclude = ("user") 
        
class AddPhotoForm(ModelForm):
    class Meta:
        model = EventPhoto
        exclude = ("event")  

        
        