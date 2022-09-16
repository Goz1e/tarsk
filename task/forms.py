from unicodedata import name
from django import forms
from .models import Comment,Task
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
            "title": forms.TextInput(attrs={"class":'border-success border-opacity-25',}),
            "description": forms.TextInput(attrs={"class":'border-success border-opacity-25',}),
            "deadline": Date_input(attrs={"class":'border-success border-opacity-25',}),
        }

class TaskUpdateForm(forms.ModelForm,):
    class Meta:
        model = Task
        fields = ('title','description','deadline','completed')

        widgets={
            "title": forms.TextInput(attrs={"class":'border-success border-opacity-25',}),
            "description": forms.TextInput(attrs={"class":'border-success border-opacity-25',}),
            "deadline": Date_input(attrs={"class":'border-success border-opacity-25',}),
            "completed":forms.CheckboxInput(attrs={"class":'border-success border-opacity-25',})
        }

class AddCommentForm(forms.ModelForm):

    
    class Meta:
        model = Comment
        fields = ['text']
        
        widgets={
            "text": forms.TextInput(attrs={"class":'border-success border-opacity-25',}),
            
            }
        labels = {
            'text': 'comment',
        }