# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse

from .dict import text
from json import dumps


def index(requests):
    return HttpResponse(dumps(text, ensure_ascii=False))

