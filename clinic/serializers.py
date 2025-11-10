from rest_framework import serializers
from .models import DoctorProfile, PatientProfile, Appointment

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["id","user","specialization","bio","available_from","available_to"]

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ["id","user","birth_date","medical_history"]

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["id","doctor","patient","scheduled_at","reason","status","created_at"]