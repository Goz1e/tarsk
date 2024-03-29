from django.db import models
from native_auth.models import MyUser
from django.urls import reverse
from datetime import datetime
from django.db.models import Q
now = datetime.now().date

# Create your models here.
class TaskQueryset(models.QuerySet):
    def user_tasks(self,user):
        return self.all().filter(user=user)
    
    def completed_tasks(self,user):
        return self.user_tasks(user).filter(completed=True)

    def active_tasks(self,user):
        return self.user_tasks(user).filter(completed=False)

    def search(self,user,query):
        lookup= (Q(title__icontains=query)|
        Q(description__icontains=query) | Q(slug__icontains=query))
        qs1 = self.user_tasks(user)
        if user.is_admin:
            qs1 = self.all()
        collabs_qs = user.collabs.all()
        qs = (qs1 | collabs_qs).distinct()
        return qs.filter(lookup)

class Task(models.Model):
    title = models.CharField(max_length=200,null=False,blank=False)
    description = models.TextField(blank=True, default='null')
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=False,null=True,related_name='my_tasks')
    slug = models.SlugField(max_length=100,unique=True,blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True,blank=True)
    completed = models.BooleanField(default=False,blank=True)
    deadline = models.DateField(blank=False,null=True)
    edited = models.BooleanField(default=False,blank=True)
    collaborators = models.ManyToManyField(MyUser,related_name='collabs',related_query_name='collabs', blank=True)
    dependencies = models.ManyToManyField("Task",related_name='deps',related_query_name='deps', blank=True)

    class Meta:
        ordering = ('deadline','time_stamp','completed')

    objects = TaskQueryset.as_manager()

    def rem_time(self):
        return (self.deadline - now()).days

    def late(self):
        return self.rem_time() <= 0
            
    def __str__(self):
        return self.title
            
    def get_absolute_url(self):
        return reverse('task:detail', kwargs={'slug' : self.slug})

    def add_comment_url(self):
        return reverse('task:add_comment', kwargs={'slug' : self.slug})

# class Dependencies(models.Model):
#     main_task = models.OneToOneField(Task,on_delete=models.CASCADE,blank=True,null=True,related_name='my_dependencies')
#     dependent_on = models.ManyToManyField(Task,blank=True,related_name='dependants')

#     class Meta:
#         verbose_name_plural = "dependencies"

#     def __str__(self) :
#         return f'dependencies for {self.main_task}'
    

class Comment(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, related_name='comment_from', on_delete=models.CASCADE)
    text = models.TextField(max_length=300,null=False,blank=False)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text