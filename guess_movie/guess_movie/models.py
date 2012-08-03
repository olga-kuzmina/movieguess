# -*- coding: utf-8 -*-
__author__ = 'olga'

from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    class Meta:
        db_table = 'user_profile'


class TMDBMovie(Model):
    tmdb_id = models.CharField(max_length=100)
    tmdb_name = models.CharField(max_length=300)


class Frame(Model):
    '''
    Кадр из фильма
    '''
    movie = models.ForeignKey(TMDBMovie)
    file = models.ImageField(upload_to='pictures')
    owner = models.ForeignKey(UserProfile)


class GuessedFrames(models.Model):
    '''
    Связи пользователей и фильмов, которые они уже угадали
    '''
    user = models.ForeignKey(UserProfile)
    frame = models.ForeignKey(Frame, related_name='users_guessed')


class WrongGuesses(models.Model):
    '''
    История ошибочных попыток угадать фильм
    '''
    frame = models.ForeignKey(Frame)
    movie = models.ForeignKey(TMDBMovie)
    counter = models.IntegerField(blank=True, default=0)

