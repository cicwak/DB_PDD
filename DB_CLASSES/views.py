# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse

from .dict import text

from json import dumps
# Create your views here.

def index(request):
    return HttpResponse(dumps(text, ensure_ascii=False))