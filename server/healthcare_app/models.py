from django.db import models
from django.contrib.auth.models import User

class Guardian(models.Model):
    GuardianID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=255)
    LastName = models.CharField(max_length=255)
    UserID = models.OneToOneField(User, on_delete=models.CASCADE) 
    PhoneNumber = models.CharField(max_length=20)
    ChatID=models.CharField(max_length=255,default=None)
    Address = models.TextField()
    RelationshipToPatient = models.CharField(max_length=255)
    RemindGuardian = models.BooleanField(default=False)
    RemindPatient = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"

# Multiple patients for a single guardian
class Patient(models.Model):
    PatientID = models.AutoField(primary_key=True)
    GuardianID = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    DateOfBirth = models.DateField()
    Gender = models.CharField(max_length=10)
    PhoneNumber = models.CharField(max_length=20)
    ChatID=models.CharField(max_length=255,default=None)
    BloodType = models.CharField(max_length=5) 

    def __str__(self):
        return self.Name
    
# Multiple Prescriptions for a patient 
class Prescription(models.Model):
    PrescriptionID = models.AutoField(primary_key=True)
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Condition = models.CharField(max_length=255)
    DoctorName = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.Condition} - {self.DoctorName}"

# Modification to the existing Medication model
class Medication(models.Model):
    MedicationID = models.AutoField(primary_key=True)
    PrescriptionID = models.ForeignKey(Prescription, related_name='medications', on_delete=models.CASCADE)
    MedicationName = models.CharField(max_length=255)
    Label = models.CharField(max_length=255)  # E.g., After breakfast
    Dosage = models.PositiveIntegerField()  # E.g., 500
    NotificationTime = models.TimeField()  # Time for notification
    StartDate = models.DateField()
    EndDate = models.DateField()

    def __str__(self):
        return self.MedicationName

# New Frequency model
class Frequency(models.Model):
    MedicationID = models.ForeignKey(Medication, related_name='Frequencies', on_delete=models.CASCADE)
    Monday = models.BooleanField(default=False)
    Tuesday = models.BooleanField(default=False)
    Wednesday = models.BooleanField(default=False)
    Thursday = models.BooleanField(default=False)
    Friday = models.BooleanField(default=False)
    Saturday = models.BooleanField(default=False)
    Sunday = models.BooleanField(default=False)

    def __str__(self):
        days = []
        if self.Monday: days.append("Monday")
        if self.Tuesday: days.append("Tuesday")
        if self.Wednesday: days.append("Wednesday")
        if self.Thursday: days.append("Thursday")
        if self.Friday: days.append("Friday")
        if self.Saturday: days.append("Saturday")
        if self.Sunday: days.append("Sunday")
        return f"{self.MedicationID.MedicationName}: {' '.join(days)}"

    @classmethod
    def get_medication_ids_for_day(cls, day):
        day_field = day.capitalize()  # Ensure the first letter is uppercase to match the model fields
        if day_field not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            raise ValueError("Invalid day provided. Please enter a valid day of the week.")
        # Filter based on the given day being True
        frequencies = cls.objects.filter(**{day_field: True})
        # Extract the Medication IDs
        medication_ids = frequencies.values_list('MedicationID__id', flat=True)
        return list(medication_ids)
    
    def get_schedule_days(self):
        print(self)
        days = []
        if self.Monday: days.append("Monday")
        if self.Tuesday: days.append("Tuesday")
        if self.Wednesday: days.append("Wednesday")
        if self.Thursday: days.append("Thursday")
        if self.Friday: days.append("Friday")
        if self.Saturday: days.append("Saturday")
        if self.Sunday: days.append("Sunday")
        return days