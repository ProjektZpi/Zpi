# -*- coding: utf8 -*-
from django.shortcuts import render_to_response, RequestContext, HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from zpi_django.events.models import Event
from zpi_django.event_comments.models import EventComment
from django.contrib.auth.models import User
import datetime
from datetime import datetime
from django.utils import formats



@csrf_exempt
def add_comment_json(request):
    
    
        user= request.user
        message=request.POST.get('comment')
        event_id=request.POST.get('event_id')
        event = Event.objects.get(id=event_id)


        comments=EventComment(user=user, event=event, comment= message)
        comments.save()
    

        event_to_comment = Event.objects.get(id=event_id)
        
        comments=EventComment.objects.filter(event=event_to_comment)
        
        content="<p><br/>Komentarze do wydarzenia:</p> <table id='comments'>"
        for comment in comments:

            content+="<tr> <td colspan='3'><hr class='table_hr'/></td>"
            content+="</tr><tr> <td class='comment_author_avatar'>"
            if comment.user.get_profile().avatar:
                content+="<img src='"+comment.user.get_profile().avatar.url+"' width='100%'/>"
            else:
                if comment.user.get_profile().gender == 'K':
                    content+="<img src='/site_media/images/women_avatar_default.jpg' width='100%' />"
                else:
                    content+="<img src='/site_media/images/men_avatar_default.jpg'  width='100%'/>"
            content+="</td><td class='hr_vertical'></td>"
            content+="<td class='comment_author'>"
            content+= comment.user.username
            content+="<br/>" 
            formatted_datetime = formats.date_format(comment.date, "SHORT_DATETIME_FORMAT")
            content+= formatted_datetime    
            content+="</td></tr><tr><td colspan='2'></td> <td class='comment_content'>"
            content+= comment.comment
            content+="</td></tr>"
        content+="</table>"  
        to_json = {
                   "id":event_id,
                   "content":content
                   }
        json = simplejson.dumps(to_json);

        return HttpResponse(json, mimetype='application/json')

