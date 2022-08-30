from asyncio import current_task
from pickle import FALSE
from urllib import request
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from task.models import Collaborators, Dependencies, Task
from django.utils.text import slugify
import string, random


@receiver(pre_save,sender=Task)
def slug_creator(sender,instance,new_slug=None,**kwargs):
    #create a slug Variable and assign the slugify(title)
    if not instance.slug:
        slug = slugify(instance.title)
        
        if new_slug is not None:
            slug = new_slug

        qs = Task.objects.filter(slug=slug)
        if qs.exists():
            new_slug = f'{slug}-{random.choice(string.ascii_lowercase)}'
            return slug_creator(sender,instance,new_slug=new_slug,**kwargs)

        instance.slug = slug
    

@receiver(post_save,sender=Task)
def dependency_Collaborators_creator(sender,instance,*args,**kwargs):
    
    if (hasattr(instance, 'my_dependencies')) == False:
        Dependencies.objects.create(main_task=instance)
    if (hasattr(instance, 'collab')) == False:
        Collaborators.objects.create(primary_task=instance)
        