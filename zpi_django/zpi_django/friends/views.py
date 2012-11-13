# -*- coding: utf8 -*-

from django.shortcuts import render_to_response, HttpResponse, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from zpi_django.friends.models import FriendList
from zpi_django.events.models import Event
from django.db.models import Q

def is_friend(user1, user2):
    flist = FriendList.objects.filter(Q(user=user1, friend=user2) | Q(user=user2, friend=user1))
    if flist:
        if flist[0].confirmed:
            return 1 # sa znajomymi
        else:
            return 2; # nie potwierdzono
    else:
        return 0 # nie sa znajomymi

def profile_information(request, user_id):
    target_user = User.objects.get(id=user_id)
    # wydarzenia target_usera
    my_events = Event.objects.filter(user=user_id).order_by('-start_date')
    # znajomi target_usera
    my_friends = FriendList.objects.filter(user=user_id).order_by('friend__username')
    if request.user.is_anonymous():
        are_friends = -2 # nie zalogowano
    elif request.user == target_user:
        are_friends = -3 # moj profil
    else:
        are_friends = is_friend(request.user.id, user_id)
    
    print are_friends
    print request.user

    return render_to_response('friends/profile_information.html', {'are_friends':are_friends,'my_events':my_events,'my_friends':my_friends,'target_user':target_user,}, context_instance=RequestContext(request))  

def remove_from_friend(request, user_id):
    from django.utils import simplejson
    if request.is_ajax():
        FriendList.objects.filter(Q(friend=user_id) | Q(user=user_id)).delete()
        to_json = {"response": "Usunięto ze znajomych",}         
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')

def add_to_friend(request, user_id):
    from django.utils import simplejson
    if request.is_ajax():
        FriendList(user=request.user,friend=User.objects.get(id=user_id), confirmed=0).save()
        FriendList(friend=request.user,user=User.objects.get(id=user_id), confirmed=0).save()
        to_json = {"response": "Dodano do znajomych",}         
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')