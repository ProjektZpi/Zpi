# -*- coding: utf8 -*-

from django.shortcuts import render_to_response, HttpResponse, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from zpi_django.statistics.views import recommendedEvents
from zpi_django.statistics.models import AuthorStatistic

from edit_profile_form import EditFirstLastName, EditPassword, EditEmail, EditCity, EditAvatar
from zpi_django.events.models import Event
from zpi_django.friends.models import FriendList
from zpi_django.calendar.models import Calendar
from zpi_django.event_comments.models import EventComment
from django.core.validators import email_re
from zpi_django.calendar.WorkoutCalendar  import WorkoutCalendar
from zpi_django.calendar.models import Calendar
from django.utils.safestring import mark_safe
import datetime



@login_required
def my_profile(request):
    user = request.user
    edit_names_form = EditFirstLastName(
            initial = {
                       "first_name": user.first_name,
                       "last_name": user.last_name,
    })
    edit_password_form = EditPassword()
    edit_email_form = EditEmail(
            initial = {
                       "email": user.email,
    })
    edit_city_form = EditCity(
            initial = {
                       "city": user.get_profile().city,
    })
    if request.method == 'POST':
        edit_avatar_form = EditAvatar(request.POST, request.FILES, instance=request.user.get_profile())

        if edit_avatar_form.is_valid():
            edit_avatar_form.save()
            return render_to_response('user_profile/my_profile.html', {'edit_names_form':edit_names_form,'edit_password_form':edit_password_form,'edit_email_form':edit_email_form,'edit_city_form':edit_city_form,'edit_avatar_form':edit_avatar_form,'user':user}, context_instance=RequestContext(request))  

    else:
        edit_avatar_form = EditAvatar(instance=request.user.get_profile())
        
    # najblizsze 4 wydarzenia
    now = datetime.datetime.now()
    close_events = Calendar.objects.filter(user=user.id, event__start_date__gt=now).order_by('event__start_date')[0:3]
    

    
    # moje wydarzenia
    my_events = Event.objects.filter(user=user.id).order_by('-start_date')
    
        
    # znajomi
    my_friends = FriendList.objects.filter(user=user.id).order_by('friend__username')
    

    
    #pobieranie wydarzeń z gustomierza
    recommended_events = recommendedEvents(request.user.id)
    
    #kalendarz
    now = datetime.datetime.now()
    year=now.year
    month= now.month
       
    my_events_calendar = Calendar.objects.filter(event__start_date__year=year, event__start_date__month=month, user=request.user.pk)  
    my_events_calendar=my_events_calendar.order_by('event__start_date')


    next_month=month+1
    next_year=year+1
    previous_month=month-1
    previous_year=year-1
    cal = WorkoutCalendar(my_events_calendar).formatmonth(year, month)
    
    
    
    #punktacja uzytkownika
    user_points = AuthorStatistic.objects.filter(user=request.user)
    if user_points.count()==0:
        user_points="brak ocen"
    else:
        user_points= user_points[0].overall
        
        
    #pobieranie ilosci utworzonych wydarzen
    create_events = Event.objects.filter(user=request.user)  
    create_events=create_events.count()
    
    
    
    #liczba znajomych
    friends = FriendList.objects.filter(user=request.user)  
    
    if (friends.count()-4>0):
        friends_min=friends.count()-4
    else:
        friends_min=0
    friends=friends[friends_min:friends.count()]
    
    
    #liczba komentarzy
    comments = EventComment.objects.filter(user=request.user)
    return render_to_response('user_profile/my_profile.html', {'close_events':close_events,'my_friends':my_friends,'my_events':my_events,'edit_names_form':edit_names_form,'edit_password_form':edit_password_form,'edit_email_form':edit_email_form,'edit_city_form':edit_city_form,'edit_avatar_form':edit_avatar_form,'user':user, 'recommended_events':recommended_events, 'calendar': mark_safe(cal), 'my_events_calendar':my_events_calendar, 'close_events':close_events, 'month':month, 'year':year, 'user_points':user_points, 'create_events':create_events, 'friend_count':friends.count(), 'comments_count':comments.count(), 'friends':friends}, context_instance=RequestContext(request))  


def is_valid_email(email):
    return bool(email_re.match(email))
        
def edit_profile(request, form_id):
    form_id = int(form_id)
    # Jeżeli form = nazwisko i imie
    if form_id == 1:
        if request.is_ajax():
            user = request.user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            if first_name == "":
                first_name = user.first_name
            if last_name == "":
                last_name = user.last_name
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            to_json = {"response": "Twoje dane osobowe zostały zmienione.",}
        else :
            to_json = {"response": "bledy",}
    # Jeżeli form = haslo
    elif form_id == 2:
        if request.is_ajax():
            user = request.user
            old_password = request.POST['old_password']
            password = request.POST['password']
            password2 = request.POST['password2']
            if user.check_password(old_password):
                if password == "" or password2 == "":
                    to_json = {"response": "Musisz wypełnić wszystkie pola.",}
                else:
                    if password == password2:
                        to_json = {"response": "Twoje hasło dostępu zostało zmienione.",}
                        user.set_password(password)
                        user.save()
                    else:
                        to_json = {"response": "Pola z nowym hasłem nie zgadzają się.",}
            else:
                to_json = {"response": "Pole z bieżącym hasłem jest nieprawidłowe.",}
        else :
            to_json = {"response": "bledy",}  
    elif form_id == 3:   
        if request.is_ajax():
            user = request.user
            email = request.POST['email']
            if is_valid_email(email):
                to_json = {"response": "Twój adres email został zmieniony.",}
                user.email = email
                user.save()
            else:
                to_json = {"response": "Podany adres email nie jest prawidłowy.",}
        else :
            to_json = {"response": "bledy",}
    elif form_id == 4:   
        if request.is_ajax():
            user = request.user
            city = request.POST['city']
            if city <> "" and city <> " ":
                to_json = {"response": "Twoje miasto zostało zaktualizowane.",}
                user.get_profile().city = city
                user.get_profile().save()
            else:
                to_json = {"response": "Pole 'Miasto' nie może być puste.",}
        else :
            to_json = {"response": "bledy",}       
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')