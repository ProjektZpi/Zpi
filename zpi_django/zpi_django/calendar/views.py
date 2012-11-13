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
def calendar2(request):
    now = datetime.datetime.now()
    return calendar(request,now.year,now.month) 

@csrf_exempt
def calendar(request, year, month):
    if request.user.is_authenticated():
        my_events = Calendar.objects.filter(event__start_date__year=year, event__start_date__month=month, user=request.user.pk)  
        my_events=my_events.order_by('event__start_date')
        
        
        year=int(year)
        month= int(month)
        
        next_month=month+1
        next_year=year+1
        previous_month=month-1
        previous_year=year-1
        cal = WorkoutCalendar(my_events).formatmonth(year, month)
        
        return render_to_response('calendar/calendar.html', {'calendar': mark_safe(cal), 'my_events':my_events, 'next_month':next_month, 'next_year':next_year,'previous_month':previous_month, 'previous_year':previous_year, 'month':month, 'year':year}, context_instance=RequestContext(request))
    else:
        return redirect('/')

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
         



