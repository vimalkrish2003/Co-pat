# Generated by Django 5.0.7 on 2024-07-21 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare_app', '0011_medication_frequency_patient_prescription_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardian',
            name='chatID',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='patient',
            name='chatID',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
