# -*- coding: utf8 -*-
from django.shortcuts import render_to_response, RequestContext, HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from zpi_django.events.models import Event
from zpi_django.event_feedbacks.models import EventFeedback
from zpi_django.statistics.models import AuthorStatistic
from django.contrib.auth.models import User
from django.db.models import Avg
import datetime
from django.core import serializers
import datetime
from django.utils import timezone
from zpi_django.statistics.views import update

@csrf_exempt
def show_feedbacks(request,event_id):
    event_to_feedback = Event.objects.get(id=event_id)
    atmosphere=EventFeedback.objects.filter(event=event_to_feedback).aggregate(Avg('atmosphere'))
    organisation=EventFeedback.objects.filter(event=event_to_feedback).aggregate(Avg('organisation'))
    
    can_write_comments=False
    if request.user.is_authenticated():
        can_write_comments=True
    error=""
    #sprawdzenie prawa do zapisu
    can_write=True


    if request.user.is_authenticated():
        if event_to_feedback.start_date>timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone()):
           can_write=False
           error="Nie możesz oceniać wydarzenia przed jego rozpoczęciem"
        else:
            is_user=EventFeedback.objects.filter(user= request.user)
            if is_user.count()>0:
               can_write=False
               error="Wysłałeś już ocenę tego wydarzenia"
    else: 
         can_write=False
         error="Musisz być zalogowany aby dodawać oceny"         
        
    if atmosphere["atmosphere__avg"]==None:     
        atmosphere_number="Brak oceny"
        atmosphere_avg=""
    else:
        atmosphere_number=atmosphere["atmosphere__avg"]
        atmosphere_avg=" \n"
    
        atmosphere_counter=0
        for i in range(int(atmosphere["atmosphere__avg"]*4-1)):
                atmosphere_avg+="<input type='radio' class='star {split:4}' name='atmosphere_star' disabled='disabled'/> \n"
                atmosphere_counter=atmosphere_counter+1
        atmosphere_avg+="<input type='radio' class='star {split:4}' name='atmosphere_star'  disabled='disabled' checked='checked'/> \n"
        atmosphere_counter=atmosphere_counter+1
        for i in range(int(20-(atmosphere["atmosphere__avg"]*4))):
             if atmosphere_counter<20:  
                atmosphere_avg+="<input type='radio' class='star {split:4}' name='atmosphere_star'  disabled='disabled'/> \n"
                atmosphere_counter=atmosphere_counter+1
       
                
    if organisation["organisation__avg"]==None:     
        organisation_number="Brak oceny"
        organisation_avg=""
    else:    
        organisation_number=organisation["organisation__avg"]
        organisation_avg=" \n"
        organisation_counter=0
        for i in range(int(organisation["organisation__avg"]*4-1)):
                organisation_avg+="<input type='radio' class='star {split:4}' name='organisation_star' disabled='disabled'/> \n"
                organisation_counter=organisation_counter+1
        organisation_avg+="<input type='radio' class='star {split:4}' name='organisation_star'  disabled='disabled' checked='checked'/> \n"
        organisation_counter=organisation_counter+1
        for i in range(int(20-(organisation["organisation__avg"]*4))):
                if organisation_counter<20:
                    organisation_avg+="<input type='radio' class='star {split:4}' name='organisation_star'  disabled='disabled'/> \n"
                    organisation_counter=organisation_counter+1

    return render_to_response('event_feedbacks/show_feedbacks.html', { 'atmosphere_avg':atmosphere_avg, 'organisation_avg':organisation_avg, 'atmosphere': atmosphere_number, 'organisation':organisation_number, 'event_id': event_id, "can_write":can_write,  "error":error, "event":event_to_feedback },
                                  context_instance=RequestContext(request))
    
    
    
    
    
    
    #JSON
@csrf_exempt
def add_feedback_json(request):


    #Zapisywanie do bazy
        user= request.user
        event_id=request.POST.get('event_id')
        event = Event.objects.get(id=event_id)
        atmosphere=request.POST.get('atmosphere')
        organisation=request.POST.get('organisation')
        if atmosphere==None:
            atmosphere=0
        if organisation==None:
            organisation=0
        event_feedbacks=EventFeedback(user=user, event=event, atmosphere=atmosphere, organisation=organisation)
        event_feedbacks.save()


         
       #odświeżanie statystyk
       
        event_to_feedback = Event.objects.get(id=event_id)
        atmosphere=EventFeedback.objects.filter(event=event_to_feedback).aggregate(Avg('atmosphere'))
        organisation=EventFeedback.objects.filter(event=event_to_feedback).aggregate(Avg('organisation'))
        
       
        
        if atmosphere["atmosphere__avg"]==None:     
            atmosphere_number="Brak oceny"
            atmosphere_avg=""
        else:
            atmosphere_number=atmosphere["atmosphere__avg"]
            atmosphere_avg=" \n"
        
            atmosphere_counter=0
            for i in range(int(atmosphere["atmosphere__avg"]*4-1)):
                    atmosphere_avg+="<input type='radio' class='star {split:4}' name='atmosphere_star' disabled='disabled'/> \n"
                    atmosphere_counter=atmosphere_counter+1
            atmosphere_avg+="<input type='radio' class='star {split:4}' name='atmosphere_star'  disabled='disabled' checked='checked'/> \n"
            atmosphere_counter=atmosphere_counter+1
            for i in range(int(20-(atmosphere["atmosphere__avg"]*4))):
                 if atmosphere_counter<20:  
                    atmosphere_avg+="<input type='radio' class='star {split:4}' name='atmosphere_star'  disabled='disabled'/> \n"
                    atmosphere_counter=atmosphere_counter+1
           
                    
        if organisation["organisation__avg"]==None:     
            organisation_number="Brak oceny"
            organisation_avg=""
        else:    
            organisation_number=organisation["organisation__avg"]
            organisation_avg=" \n"
            organisation_counter=0
            for i in range(int(organisation["organisation__avg"]*4-1)):
                    organisation_avg+="<input type='radio' class='star {split:4}' name='organisation_star' disabled='disabled'/> \n"
                    organisation_counter=organisation_counter+1
            organisation_avg+="<input type='radio' class='star {split:4}' name='organisation_star'  disabled='disabled' checked='checked'/> \n"
            organisation_counter=organisation_counter+1
            for i in range(int(20-(organisation["organisation__avg"]*4))):
                    if organisation_counter<20:
                        organisation_avg+="<input type='radio' class='star {split:4}' name='organisation_star'  disabled='disabled'/> \n"
                        organisation_counter=organisation_counter+1  
              
            to_json = {
                       "info":"Ocena została dodana",
                       "atmosphere_number":atmosphere_number,
                       "atmosphere_avg":atmosphere_avg,
                        "organisation_number":organisation_number,
                       "organisation_avg": organisation_avg
                       }
            json = simplejson.dumps(to_json);
            
            #odświeżenie statystyk autora
            update_statistic = update(event_id)
            
            
            return HttpResponse(json, mimetype='application/json')

