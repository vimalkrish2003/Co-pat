from django.db import models
from healthcare_app.models import Guardian, Medication, Patient

class MedicationReminderForToday(models.Model):
    MedicationReminderForTodayID = models.AutoField(primary_key=True)
    GuardianID = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    GuardianChatID = models.CharField(max_length=255)
    RemindGuardian = models.BooleanField(default=False)  # Added field
    RemindPatient = models.BooleanField(default=False)   # Added field
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    PatientName = models.CharField(max_length=255)
    PatientChatID = models.CharField(max_length=255)
    MedicationID = models.ForeignKey(Medication, on_delete=models.CASCADE)
    MedicationName = models.CharField(max_length=255)
    Dosage = models.PositiveIntegerField()
    Label = models.TextField()
    NotificationTime = models.TimeField()
    isTaken = models.BooleanField(default=False)
    TimeTaken = models.TimeField(null=True, blank=True, default=None)

    class Meta:
        indexes = [
            models.Index(fields=['NotificationTime']),
            # Add other indexes as needed
        ]

class MedicationLog(models.Model):
    LogID = models.AutoField(primary_key=True)
    CurrentDateTime = models.DateTimeField(auto_now_add=True)
    GuardianID = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    MedicationID = models.ForeignKey(Medication, on_delete=models.CASCADE)
    NotificationTime = models.TimeField()
    isTaken = models.BooleanField(default=False)
    TimeTaken = models.TimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['GuardianID']),
            models.Index(fields=['PatientID']),
        ]