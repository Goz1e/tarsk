# Generated by Django 4.1 on 2023-01-09 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_alter_task_collaborators_delete_collaborations'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='dependencies',
            field=models.ManyToManyField(related_name='deps', related_query_name='deps', to='task.task'),
        ),
        migrations.DeleteModel(
            name='Dependencies',
        ),
    ]
