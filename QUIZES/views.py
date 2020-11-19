from django.shortcuts import render, HttpResponse

from json import dumps

from .models import QUIZER

# Create your views here.

def index(request):
    answer = {}
    quizes = QUIZER.objects.all()

    for item in quizes:

        id_test = item.id_test
        descQuiz = item.descQuiz
        hard = item.hard
        imgQuiz = item.imgQuiz
        name = item.name
        points = item.points
        questions = []

        questions_almost = item.questions
        for dota_zap in questions_almost.split(';'):
            vertical_strip = dota_zap.split('|')
            img_url = vertical_strip[0]
            nameQuest = vertical_strip[1]

            SM = []
            for x in vertical_strip[2].split(','):
                SM.append(x)

            right = vertical_strip[3]
            upl = {'img' : img_url, 'nameQuest' : nameQuest, 'questions' : SM, 'right' : right}
            questions.append(upl)
        questions.append({'length' : len(questions) - 1})

        answer[id_test] = {'descQuiz' : descQuiz, 'hard' : hard, 'imgQuiz' : imgQuiz, 'name' : name, 'points' : points,
                           'questions' : questions, 'type' : item.type}

    return HttpResponse(dumps(answer, ensure_ascii=False))
