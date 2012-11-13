# -*- coding: utf8 -*-
from django.shortcuts import render_to_response, HttpResponse, redirect, RequestContext
from django.utils import simplejson
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from zpi_django.user_profile.models import UserProfile
from auth_forms import RegisterForm, RegisterFormAdvanced, LoginForm

def login_view(request):
    if request.is_ajax():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            to_json = {"response": "",}
        else:
            to_json = {"response": "błędny login i/lub hasło",}
            
            
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')

def logout_view(request):
    logout(request)
    return redirect('/')

def login_form_alternative(request):
    if 'next' in request.GET :
        next_page = request.GET['next']
        print next_page
    #print next_page
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST['next_page']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(next_page)
            else:
                # Return a 'disabled account' error message
                return redirect('/')
        else:
            # Return an 'invalid login' error message.
            login_form_alternative = LoginForm(request.POST)
            return render_to_response('auth/login.html', {'error':'Podano błędny login i/lub hasło','login_form_alternative':login_form_alternative,'next_page':next_page}, context_instance=RequestContext(request))

    else :
        login_form_alternative = LoginForm()
        return render_to_response('auth/login.html', {'login_form_alternative':login_form_alternative,'next_page':next_page,}, context_instance=RequestContext(request))
def register_view(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        register_form_advanced = RegisterFormAdvanced(request.POST)
        if register_form.is_valid() and register_form_advanced.is_valid():
            user = register_form.cleaned_data
            new_user = User.objects.create_user(user['username'], user['email'], user['password'])
            new_user.first_name = user['first_name']
            new_user.last_name = user['last_name']
            new_user.save()
            
            return redirect('/')
    else:
        register_form = RegisterForm()
        register_form_advanced = RegisterFormAdvanced()
    return render_to_response('auth/registration.html', {'register_form':register_form,'register_form_advanced':register_form_advanced}, context_instance=RequestContext(request))