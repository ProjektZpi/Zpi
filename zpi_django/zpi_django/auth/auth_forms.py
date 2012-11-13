# -*- coding: utf8 -*-

from django import forms

from django.contrib.auth.models import User
from zpi_django.user_profile.models import UserProfile


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password',)
        widgets = {
            'password': forms.PasswordInput(),
        }
class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Pseudonim *")
    password = forms.CharField(label="Hasło *", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtórz hasło *", widget=forms.PasswordInput)
    email = forms.EmailField(label="Adres e-mail *")
    
    def __init__(self, *args, **kw):
        super(forms.ModelForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'username',
            'password',
            'password2',
            'email',
            'first_name',
            'last_name',
        ]
    
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','email')

    error_messages = {
        'duplicate_username': ("Pseudonim zajęty. Wybierz inny"),
        'password_mismatch': ("Podane hasła nie są takie same."),
    }
    


    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
   
    def clean_password2(self):
        password = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data["password2"]
        if password != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2
        
class RegisterFormAdvanced(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user','avatar')

        
        