from django.db import models
from django.conf import settings


class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,blank=True,null=True)
    specialization = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    available_from = models.TimeField(null=True,blank=True)
    available_to = models.TimeField(null=True,blank=True)
    
    
    def __str__(self):
        return f"Dr. {self.full_name or self.user.username} ({self.specialization})"
    

class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,null=True,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True)
    
    def __str__(self):
        return self.full_name or self.user.username

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="appointments", null=True, blank=True)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="appointments")
    scheduled_at = models.DateTimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment #{self.id} - {self.patient} with {self.doctor} at {self.scheduled_at}"


class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="prescription")
    notes = models.TextField()


    def __str__(self):
        return f"Prescription for appointment #{self.appointment.id}"

