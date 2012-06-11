# -*- coding: utf-8 -*-
__author__ = 'olga'

from django.db import models
from django.db.models.base import Model

class Movie(Model):
    '''
    Фильм
    '''
    name = models.CharField(max_length=300)


class Frame(Model):
    '''
    Кадр из фильма
    '''
    movie = models.ForeignKey(Movie)
    picture_path = models.CharField(max_length=100)
