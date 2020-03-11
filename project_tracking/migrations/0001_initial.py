# Generated by Django 2.2.6 on 2020-03-07 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('key', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=155)),
                ('category_id', models.IntegerField(null=True)),
                ('category_name', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssueTypes',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('project_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_tracking.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('key', models.CharField(max_length=10)),
                ('url', models.URLField()),
                ('summary', models.CharField(max_length=300)),
                ('description', models.TextField(null=True)),
                ('status_change_date', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('status_id', models.IntegerField()),
                ('status_name', models.CharField(max_length=30)),
                ('priority_id', models.IntegerField()),
                ('priority_name', models.CharField(max_length=40)),
                ('issue_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_tracking.IssueTypes')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_tracking.Project')),
            ],
        ),
    ]