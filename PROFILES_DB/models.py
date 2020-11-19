# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

class PROFILES(models.Model):
    id_profiles = models.IntegerField()
    Info = models.TextField()
    Passed = models.TextField()
    Points = models.TextField()
    Scanned = models.TextField()


    # id
    # Passed (ID, NAME, POINTSALL, pointsMy, ratingPoints, reload;...)
    # Points (points, points, ..., points)
    # scanned(ID, CLASS, IMG_URL, NUMBER, SOURCEPHOTO, TEXT, TITLE;...)
    #
    #
