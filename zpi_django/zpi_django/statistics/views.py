# -*- coding: utf8 -*-
from django.shortcuts import render_to_response, HttpResponse, redirect, RequestContext
from django.contrib.auth.models import User
from zpi_django.events.models import Event, Category
from zpi_django.statistics.models import AuthorStatistic, Gustomierz
from zpi_django.event_feedbacks.models import EventFeedback
from zpi_django.tags.models import EventTag
from zpi_django.events.models import Event
from zpi_django.calendar.models import Calendar
from django.contrib.auth.models import User
from django.db.models import Avg
import datetime



def update(event_id):
     # update statystyk autora
        #pobieranie id eventu z parametru metody
        event = Event.objects.get(id=event_id)
        

        
        #pobieranie eventów autora
        author_events=Event.objects.filter(user=event.user)
        
        
        #liczenie średniej ze wszystkich eventów autora
        atmosphere_avg=EventFeedback.objects.filter(event__in=author_events).aggregate(Avg('atmosphere'))
        organisation_avg=EventFeedback.objects.filter(event__in=author_events).aggregate(Avg('organisation'))
        
        #liczenie ogolne średniej
        overall = (atmosphere_avg["atmosphere__avg"]+organisation_avg["organisation__avg"])/2
        
        #liczenie "wezme udzial"
        join_count=Calendar.objects.filter(event__in=author_events).count()
        
        #sprawdzanie czy rekord juz istnieje
        is_author= AuthorStatistic.objects.filter(user=event.user)
        if is_author.count()==0:
            #dodaj nowy rekord
            author_statistic=AuthorStatistic(user=event.user,  atmosphere_avg=atmosphere_avg["atmosphere__avg"],  organisation_avg=organisation_avg["organisation__avg"], overall=overall, liked_count=join_count)
            author_statistic.save()  
        else:
            #aktualizuj
            record_to_update = AuthorStatistic.objects.get(user=event.user)
            record_to_update.atmosphere_avg=atmosphere_avg["atmosphere__avg"]
            record_to_update.organisation_avg=organisation_avg["organisation__avg"]
            record_to_update.liked_count=join_count   
            record_to_update.save()
            
            
def gustomierz(user_id, number_of_tags):
        user = User.objects.filter(id=user_id)
        user=user[0]
        #wszystkie tagi slownik
        tags = {}
        #wyszukiwanie ocen
        for event in EventFeedback.objects.filter(user=user):
            avg = (event.atmosphere+float(event.organisation))/2
            for tag in EventTag.objects.filter(event=event.event):
                if tags.has_key(tag.name):
                    value= tags[tag.name]+avg
                    tags[tag.name] = value
                else:
                    tags[tag.name]=avg
        #czyszczenie starych wpisów
        Gustomierz.objects.filter(user=user).delete() 
                   
        licznik=0          
        for key, value in sorted(tags.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            licznik=licznik+1
            if licznik<(float(number_of_tags)+1):
                gustomierz=Gustomierz(user=user,  tag=key, tag_number=licznik, overall_avg=value)
                gustomierz.save()  
           
def recommendedEvents(user_id):
        #pobieranie usera
        user = User.objects.filter(id=user_id)
        user=user[0]
        tag1=""
        tag2=""
        gustomierz = Gustomierz.objects.filter(user=user).order_by("tag_number")
        if gustomierz.count()>=2:
            tag1=gustomierz[0].tag
            tag2=gustomierz[1].tag
        if gustomierz.count()==1:
            tag1=gustomierz[0].tag

        


        
        now = datetime.datetime.now()
        show_events= list() 
        #wyszukiwanie po tagu nr 1
        number_events=0
        try:
            tags1 = EventTag.objects.filter(name=tag1, event__start_date__gt=now, event__place__city__name=user.get_profile().city).order_by("event__start_date")
        except EventTag.DoesNotExist:
            try:
                tags1 = EventTag.objects.filter(name=tag1, event__start_date__gt=now).order_by("event__start_date")
            except EventTag.DoesNotExist:
                tags1=""

        if tags1!="":
            if tags1.count()>=2:        
                show_events.append(tags1[0].event)
                number_events=1
                if tags1[0].event!=tags1[1].event:
                    show_events.append(tags1[1].event)
                    number_events=2
            if tags1.count()==1:    
                show_events.append(tags1[0].event)
                number_events=1
        

        #wyszukiwanie wydarzen dla tagu nr 2     
        try:
            tags2 = EventTag.objects.filter(name=tag2, event__start_date__gt=now, event__place__city__name=user.get_profile().city).order_by("event__start_date")
        except EventTag.DoesNotExist:
            try:
                tags2 = EventTag.objects.filter(name=tag2, event__start_date__gt=now).order_by("event__start_date")
            except EventTag.DoesNotExist:
                tags2=""

        if tags2!="" and number_events>0:
            if tags2.count()>=2 and number_events==1:        
                if(tags2[0].event!=show_events[0]):
                    show_events.append(tags2[0].event)
                if(tags2[1].event!=show_events[0] and tags2[1].event!=show_events[1]):
                    show_events.append(tags2[1].event)
            if tags2.count()==1: 
                if  len(show_events)>=2:  
                    if(tags2[0].event!=show_events[0] and tags2[0].event!=show_events[1]):
                        show_events.append(tags2[0].event)
                else:
                    if(tags2[0].event!=show_events[0]):
                        show_events.append(tags2[0].event)
        else:
            if number_events==0:
                if  len(show_events)>=2:  
                        show_events.append(tags2[0].event)
                        if(tags2[0].event!=tags2[1].event):
                            show_events.append(tags2[1].event)
                else:
                    if len(show_events)==1:
                        show_events.append(tags2[0].event)
                    
        return show_events