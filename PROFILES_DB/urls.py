# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index),

    path('get_profile/', get_profile), # get  id=   получение фулл инфы профиля
    path('get_points/', get_points), # get  id=     получение толькo Points
    path('get_points_id/', get_points_id), # get  id=&points_id=    получение Points по его идентификатору
    path('get_passed/', get_passed), # get  id=    получение всех пройденных тестов
    path('get_passed_id/', get_passed_id), # get  id=&passed_id=    получение пройденного теста по его идентификатору
    path('get_scanned/', get_scanned), # get id=    получение всех отсканированных знаков пользователя

    path('delete_passed_id/', delete_passed_id), # get id=&passed_id=   удаление контретно пройденного теста
    path('delete_points_id/', delete_points_id), # get id=&points_id=   удаление конкретных очков
    path('delete_passed/', delete_passed), # get id=    удаление всех пройденных тестов
    path('delete_points/', delete_points), # get id=    удаление всех очков
    path('delete_info/', delete_info), # get id=    удаление всей информации о пользователе

    path('post_points_id/', post_points_id), # post json={points_id : points}   отправить очки
    path('post_scanned_id/', post_scanned_id), # post json={id : ... , json : {...}     отправить сканированную картинку
    path('post_info/', post_info), # post json={id : ..., json : { ... } }      отправить информацию пользователя
    path('post_passed_id/', post_passed_id), # post json={'id': ... , 'json' : {'name': .... }}отправить пройденный тест
]