# Generated by Django 2.2.6 on 2020-01-18 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='projects',
            field=models.ManyToManyField(to='project_manager.Project'),
        ),
    ]
