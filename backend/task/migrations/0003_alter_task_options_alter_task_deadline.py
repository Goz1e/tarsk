# Generated by Django 4.1 on 2023-01-04 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_task_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('deadline', 'time_stamp', 'completed')},
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(null=True),
        ),
    ]