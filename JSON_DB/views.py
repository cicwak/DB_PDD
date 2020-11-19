from django.shortcuts import render, HttpResponse
from .models import JSON1
import requests

import json


# Create your views here.

# ensure_ascii=False
# {'-MGxcFc-fJjiikgcIXiW': {'class': '', 'img_url': [], 'number': '', 'text': [], 'title': ''},


def index(request):
    a = {}
    json_ = JSON1.objects.all()
    for item in json_:
        img_url = [element.strip("'[]") for element in item.img_url.split(", ")]
        a[item.key] = {'class': item.klass, 'img_url': img_url, 'number': item.number, 'text': item.text,
                       'title': item.title}
    return HttpResponse(json.dumps(a, ensure_ascii=False))


def filling(request):
    r = requests.get('https://pddsigns-b18ec.firebaseio.com/JSON.json').json()
    for i in r:
        for ir in r[i]:
            a = r[i][ir]

            js = JSON1(key=ir, img_url=a['img_url'], klass=a['class'], number=a['number'], text=a['text'],
                       title=a['title'])
            js.save()
    return HttpResponse('<h1>ВСЕ НОРМ!!!!</h1>')