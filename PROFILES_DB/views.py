# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse

from random import randint
from json import dumps, loads
from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from .models import PROFILES

client_secret = "wvl68m4dR1UpLrVRli"


def is_valid(*, query: dict, secret: str, sign) -> bool:
    """Check VK Apps signature"""
    vk_subset = OrderedDict(sorted(x for x in query.items() if x[0][:3] == "vk_"))
    hash_code = b64encode(HMAC(secret.encode(), urlencode(vk_subset, doseq=True).encode(), sha256).digest())
    decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')
    return sign == decoded_hash_code


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


def str_to_list(text):
    # строка должна быть вида('[...]')
    answer = []
    text = text[1:len(text) - 1]
    list_text = text.split(',')
    for i in list_text:
        answer.append(i.strip('"[]'))
    return answer


def replace_symbol_from_comma(list_request):
    answer_list = []
    for item in list_request:
        answer_list.append(item.replace(',', ':'))

    answer_str = ''
    for item in answer_list:
        item += ' '
        answer_str += item

    answer = [answer_str]

    return answer


def index(request):

    answer = {}
    for item in PROFILES.objects.all():
        # Формируем Passed
        Passed = {}
        Points = {}
        Scanned = {}
        for Passed_item in item.Passed.split(';'):
            items_passed = Passed_item.split(',')

            if items_passed[5] == 'true':
                passed_reload = None
                reload = {}
                name_dict = random_name_32bit()
                reload['reloadName'] = name_dict
                Passed[name_dict] = {'name': items_passed[1], 'pointsAll': items_passed[2],
                                     'pointsMy': items_passed[3],
                                     'ratingPoints': items_passed[4], 'reload': items_passed[5],
                                     'reloadName': {random_name_32bit(): reload}
                                     }
            else:
                Passed[items_passed[0]] = {'name': items_passed[1], 'pointsAll': items_passed[2],
                                           'pointsMy': items_passed[3],
                                           'ratingPoints': items_passed[4], 'reload': items_passed[5]
                                           }

        # Формируем Points
        for Points_item in item.Points.split(','):
            Points[random_name_32bit()] = Points_item
        # Формируем Scanned
        for Scanned_item in item.Scanned.split(';'):
            SCAN = Scanned_item.split('|')
            text = []
            text = replace_symbol_from_comma(str_to_list(SCAN[5]))
            text[0].replace(', ', ',')

            if SCAN[6][len(SCAN[6]) - 1] != '.':
                title = SCAN[6] + '.'
            else:
                title = SCAN[6]
            Scanned[random_name_32bit()] = {'class': SCAN[0], 'date': SCAN[1],
                                            'img_url': SCAN[2],
                                            'number': SCAN[3], 'sourcePhoto': SCAN[4],
                                            'text': text,
                                            'title': title,
                                            }

        answer[item.id_profiles] = {'Passed': Passed, 'Points': Points, 'Scanned': Scanned}

    return HttpResponse(dumps(answer, ensure_ascii=False))


