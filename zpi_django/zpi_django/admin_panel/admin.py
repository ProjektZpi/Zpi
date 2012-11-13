#-*- coding: utf-8 -*-
from django.contrib.gis import admin
# Tutaj rejestrujemy funkcje admina, wygląd jak i decydujemy jakie modele mają być używane w panelu. 

# APP cities
from zpi_django.cities.models import City
admin.site.register(City)


from zpi_django.place.models import Place
admin.site.register(Place,admin.OSMGeoAdmin)
###############################################################################################################
# APP events
from zpi_django.events.models import Event, Category, EventPhoto

class EventPhotoInline(admin.StackedInline):
    model = EventPhoto
    
class EventAdmin(admin.ModelAdmin):
        
    inlines = [EventPhotoInline]
    list_display = ('name','category','start_date','end_date','introduction')
    list_filter = ('start_date','end_date')

admin.site.register(Category)
admin.site.register(Event, EventAdmin)

###############################################################################################################
# APP event_comments
from zpi_django.event_comments.models import EventComment
admin.site.register(EventComment)

###############################################################################################################
# APP event_feedbacks
from zpi_django.event_feedbacks.models import EventFeedback
admin.site.register(EventFeedback)
###############################################################################################################
# APP event_observators
from zpi_django.event_observators.models import EventObservator
admin.site.register(EventObservator)

###############################################################################################################
# APP statistics
from zpi_django.statistics.models import AuthorStatistic
admin.site.register(AuthorStatistic)

from zpi_django.statistics.models import Gustomierz
admin.site.register(Gustomierz)



###############################################################################################################
# APP tags
from zpi_django.tags.models import EventTag
admin.site.register(EventTag)

###############################################################################################################
# APP user_profile
from zpi_django.user_profile.models import UserProfile
admin.site.register(UserProfile)

###############################################################################################################
# APP calendar
from zpi_django.calendar.models import Calendar
admin.site.register(Calendar)

###############################################################################################################
# APP friends
from zpi_django.friends.models import FriendList
admin.site.register(FriendList)
