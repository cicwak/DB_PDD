from django.db import models

# Create your models here.

class QUIZER(models.Model):
    id_test = models.TextField()
    descQuiz = models.TextField()
    hard = models.CharField(max_length=32)
    imgQuiz = models.TextField()
    name = models.TextField()
    points = models.IntegerField()
    questions = models.TextField()
    type = models.TextField()
    # questions = 'IMG_URL|NAMEQUEST|SM,SM,SM|RIGHT;IMG_URL|NAMEQUEST|SM,SM,SM|RIGHT'
