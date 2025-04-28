from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'User'

class Specialization(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'Specialization'

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    contact = models.CharField(max_length=15)
    specialization = models.ForeignKey(Specialization, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Doctor'

from django.contrib.auth.models import User

class Patient(models.Model):
    # No user field now!
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.namey
    class Meta:
        managed = False
        db_table = 'Patient'

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Scheduled')
    symptoms = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.user.username} - {self.date}"
    
    class Meta:
        managed = False
        db_table = 'Appointment'

class Treatment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.DO_NOTHING)
    diagnosis = models.TextField()
    prescription = models.TextField()

    class Meta:
        managed = False
        db_table = 'Treatment'


# Create your models here.
