# Generated by Django 2.2.6 on 2020-01-27 23:32

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('p_key', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='p_key')),
                ('p_id', models.IntegerField()),
            ],
        ),
    ]
