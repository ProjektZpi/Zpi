# -*- coding: utf8 -*-
from django import forms
from django.contrib.auth.models import User

from zpi_django.user_profile.models import UserProfile

class EditFirstLastName(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name',)
        
class EditPassword(forms.ModelForm):
    old_password = forms.CharField(label="Bieżące", widget=forms.PasswordInput)
    password = forms.CharField(label="Nowe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtórz nowe", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('old_password','password','password2',)

class EditEmail(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)    

class EditCity(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('city',)

class EditAvatar(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)  