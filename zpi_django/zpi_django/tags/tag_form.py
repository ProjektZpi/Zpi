# -*- coding: utf8 -*-
from django.forms import ModelForm
from models import EventTag

        
class AddTagForm(ModelForm):
    class Meta:
        model = EventTag 
        exclude = ("event") 
        