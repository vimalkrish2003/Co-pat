# Generated by Django 5.0.7 on 2024-07-19 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare_app', '0010_remove_medication_prescriptionid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('MedicationID', models.AutoField(primary_key=True, serialize=False)),
                ('MedicationName', models.CharField(max_length=255)),
                ('Label', models.CharField(max_length=255)),
                ('Dosage', models.PositiveIntegerField()),
                ('NotificationTime', models.TimeField()),
                ('StartDate', models.DateField()),
                ('EndDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Frequency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Monday', models.BooleanField(default=False)),
                ('Tuesday', models.BooleanField(default=False)),
                ('Wednesday', models.BooleanField(default=False)),
                ('Thursday', models.BooleanField(default=False)),
                ('Friday', models.BooleanField(default=False)),
                ('Saturday', models.BooleanField(default=False)),
                ('Sunday', models.BooleanField(default=False)),
                ('MedicationID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Frequencies', to='healthcare_app.medication')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('PatientID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
                ('DateOfBirth', models.DateField()),
                ('Gender', models.CharField(max_length=10)),
                ('PhoneNumber', models.CharField(max_length=20)),
                ('BloodType', models.CharField(max_length=5)),
                ('GuardianID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthcare_app.guardian')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('PrescriptionID', models.AutoField(primary_key=True, serialize=False)),
                ('Condition', models.CharField(max_length=255)),
                ('DoctorName', models.CharField(max_length=255)),
                ('PatientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthcare_app.patient')),
            ],
        ),
        migrations.AddField(
            model_name='medication',
            name='PrescriptionID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medications', to='healthcare_app.prescription'),
        ),
    ]