def get_profile(request):
    answer = {}
    id_profiles = request.GET.get('id')

    try:
        profile = PROFILES.objects.get(id_profiles=id_profiles)

    except Exception:
        save = PROFILES(id_profiles=id_profiles, Passed='', Points='', Scanned='', Info='')
        save.save()
        profile = PROFILES.objects.get(id_profiles=id_profiles)
        return HttpResponse(dumps(None, ensure_ascii=False))

    Info = {}
    Passed = {}
    Points = {}
    Scanned = {}

    try:
        Info_item = profile.Info.split('|')
        Info['0'] = {'bdate': Info_item[0], 'can_access_closed': Info_item[1], 'can_invite_to_chats': Info_item[2],
                     'city': {'id': Info_item[3], 'title': Info_item[4]},
                     'country': {'id': Info_item[5], 'title': Info_item[6]},
                     'first_name': Info_item[7], 'id': Info_item[8], "is_closed": Info_item[9],
                     'last_name': Info_item[10], 'photo_100': Info_item[11],
                     'photo_200': Info_item[12], 'photo_max_orig': Info_item[13],
                     'points': Info_item[14], 'request_id': Info_item[15], 'sex': Info_item[16],
                     'timezone': Info_item[17]}
    except Exception:
        Info = None

    try:
        for Passed_item in profile.Passed.split(';'):
            items_passed = Passed_item.split(',')

            if items_passed[5] == 'true':
                passed_reload = None
                reload = {}
                name_dict = items_passed[0]
                reload['reloadName'] = name_dict
                Passed[name_dict] = {'name': items_passed[1], 'pointsAll': items_passed[2],
                                     'pointsMy': items_passed[3],
                                     'ratingPoints': items_passed[4], 'reload': items_passed[5],
                                     'reloadName': {items_passed[0]: reload}
                                     }
            else:
                Passed[items_passed[0]] = {'name': items_passed[1], 'pointsAll': items_passed[2],
                                           'pointsMy': items_passed[3],
                                           'ratingPoints': items_passed[4], 'reload': items_passed[5]
                                           }
    except Exception:
        Passed = None

    try:
        for Points_item in profile.Points.split(';'):
            points = Points_item.split(',')
            Points[points[0]] = {points[0]: points[1]}
    except Exception:
        Points = None

    try:
        for Scanned_item in profile.Scanned.split(';'):
            SCAN = Scanned_item.split('|')
            img_url = SCAN[3].split(',')

            text = [SCAN[5]]
            text[0].replace(', ', ',')

            if SCAN[6][len(SCAN[6]) - 1] != '.':
                title = SCAN[6] + '.'
            else:
                title = SCAN[6]

            Scanned[SCAN[0]] = {'class': SCAN[1], 'date': SCAN[2],
                                'img_url': img_url, 'sourcePhoto': SCAN[4],
                                'text': text,
                                'title': title,
                                }
    #  Знаки дополнительной информации | 24.10.2020 | https://media.am.ru/pdd/sign/m/8.13.png | 8.13 | https://sun9-74.userapi.com/XvKkG6vFpVsOwQ2RB_Ryn1UW63Hf2iWl8fSagQ/eAyhlFWYsiw.jpg | Указывает направление главной дороги на перекрестке. Таблички 8.13 при расположении ,знаков над проезжей частью, обочиной или тротуаром размещаются сбоку от знака|Направление главной дороги | BHuQW7ZtriITWQWX ; LtvlnFHoWOsMHZLk | aaaa | 2 | ['sdfsdngsdfg'] | 0 | ['Обозначают препятствие и направление его объезда. Применяются со знаками   4.2.1   -   4.2.3  '] | Препятствие
    except Exception:
        Scanned = None

    answer[id_profiles] = {}

    if Info is not None:
        answer[id_profiles]['Info'] = Info

    if Passed is not None:
        answer[id_profiles]['Passed'] = Passed

    if Points is not None:
        answer[id_profiles]['Points'] = Points

    if Scanned is not None:
        answer[id_profiles]['Scanned'] = Scanned

    if (Info is None) and (Passed is None) and (Points is None) and (Scanned is None):
        return HttpResponse(dumps(None, ensure_ascii=False))

    return HttpResponse(dumps(answer, ensure_ascii=False))


def get_points(request):
    Points = {}
    id_profiles = request.GET.get('id')

    try:
        profile = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    try:
        for Points_item in profile.Points.split(';'):
            points = Points_item.split(',')
            Points[points[0]] = {points[0]: points[1]}
    except Exception:
        Points = None

    if Points == None:
        return HttpResponse(dumps(None, ensure_ascii=False))
    else:
        answer = Points

    return HttpResponse(dumps(answer, ensure_ascii=False))


def get_passed(request):
    Passed = {}
    id_profile = request.GET.get('id')

    try:
        profile = PROFILES.objects.get(id_profiles=id_profile)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    try:
        for Passed_item in profile.Passed.split(';'):
            items_passed = Passed_item.split(',')

            if items_passed[5] == 'true':
                passed_reload = None
                reload = {}
                name_dict = items_passed[0]
                reload['reloadName'] = name_dict
                Passed[name_dict] = {'name': items_passed[1], 'pointsAll': items_passed[2],
                                     'pointsMy': items_passed[3],
                                     'ratingPoints': items_passed[4], 'reload': items_passed[5],
                                     'reloadName': {items_passed[0]: reload}
                                     }
            else:
                Passed[items_passed[0]] = {'name': items_passed[1], 'pointsAll': items_passed[2],
                                           'pointsMy': items_passed[3],
                                           'ratingPoints': items_passed[4], 'reload': items_passed[5]
                                           }
    except Exception:
        Passed = None

    if Passed is None:
        return HttpResponse(dumps(None, ensure_ascii=False))
    else:
        answer = Passed

    return HttpResponse(dumps(answer, ensure_ascii=False))


