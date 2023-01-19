from rest_framework import serializers
from native_auth.models import MyUser
from task.models import (
    Task,Comment,
)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    delete_link = serializers.HyperlinkedIdentityField(view_name='delete-comment',lookup_field='id')
    class Meta:
        model = Comment
        fields = ['id','delete_link','task','author','text','time_stamp']

class TaskInLineSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Task
        fields = ['title']

class UserInLineSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MyUser
        fields = ['email']


class TaskSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(view_name='task-detail',lookup_field='slug')
    
    class Meta:
        model = Task
        fields = ['pk','title','description','slug','detail',
        'time_stamp','dependencies','completed','deadline','edited',]

class TaskDetailSerializer(serializers.ModelSerializer):
    dependencies = TaskInLineSerializer(
        many=True,
        read_only=True,
        )
    collaborators = UserInLineSerializer(
        many=True,
        read_only=True,
        )
    comments = CommentSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Task
        fields = ['pk','title','description','slug',
        'time_stamp','completed','deadline','edited','collaborators','dependencies','comments']


