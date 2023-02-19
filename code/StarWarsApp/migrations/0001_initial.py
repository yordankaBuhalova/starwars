# Generated by Django 4.1.6 on 2023-02-17 15:49

import StarWarsApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetCSV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(max_length=300, upload_to=StarWarsApp.models.directory_path, verbose_name='Path')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Created date')),
            ],
        ),
    ]
