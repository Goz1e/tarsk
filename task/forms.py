from unicodedata import name
from django import forms
from .models import Collaborators, Comment, Dependencies, Task
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout
from accounts.models import MyUser

class Date_input(forms.DateInput):
    input_type= 'date'


# qs = list(MyUser.objects.all())
# sn = [x for x in range(1,len(qs)+1)]
# collaborator_choices=[(str(sn[i]),str(qs[i])) for i in range(len(sn)) ] 


class TaskCreateForm(forms.ModelForm,):
    class Meta:
        model = Task
        fields = ('title','description','deadline')

        widgets={
            "title": forms.TextInput(attrs={}),
            "description": forms.TextInput(attrs={}),
            "deadline": Date_input(),
        }

class TaskUpdateForm(forms.ModelForm,):
    class Meta:
        model = Task
        fields = ('title','description','deadline','completed')

        widgets={
            "title": forms.TextInput(attrs={}),
            "description": forms.TextInput(attrs={}),
            "deadline": Date_input(),
            "completed":forms.CheckboxInput()
        }

class AddCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

        widgets={
            "text": forms.TextInput(attrs={}),
            }


class DependenciesForm(forms.ModelForm):

    class Meta:
        model = Dependencies
        fields = ['dependent_on']
        widgets = {
            'dependent_on':forms.CheckboxSelectMultiple()
        }


class CollabForm(forms.ModelForm):
    class Meta:
        model = Collaborators
        fields = ['users']
        widgets = {
            'users':forms.CheckboxSelectMultiple(attrs={'name':'collab_edit_form'})
        }
        
    