# -*- coding: utf-8 -*-
from random import randint

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from .models import LINKS

from json import dumps, loads

# Create your views here.
'''
@csrf_exempt
@ensure_csrf_cookie
'''


def random_name_32bit(lens=32):
    letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z',
              'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z',
              '-', '+', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    name = ''
    for i in range(lens):
        name += letter[randint(0, len(letter) - 1)]
    return name


def index(request):
    answer = {}
    links = LINKS.objects.all()
    for links_item in links:
        answer[links_item.id_link] = {links_item.id_link: links_item.link}
    if answer == {}:
        return HttpResponse(dumps(None, ensure_ascii=False))
    return HttpResponse(dumps(answer, ensure_ascii=False))


def get_links(request):
    id_link = request.GET.get('id_link')
    link = LINKS.objects.get(id_link=id_link)
    return HttpResponse(dumps({link.id_link: {link.id_link: link.link}}, ensure_ascii=False))


@csrf_exempt
@ensure_csrf_cookie
def post_link(request):
    json = loads(request.body.decode())
    json = json['link']

    link = LINKS(id_link=random_name_32bit(), link=json)
    link.save()
    return HttpResponse(dumps({link.id_link: {link.id_link: link.link}}, ensure_ascii=False))
