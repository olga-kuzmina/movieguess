# -*- coding: utf-8 -*-
__author__ = 'olga'

from django.db import models
from django.db.models.base import Model

class Frame(Model):
    '''
    Кадр из фильма
    '''
    movie_tmdb_id = models.CharField(max_length=100)
    movie_tmdb_name = models.CharField(max_length=300)
    file = models.ImageField(upload_to='pictures')
