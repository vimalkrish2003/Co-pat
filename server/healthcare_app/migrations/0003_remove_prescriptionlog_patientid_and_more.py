# Generated by Django 5.0.6 on 2024-07-03 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare_app', '0002_rename_email_guardian_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescriptionlog',
            name='PatientID',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='PatientID',
        ),
        migrations.RemoveField(
            model_name='prescriptionlog',
            name='PrescriptionID',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
        migrations.DeleteModel(
            name='Prescription',
        ),
        migrations.DeleteModel(
            name='PrescriptionLog',
        ),
    ]