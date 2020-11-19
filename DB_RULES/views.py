# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse

from json import dumps
from .dict import text

# Create your views here.

def index(requests):
    return HttpResponse(dumps(text, ensure_ascii=False))