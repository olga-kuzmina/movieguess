# -*- coding: utf-8 -*-
__author__ = 'olga'
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
import json

def add(request):
    return render_to_response("add_frame.html", {})


def guess(request):
    return render_to_response("guess_frame.html", {})


def movies_list(request):
    data = [{'value': u'Фантомас', 'id': 1}, {'value': u'Фантомас разбушевался', 'id': 2}]
    return HttpResponse(json.dumps(data), mimetype="application/json")
