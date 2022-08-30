from django.contrib import admin

from task.models import *

# Register your models here.
admin.site.register(Collaborators)
admin.site.register(Task)
admin.site.register(Dependencies)
admin.site.register(Comment)