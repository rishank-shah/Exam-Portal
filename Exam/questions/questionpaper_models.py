from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from .question_models import Question_DB
from django import forms

class Question_Paper(models.Model):
    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "Professor"}, on_delete=models.CASCADE)
    qPaperTitle = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question_DB)

    def __str__(self):
        return f' Question Paper Title :- {self.qPaperTitle}\n'


class QPForm(ModelForm):
    def __init__(self,professor,*args,**kwargs):
        super (QPForm,self ).__init__(*args,**kwargs) 
        self.fields['questions'].queryset = Question_DB.objects.filter(professor=professor)

    class Meta:
        model = Question_Paper
        fields = '__all__'
        exclude = ['professor']
        widgets = {
            'qPaperTitle': forms.TextInput(attrs = {'class':'form-control'})
        }
