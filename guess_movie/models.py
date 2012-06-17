# -*- coding: utf-8 -*-
__author__ = 'olga'

from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User

class Frame(Model):
    '''
    Кадр из фильма
    '''
    movie_tmdb_id = models.CharField(max_length=100)
    movie_tmdb_name = models.CharField(max_length=300)
    file = models.ImageField(upload_to='pictures')


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    class Meta:
        db_table = 'user_profile'