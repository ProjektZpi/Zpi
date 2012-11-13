# -*- coding: utf8 -*-
from time import strptime, strftime
from django import forms
from django.forms import fields
from zpi_django.events.widgets import JqSplitDateTimeWidget

class JqSplitDateTimeField(fields.MultiValueField):
    widget = JqSplitDateTimeWidget

    def __init__(self, *args, **kwargs):
        """
        Have to pass a list of field types to the constructor, else we
        won't get any data to our compress method.
        """
        all_fields = (
            fields.CharField(max_length=10),
            fields.CharField(max_length=2),
            fields.CharField(max_length=2)
            )
        super(JqSplitDateTimeField, self).__init__(all_fields, *args, **kwargs)
    
    def compress(self, data_list):
        """
        Takes the values from the MultiWidget and passes them as a
        list to this function. This function needs to compress the
        list into a single object to save.
        """
        if data_list:
            if not (int(data_list[1])>0 and int(data_list[1])<24):
                raise forms.ValidationError("Podana godzina jest błędna.")
            if not (int(data_list[2])>0 and int(data_list[2])<60):
                raise forms.ValidationError("Podana minuta jest błędna.")
            input_time = strptime("%s:%s"%(data_list[1], data_list[2]), "%H:%M")
            datetime_string = "%s %s" % (data_list[0], strftime('%H:%M', input_time))
            print "Datetime: %s"%datetime_string
            return datetime_string
        return None