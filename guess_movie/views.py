# -*- coding: utf-8 -*-
__author__ = 'olga'
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
import json

from models import Frame

def add(request):
    if request.method == 'GET':
        return render_to_response("add_frame.html", {})
    elif request.method == 'POST':
        file = request.FILES['file']
        frame = Frame()
        frame.file = file
        frame.movie_tmdb_id = request.POST['movie_id']
        frame.movie_tmdb_name = request.POST['movie_name']
        frame.save()
        return render_to_response("add_frame.html", {'result': u'Файл был успешно загружен'})


def guess(request):
    if request.method == 'GET':
        frame = Frame.objects.order_by('?')[0]
        return render_to_response("guess_frame.html", {'img_src': frame.file.url, 'frame_id': frame.id})
    elif request.method == 'POST':
        frame = Frame.objects.get(id=int(request.POST['frame_id']))
        if str(frame.movie_tmdb_id) == str(request.POST['movie_id']):
            return HttpResponse(json.dumps({'success': True, 'movie_name': frame.movie_tmdb_name}))
        else:
            return HttpResponse(json.dumps({'success': False, 'movie_name': frame.movie_tmdb_name}))


def movies_list(request):
    data = [{'value': u'Фантомас', 'id': 1}, {'value': u'Фантомас разбушевался', 'id': 2}]
    return HttpResponse(json.dumps(data), mimetype="application/json")
