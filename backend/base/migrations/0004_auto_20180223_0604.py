# Generated by Django 2.0.2 on 2018-02-23 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20180222_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breastdiagnosisdata',
            name='tumor_grade',
            field=models.FloatField(),
        ),
    ]
