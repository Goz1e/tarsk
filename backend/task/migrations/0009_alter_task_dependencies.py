# Generated by Django 4.1 on 2023-01-14 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_alter_task_collaborators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='dependencies',
            field=models.ManyToManyField(blank=True, null=True, related_name='deps', related_query_name='deps', to='task.task'),
        ),
    ]
