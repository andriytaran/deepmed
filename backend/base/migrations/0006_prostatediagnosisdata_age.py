# Generated by Django 2.0.2 on 2018-03-05 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_prostatediagnosisdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='prostatediagnosisdata',
            name='age',
            field=models.IntegerField(default=18),
        ),
    ]
