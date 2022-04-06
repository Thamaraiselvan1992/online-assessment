from pydoc import describe
from django.db import models

# Create your models here.


class Assesment(models.Model):
    title =models.CharField(max_length=100)
    description =models.TextField()
    questions =models.TextField()