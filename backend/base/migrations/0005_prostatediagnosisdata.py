# Generated by Django 2.0.2 on 2018-03-05 00:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0004_auto_20180223_0604'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProstateDiagnosisData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sex', models.CharField(default='Male', max_length=64)),
                ('ethnicity', models.CharField(max_length=64)),
                ('tumor_size_in_mm', models.IntegerField(blank=True, default=0, null=True)),
                ('gleason_primary', models.IntegerField(blank=True, default=0, null=True)),
                ('gleason_secondary', models.IntegerField(blank=True, default=0, null=True)),
                ('psa', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prostate_cancer_diagnoses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
