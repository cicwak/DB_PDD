from django.db import models

# Create your models here.

class JSON1(models.Model):
    key = models.TextField(max_length=32)
    img_url = models.TextField(max_length=256)
    klass = models.TextField(max_length=256)
    number = models.TextField(max_length=256)
    text = models.TextField(max_length=256)
    title = models.TextField(max_length=256)