
from django import forms
from .models import Assesment

class AssesmentForm(forms.ModelForm):
    class Meta:
        model = Assesment
        fields = ('title','description','questions')
