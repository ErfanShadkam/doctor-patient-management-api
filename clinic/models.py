from django.db import models
from django.conf import settings


class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    available_from = models.TimeField(null=True,blank=True)
    available_to = models.TimeField(null=True,blank=True)
    
    

class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True)
    
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="appointments")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="appointments")
    scheduled_at = models.DateTimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)



