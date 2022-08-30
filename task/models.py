from django.db import models
from django.shortcuts import get_object_or_404
from accounts.models import MyUser
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200,null=False,blank=False)
    description = models.TextField(blank=True, default='null')
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=False,null=True,related_name='my_tasks')
    slug = models.SlugField(max_length=100,unique=True,blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True,blank=True)
    completed = models.BooleanField(default=False,blank=True)
    deadline = models.DateField(blank=True,null=True)
    edited = models.BooleanField(default=False,blank=True)

    class Meta:
        ordering = ('-deadline','time_stamp')

    def __str__(self):
        return self.title
            
    def get_absolute_url(self):
        return reverse('task:detail', kwargs={'slug' : self.slug})

    def update_url(self):
        return reverse('task:update', kwargs={'slug' : self.slug})
    
    def completed_url(self):
        return reverse('task:completed', kwargs={'slug' : self.slug})

    def add_comment_url(self):
        return reverse('task:add_comment', kwargs={'slug' : self.slug})

    
    def update_dependencies_url(self):
        return reverse('task:update_dependencies', kwargs={'slug' : self.slug})

class Comment(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE, related_name='comment_on')
    author = models.ForeignKey(MyUser, related_name='comment_from', on_delete=models.CASCADE)
    text = models.TextField(max_length=300,null=False,blank=False)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Dependencies(models.Model):
    main_task = models.OneToOneField(Task,on_delete=models.CASCADE,blank=True,null=True,related_name='my_dependencies')
    dependent_on = models.ManyToManyField(Task,blank=True,)

    class Meta:
        verbose_name_plural = "dependencies"

    def __str__(self) :
        return f'dependencies for {self.main_task}'
    

class Collaborators(models.Model):
    primary_task = models.OneToOneField(Task,related_name='collab',on_delete=models.CASCADE)
    users = models.ManyToManyField(MyUser,related_name='collaborators',)

    class Meta:
        verbose_name_plural = "collaborators"

    def __str__(self) :
        return f'collaborators on  {self.primary_task}'