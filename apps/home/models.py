from pydoc import describe
from django.db import models

# Create your models here.


class Assesment(models.Model):
    title =models.CharField(max_length=100)
    description =models.TextField()
    questions =models.TextField(null=True,blank=True)

class Candidate(models.Model):
    candidate_name =models.CharField(max_length=100)
    candidate_email =models.EmailField(max_length=254)
    candidate_mobile =models.BigIntegerField()

class CandidateAssessment(models.Model):
    candidate_id =models.CharField(max_length=100)
    token =models.TextField()
    assessment_id =models.IntegerField(null=True,blank=True)
    process =models.IntegerField(default=0)