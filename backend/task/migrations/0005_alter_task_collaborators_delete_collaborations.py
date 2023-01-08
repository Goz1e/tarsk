# Generated by Django 4.1 on 2023-01-08 02:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0004_task_collaborators_alter_dependencies_dependent_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='collaborators',
            field=models.ManyToManyField(related_name='collabs', related_query_name='collabs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Collaborations',
        ),
    ]
