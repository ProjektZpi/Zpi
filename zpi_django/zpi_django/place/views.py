from django.contrib.gis.geos import fromstr
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from zpi_django.cities.models import City
from zpi_django.events.models import Event
from zpi_django.place.addPlace import addPlace
from zpi_django.place.models import Place

def maps(request):
    return render_to_response("places/add_Place.html")


@csrf_exempt
def modify_place(request,place_id):
    ev=Event.objects.get(id=1)
    place=Place.objects.get(id=place_id)
    print 'modify Place'
    if request.is_ajax(): 
        print 'ajax' 
        adr=request.POST.get('address',"")
        lat=request.POST.get("lat","")
        lng=request.POST.get("lng","")
        current_city=request.POST.get("city","")         
        if place.address!=adr:
            place.address=adr
        p=fromstr("POINT(%s %s)" % (lng,lat))
        place.location=p
        
        query=City.objects.filter(name=current_city)[:1]
        city=City.objects.get(id=place.city.id)
        if query!=city:
            print 'pierwszy if'
            print query
            print city
            if(query):
                print 'place.city=city'
                place.city=city
            else:
                print 'nowe miasto'
                c=City.objects.create(name=current_city)
                place.city=c
        print "miejsce zmienione"                   
        place.save()
       
        return HttpResponse(simplejson.dumps('ok'), mimetype='application/json')
    else:
        return render_to_response("places/edit_place.html",{'event':ev}, context_instance=RequestContext(request))
    





@csrf_exempt
def add_Place(request):
    if(request.is_ajax()):      
        if request.method == 'POST':
            print request.POST
            adr=request.POST.get('address',"")
            lat=request.POST.get("lat","")
            lng=request.POST.get("lng","")
            current_city=request.POST.get("city","")
            query=City.objects.filter(name=current_city)
            p=fromstr("POINT(%s %s)" % (lng,lat))
            if(query):  
                city=City.objects.get(name=current_city)          
                place=Place(address=adr,city=city, location=p)
                place.save();
            else:
                city=City.objects.create(name=current_city)
                place=Place(address=adr,city=city, location=p);
                place.save();
                
            return HttpResponse(simplejson.dumps(dict(id_place=place.id)), mimetype='application/json')
   #         lat=smart_unicode(request.POST.get('lat',""),encoding="utf-8",strings_only=False,errors="strict" )
   #         lng=smart_unicode(request.POST.get('lng',""),encoding="utf-8",strings_only=False,errors="strict" )


        else:
            message = "error"
            json = simplejson.dumps(message)
            return HttpResponse(json, mimetype='application/json')
    else:
        message = "error"
        json = simplejson.dumps(message)
        return HttpResponse(json, mimetype='application/json')
    

        
   
