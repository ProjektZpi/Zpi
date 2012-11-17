# -*- coding: utf8 -*-
from django.shortcuts import render_to_response, HttpResponse, redirect, RequestContext
from django.utils.safestring import mark_safe
from zpi_django.calendar.WorkoutCalendar  import WorkoutCalendar
from zpi_django.calendar.models import Calendar
from zpi_django.events.models import Event
from zpi_django.statistics.views import update
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson



@csrf_exempt
def join_json(request):  
#Zapisywanie do bazy
    user= request.user
    event_id=request.POST.get('event_id')
    event = Event.objects.get(id=event_id)
    calendar=Calendar(user=user, event=event)
    calendar.save()


    to_json = {
               
               }
    json = simplejson.dumps(to_json);

   #odswiezenie statystyk
    update_statistic = update(event_id)
    
    return HttpResponse(json, mimetype='application/json')
         
         
@csrf_exempt
def calendar_json(request):  

    year=request.POST.get('year')
    month=request.POST.get('month')
    
    year=(int)(year)
    month=(int)(month)

    my_events = Calendar.objects.filter(event__start_date__year=year, event__start_date__month=month, user=request.user.pk)  
    my_events=my_events.order_by('event__start_date')
    


    next_month=month+1
    next_year=year+1
    previous_month=month-1
    previous_year=year-1
    cal = WorkoutCalendar(my_events).formatmonth(year, month)
    
    #lista eventow
    my_events = Calendar.objects.filter(event__start_date__year=year, event__start_date__month=month, user=request.user.pk)  
    my_events=my_events.order_by('event__start_date')
    
    event_list=""
    if my_events.count()!=0:
       for my_event in my_events:
           event_list+="<li><a href='/wydarzenia/informacje/"+str(my_event.event.id)+"'><b>"+my_event.event.name+"</b> "+str(my_event.event.start_date)+"</a></li>"
    else:
        event_list="<a> Nie jesteś zapisany na żadne wydarzenie</a>"
    
    
    to_json = {
               "calendar":mark_safe(cal),
               "event_list": event_list,
               }
    json = simplejson.dumps(to_json);

    return HttpResponse(json, mimetype='application/json')


