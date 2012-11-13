#!/usr/bin/python

from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Menu, Exhibit, Photo, Article
from tiff2012.views import get_content_from_template
from tiff2012.views import make_lang

def texts_by_slug(request, slug):
    template = Menu.objects.get(slug=slug).template

    return get_content_from_template(request,template,slug)


def artist_detail(request, artist_id):
    make_lang(request)
    artist = Exhibit.objects.get(id = artist_id)
    photos = Photo.objects.filter(artist = artist)
    path = request.path
    current_url = path.split('/')
    my_path = "/"+current_url[1]+"/"+current_url[2]+"/"
    return render_to_response('content/artist_detail.html',
                              {'current_url':my_path,'artist_name':artist.artist,'full_desc':artist.full_desc, 'artist_photo':artist.artist_photo, 'photos':photos},
                              context_instance=RequestContext(request)
                              )

def one_article(request, article_id):
    make_lang(request)
    path = request.path
    current_url = path.split('/')
    my_path = "/"+current_url[1]+"/"+current_url[2]+"/"
    article = Article.objects.get(id=article_id)
    return render_to_response('content/one_article.html',
                              {'current_url': my_path,'article':article,},
                              context_instance=RequestContext(request))
   