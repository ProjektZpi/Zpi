import calendar
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class WorkoutCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            body=""   
            counter=0; 
            if day in self.workouts:
                counter=counter+1
                cssclass += ' filled'
                title=""
                # gdy jest wiecej niz jedno wydarzenie
                if len(self.workouts[day])>1:
                    title+="<table id='events'>"
                    title+="<tr><td>Nazwa:</td><td>Start:</td><td>Miejsce</td></tr>"
                    for i in self.workouts[day]:
                        title+="<tr><td>"+i.event.name+"</td><td>"+i.event.start_date.strftime('%Y-%m-%d')+"</td><td>"+i.event.place.address+"</td></tr>"
                    title+="</table>" 
                    body += '<br/><a class="tooltip" title="'+title+'">'+str(len(self.workouts[day]))+' wydarzenia</a>'
                #gdy jest jedno wydarzenie
                else:
                    #gdy nazwa jest za dluga
                    if len(self.workouts[day][0].event.name) >10:
                        title+="<table id='events'><tr><td>Nazwa:</td><td>Start:</td><td>Miejsce</td></tr>"
                        title+="<tr><td>"+self.workouts[day][0].event.name+"</td><td>"+self.workouts[day][0].event.start_date.strftime('%Y-%m-%d')+"</td><td>"+self.workouts[day][0].event.place.address+"</td></tr></table>"
                        body += '<br/><a href="/wydarzenia/informacje/'+str(self.workouts[day][0].event.id) +'" class="tooltip" title="'+title+'">'+self.workouts[day][0].event.name[0:10]+"...</a>"
                    # gdy nazwa jest krotka    
                    else:
                        title="<table id='events'><tr><td>Nazwa:</td><td>Start:</td><td>Miejsce</td></tr>"
                        title+="<tr><td>"+self.workouts[day][0].event.name+"</td><td>"+self.workouts[day][0].event.start_date.strftime('%Y-%m-%d')+"</td><td>"+self.workouts[day][0].event.place.address+"</td></tr></table>"
                        body += '<br/><a href="/wydarzenia/informacje/'+str(self.workouts[day][0].event.id) +'" class="tooltip" title="'+title+'">'+self.workouts[day][0].event.name+"</a>"
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))

            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(WorkoutCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        field = lambda workout: workout.event.start_date.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s"  >%s</td>' % (cssclass, body)