def get_passed_id(request):
    Passed = {}

    id_passed = request.GET.get('passed_id')
    id_profiles = request.GET.get('id')

    profile = PROFILES.objects.get(id_profiles=id_profiles)
    try:
        for Passed_item in profile.Passed.split(';'):
            if Passed_item.split(',')[0] == id_passed:
                answer = {}

                items_passed = Passed_item.split(',')

                if items_passed[5] == 'true':

                    reload = {'reloadName': items_passed[0]}
                    Passed[items_passed[0]] = {'name': items_passed[1], 'pointsAll': items_passed[2],
                                               'pointsMy': items_passed[3],
                                               'ratingPoints': items_passed[4], 'reload': items_passed[5],
                                               'reloadName': {items_passed[0]: reload}
                                               }
                else:
                    Passed[items_passed[0]] = {'name': items_passed[1], 'pointsAll': items_passed[2],
                                               'pointsMy': items_passed[3],
                                               'ratingPoints': items_passed[4], 'reload': items_passed[5]
                                               }

                answer = Passed

                return HttpResponse(dumps(answer, ensure_ascii=False))
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    return HttpResponse(dumps(None, ensure_ascii=False))


def get_points_id(request):
    id_points = request.GET.get('points_id')
    id_profiles = request.GET.get('id')

    try:
        profile = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    for Points_item in profile.Points.split(';'):
        if Points_item.split(',')[0] == id_points:
            answer = {id_points: Points_item.split(',')[1]}
            return HttpResponse(dumps(answer, ensure_ascii=False))

    return HttpResponse(dumps(None, ensure_ascii=False))


def delete_passed_id(request):
    reedit = ''
    ans = False

    id_passed = request.GET.get('passed_id')
    id_profiles = request.GET.get('id')

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    for Passed_item in profiles.Passed.split(';'):
        if Passed_item.split(',')[0] == id_passed:
            ans = True
        else:
            reedit += Passed_item + ';'

    profiles.Passed = reedit[0:len(reedit) - 1]
    profiles.save()

    if ans == True:
        return HttpResponse(dumps(True, ensure_ascii=False))

    return HttpResponse(dumps(None, ensure_ascii=False))


def delete_points_id(request):
    points_id = request.GET.get('points_id')
    id_profiles = request.GET.get('id')

    ans = False
    reedit = ''

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    for Points_item in profiles.Points.split(';'):
        if Points_item.split(',')[0] == points_id:
            ans = False
        else:
            reedit += Points_item + ';'

    profiles.Points = reedit[0:len(reedit) - 1]
    profiles.save()

    if ans == True:
        return HttpResponse(dumps(True, ensure_ascii=False))

    return HttpResponse(dumps(None, ensure_ascii=False))


@csrf_exempt
@ensure_csrf_cookie
def post_points_id(request):
    json = loads(request.body.decode())
    id_profiles = json['id']

    ans = False
    reedit = ''

    for i in json:
        pass

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    for Points_item in profiles.Points.split(';'):
        if str(Points_item.split(',')[0]) == str(i):
            ans = True
        else:
            reedit += Points_item + ';'

    profiles.Points = reedit + '{},{}'.format(i, json[i])
    profiles.save()

    if ans == True:
        return HttpResponse(dumps(None, ensure_ascii=False))

    return HttpResponse(dumps(True, ensure_ascii=False))


def delete_passed(request):
    id_profiles = request.GET.get('id')

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    profiles.Passed = ''
    profiles.save()
    return HttpResponse(dumps(True, ensure_ascii=False))


@csrf_exempt
@ensure_csrf_cookie
def post_passed_id(request):
    json = loads(request.body.decode())
    id_profiles = json['id']
    json = json['json']

    print('id_profiles')
    print('json')

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    for Passed_item in profiles.Passed.split(';'):
        passed_item = Passed_item.split(',')
        if passed_item[1] == json['name']:
            return HttpResponse(dumps(None, ensure_ascii=False))

    answer = {}
    for item in json:
        if item == 'name':
            answer['name'] = json[item]

        if item == 'pointsAll':
            answer['pointsAll'] = json[item]

        if item == 'pointsMy':
            answer['pointsMy'] = json[item]

        if item == 'ratingPoints':
            answer['ratingPoints'] = json[item]

        if item == 'reload':
            answer['reload'] = json[item]

    index = random_name_32bit(lens=16)
    profiles.Passed = profiles.Passed + ';{},{},{},{},{},{}'.format(index, answer['name'],
                                                                    answer['pointsAll'],
                                                                    answer['pointsMy'], answer['ratingPoints'],
                                                                    answer['reload'])

    profiles.save()

    return HttpResponse(dumps({'name': index}, ensure_ascii=False))


