# -*- coding: utf-8 -*-
__author__ = 'olga'
from django.shortcuts import render_to_response

def add(request):
    return render_to_response("add_frame.html", {})

def guess(request):
    return render_to_response("guess_frame.html", {})
