# Generated by Django 4.1.6 on 2023-02-18 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StarWarsApp', '0002_alter_datasetcsv_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetcsv',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
    ]