# Generated by Django 5.0.7 on 2024-08-24 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare_app', '0013_rename_chatid_guardian_chatid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardian',
            name='RemindGuardian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='guardian',
            name='RemindPatient',
            field=models.BooleanField(default=False),
        ),
    ]