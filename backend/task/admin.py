from django.contrib import admin
from .models import (
    Task, Comment, Dependencies
)
# Register your models here.
admin.site.register(Task)
admin.site.register(Dependencies)
admin.site.register(Comment)
