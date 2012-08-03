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
from django.db.models import Count, Max

from models import Frame, UserProfile, GuessedFrames, TMDBMovie, WrongGuesses

@login_required
def add(request):
    if request.method == 'GET':
        return render_to_response("add_frame.html", {}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        movie, created = TMDBMovie.objects.get_or_create(tmdb_id=request.POST['movie_id'],
            tmdb_name=request.POST['movie_name'])

        file = request.FILES['file']
        frame = Frame()
        frame.file = file
        frame.movie = movie
        frame.owner = request.user.userprofile
        frame.save()
        return render_to_response("add_frame.html", {'result': u'Файл был успешно загружен'},
            context_instance=RequestContext(request))


@login_required
def guess(request):
    if request.method == 'GET':
        # Показываются в случайном порядке фильмы, которые добавиили другие пользователи и которые еще не были угаданы.
        frame = Frame.objects.order_by('?').exclude(owner_id=request.user.userprofile.id).\
        exclude(users_guessed__user_id=request.user.userprofile)
        if frame:
            return render_to_response("guess_frame.html", {'img_src': frame[0].file.url, 'frame_id': frame[0].id},
                context_instance=RequestContext(request))
        else:
            return render_to_response("add_frame.html", {'result': u'К сожалению, вы уже угадали все фильмы.'},
                context_instance=RequestContext(request))

    elif request.method == 'POST':
        frame = Frame.objects.get(id=int(request.POST['frame_id']))
        max_wrong_guesses = WrongGuesses.objects.filter(frame=frame).aggregate(max=Max('counter'))
        wrong_guess = WrongGuesses.objects.filter(frame=frame, counter=max_wrong_guesses['max']).values(
            'movie__tmdb_name')
        result = {'wrong_guess': wrong_guess[0]['movie__tmdb_name']} if wrong_guess else {}
        if str(frame.movie.tmdb_id) == request.POST['movie_id']:
            GuessedFrames.objects.create(frame=frame, user=request.user.userprofile)
            result.update({'success': True, 'movie_name': frame.movie.tmdb_name})
            return HttpResponse(json.dumps(result))
        else:
            movie, created = TMDBMovie.objects.get_or_create(tmdb_id=request.POST['movie_id'],
                tmdb_name=request.POST['movie_name'])
            obj, created = WrongGuesses.objects.get_or_create(movie=movie, frame=frame)
            obj.counter += 1
            obj.save()
            result.update({'success': False, 'movie_name': frame.movie.tmdb_name})
            return HttpResponse(json.dumps(result))


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


def rating(request):
    if request.method == "GET":
        users = GuessedFrames.objects.values('user__user__username').annotate(gcount=Count('user')).order_by('-gcount')[
                :10]
        users = list(users)
        map(lambda el: el.update({'index': users.index(el) + 1}), users)
        return render_to_response("rating.html", {'records': users})