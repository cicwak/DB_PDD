from django.db import models

# Create your models here.

class LINKS(models.Model):
    id_link = models.TextField()
    link = models.TextField()