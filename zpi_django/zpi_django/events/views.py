# -*- coding: utf8 -*-
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.models import Avg
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from zpi_django.calendar.models import Calendar
from zpi_django.cities.models import City
from zpi_django.event_comments.models import EventComment
from zpi_django.event_feedbacks.models import EventFeedback
from zpi_django.events.events_forms import AddEventForm, AddPhotoForm
from zpi_django.events.models import Event, Category
from zpi_django.statistics.models import AuthorStatistic
from zpi_django.statistics.views import gustomierz, update, recommendedEvents
from zpi_django.tags.models import EventTag
from zpi_django.tags.tag_form import AddTagForm
import datetime

def show_events(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    cities = City.objects.all()
    return render_to_response('events/events_grid.html', { 'events': events, 'categories':categories, 'cities':cities },
                                  context_instance=RequestContext(request))


@csrf_exempt    
def modify_event(request,event_id):
    event=Event.objects.get(id=event_id)
    e_id=event.id
    tagFormset=inlineformset_factory(Event,EventTag,can_delete=True,extra=1)       
    print event.place.location.x  
    if request.method == 'POST':
        eventform=AddEventForm(request.POST,request.FILES,instance=event)
        tagform=tagFormset(request.POST,instance=event)       
        eventform.save()
        tagform.save()

        
        print 'zmienione'
        url = reverse('zpi_django.events.views.event_detail', kwargs={'event_id': e_id})
        return HttpResponseRedirect(url)   
    else:
            eventform=AddEventForm(instance=event)
            tagform=tagFormset(instance=event)

            return render_to_response("events/edit_event.html", {'event':event,'add_event_form': eventform,'add_tag_form':tagform
                                                                      }, context_instance=RequestContext(request))    
    
    



@csrf_exempt
def add_event(request):
    if request.user.is_authenticated():
        current_user= request.user 
        if request.method == 'POST':
            event=Event(user=current_user)
                     
            event_form = AddEventForm(request.POST,request.FILES,instance=event)
            photo_form = AddPhotoForm(request.POST,request.FILES)
            add_tag_form=AddTagForm(request.POST)
            event=event_form.save(commit=False)
            event.user=current_user
            event.save()
            
            photos= photo_form.save(commit=False)
            photos.event =event
            photos.save()
            tags=request.POST.get('tags-name')
            tags=tags.split(",") 
            for tag in tags:
                tag= tag.replace(' ','')

                all_tags = EventTag.objects.filter(name=tag)
                if all_tags.count()==0:
                    a1 = EventTag(name=tag)
                    a1.save()
                    a1.event.add(event)

                else:
                    a1 = EventTag.objects.get(name=tag)
                    a1.event.add(event)
                    
            event_id=event.id
            site= 'http://%s%s' % (Site.objects.get_current().domain,
                               reverse('zpi_django.events.views.event_detail', kwargs={'event_id':event_id}))
    #        print site        
            return render_to_response("events/add_succesfull.html", {
                'message': 'Wydarzenie zostało dodane!','url':site
            }, context_instance=RequestContext(request))   
    
        else:
            event_form=AddEventForm()
            photo_form = AddPhotoForm()
            add_tag_form=AddTagForm(prefix='tags')
            return render_to_response('events/add_event_wizard.html', { 'add_event_form': event_form, 'add_photo_form':photo_form,
                                                                       'add_tag_form':add_tag_form},
                                      context_instance=RequestContext(request))
    else:
                        return render_to_response('auth/registration.html',
                                      context_instance=RequestContext(request))
@csrf_exempt
def event_detail(request,event_id):
    event = Event.objects.get(id=event_id)
    comments=EventComment.objects.filter(event=event)
    

            
            
    #pobieranie statystyk autora
    author_statistic = AuthorStatistic.objects.filter(user=event.user)
    if author_statistic.count()==0:
        author_statistic="brak ocen"
    else:
        author_statistic= author_statistic[0].overall
   
    
    can_write_comments=False
    if request.user.is_authenticated():
        can_write_comments=True

    # kod do buttonu "wezmę udział"
    can_join=False
    if can_write_comments:
        can_join=True
        event_to_join = Event.objects.get(id=event_id)
        is_user=Calendar.objects.filter(user= request.user, event=event_to_join)
        if is_user.count()>0:
            can_join=False
        
        
    # kod odpowiedzialny za feedback
    event_to_feedback = Event.objects.get(id=event_id)
    atmosphere=EventFeedback.objects.filter(event=event_to_feedback).aggregate(Avg('atmosphere'))
    organisation=EventFeedback.objects.filter(event=event_to_feedback).aggregate(Avg('organisation'))
    
    can_write=True
    error=""
    #sprawdzenie prawa do zapisu
    if request.user.is_authenticated():
        if event_to_feedback.start_date>timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone()):
            can_write=False
            error="Nie możesz oceniać wydarzenia przed jego rozpoczęciem"
        else:
            is_user=EventFeedback.objects.filter(user= request.user, event=event_to_feedback)
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
                    
    #aktualizowanie gustomierza
    update_gustomierz = gustomierz(request.user.id,2)
    
    return render_to_response('events/event_detail.html', { 'event': event, 'comments': comments, 'can_write':can_write, "can_write_comments": can_write_comments, 'atmosphere_avg':atmosphere_avg, 'organisation_avg':organisation_avg, 'atmosphere': atmosphere_number, 'organisation':organisation_number, 'event_id': event_id,  "error":error, "event":event_to_feedback, 'can_join':can_join, 'author_statistic':author_statistic },
                                  context_instance=RequestContext(request)) 

 