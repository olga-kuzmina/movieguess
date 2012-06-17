# -*- coding: utf-8 -*-
__author__ = 'olga'
from django.shortcuts import render_to_response, redirect
from django.http import Http404, HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json

from models import Frame, UserProfile

@login_required
def add(request):
    if request.method == 'GET':
        return render_to_response("add_frame.html", {}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        file = request.FILES['file']
        frame = Frame()
        frame.file = file
        frame.movie_tmdb_id = request.POST['movie_id']
        frame.movie_tmdb_name = request.POST['movie_name']
        frame.save()
        return render_to_response("add_frame.html", {'result': u'Файл был успешно загружен'},
            context_instance=RequestContext(request))


@login_required
def guess(request):
    if request.method == 'GET':
        frame = Frame.objects.order_by('?')[0]
        return render_to_response("guess_frame.html", {'img_src': frame.file.url, 'frame_id': frame.id},
            context_instance=RequestContext(request))
    elif request.method == 'POST':
        frame = Frame.objects.get(id=int(request.POST['frame_id']))
        if str(frame.movie_tmdb_id) == str(request.POST['movie_id']):
            return HttpResponse(json.dumps({'success': True, 'movie_name': frame.movie_tmdb_name}))
        else:
            return HttpResponse(json.dumps({'success': False, 'movie_name': frame.movie_tmdb_name}))


@transaction.commit_on_success
def register(request):
    if request.method == 'GET':
        return render_to_response("register.html", {}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        user = User.objects.create_user(request.POST["login"], request.POST["email"], request.POST["password"])
        user.first_name = request.POST["name"]
        user.last_name = request.POST["surname"]
        user.save()
        user.userprofile = UserProfile.objects.create(user=user)
        login(request, authenticate(username=user.username, password=request.POST["password"]))
        return redirect('guess_movie.views.guess')
