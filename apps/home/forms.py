
from django import forms
from .models import Assesment,Candidate

class AssesmentForm(forms.ModelForm):
    class Meta:
        model = Assesment
        fields = ('title','description','questions')

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('candidate_name','candidate_email','candidate_mobile')