@csrf_exempt
@ensure_csrf_cookie
def post_passed_id_add(request):
    json = loads(request.body.decode())
    id_profiles = json['id']
    json = json['json']

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    answer = {}
    for item in json:
        if item == 'name':
            answer['name'] = json[item]

        if item == 'pointsAll':
            answer['pointsAll'] = json[item]

        if item == 'pointsMy':
            answer['pointsMy'] = json[item]

        if item == 'ratingPoints':
            answer['ratingPoints'] = json[item]

        if item == 'reload':
            answer['reload'] = json[item]

    index = random_name_32bit(lens=16)
    profiles.Passed = profiles.Passed + ';{},{},{},{},{},{}'.format(index, answer['name'],
                                                                    answer['pointsAll'],
                                                                    answer['pointsMy'], answer['ratingPoints'],
                                                                    answer['reload'])

    profiles.save()

    return HttpResponse(dumps({'name': index}, ensure_ascii=False))


def delete_points(request):
    id_profiles = request.GET.get('id')

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    profiles.Points = ''
    profiles.save()
    return HttpResponse(dumps(True, ensure_ascii=False))


def get_scanned(request):
    id_profiles = request.GET.get('id')
    Scanned = {}

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    try:
        for Scanned_item in profiles.Scanned.split(';'):
            SCAN = Scanned_item.split('|')
            img_url = ''
            text = [SCAN[5]]
            text[0].replace(', ', ',')

            if SCAN[6][len(SCAN[6]) - 1] != '.':
                title = SCAN[6] + '.'
            else:
                title = SCAN[6]

            Scanned[SCAN[7]] = {'class': SCAN[0], 'date': SCAN[1],
                                'img_url': img_url,
                                'number': SCAN[3], 'sourcePhoto': SCAN[4],
                                'text': text,
                                'title': title,
                                }

    except Exception:
        Scanned = None

    return HttpResponse(dumps(Scanned, ensure_ascii=False))


@csrf_exempt
@ensure_csrf_cookie
def post_scanned_id(request):
    json = loads(request.body.decode())
    id_profiles = json['id']
    json = json['json']

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    img_url = ''
    text = ''

    answer = {}
    for item in json:
        if item == 'class':
            answer['class'] = json[item]

        if item == 'date':
            answer['date'] = json[item]

        if item == 'img_url':
            answer['img_url'] = json[item]
            for i in json[item]:
                img_url += i

        if item == 'sourcePhoto':
            answer['sourcePhoto'] = json[item]

        if item == 'text':
            answer['text'] = json[item]
            for i in json[item]:
                text += i

        if item == 'title':
            answer['title'] = json[item]

    index = random_name_32bit(lens=16)
    profiles.Scanned = profiles.Scanned + ';{}|{}|{}|{}|{}|{}|{}'.format(index, json['class'], json['date'], img_url,
                                                                         json['sourcePhoto'], text, json['title'])

    profiles.save()

    return HttpResponse(dumps({'name': index}, ensure_ascii=False))


def delete_info(request):
    id_profiles = request.GET.get('id')

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    profiles.Info = ''
    profiles.save()

    return HttpResponse(dumps(True, ensure_ascii=False))


@csrf_exempt
@ensure_csrf_cookie
def post_info(request):
    json = loads(request.body.decode())
    id_profiles = json['id']
    json = json['json']

    try:
        profiles = PROFILES.objects.get(id_profiles=id_profiles)
    except Exception:
        return HttpResponse(dumps(None, ensure_ascii=False))

    answer = ''
    answer += '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(json['bdate'], json['can_access_closed'],
                                                                             json['can_invite_to_chats'],
                                                                             json['city']['id'], json['city']['title'],
                                                                             json['country']['id'],
                                                                             json['country']['title'],
                                                                             json['first_name'], json['id'],
                                                                             json['is_closed'], json['last_name'],
                                                                             json['photo_100'], json['photo_200'],
                                                                             json['photo_max_orig'], json['points'],
                                                                             json['request_id'], json['sex'],
                                                                             json['timezone'])

    profiles.Info = answer
    profiles.save()

    return HttpResponse(dumps(True, ensure_ascii=False))
