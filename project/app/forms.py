from cProfile import label
from dataclasses import field
from django import forms
from .models import QuizOptions,Quiz

class QuestionForm(forms.ModelForm):

    class Meta:
        model = QuizOptions
        exclude = ('quiz',)
        widgets = {'quiz': forms.HiddenInput(),}


class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = '__all__' 
        widgets = {'user_app': forms.HiddenInput(),'token': forms.HiddenInput(),}