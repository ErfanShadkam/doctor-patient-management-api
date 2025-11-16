from rest_framework import serializers
from .models import DoctorProfile, PatientProfile, Appointment,Prescription

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["id","user","specialization","bio","available_from","available_to"]

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ["full_name","birth_date","medical_history",'id']
        read_only_fields = ['id']

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"

class PrescriptionSerializer(serializers.ModelSerializer):
    appointment_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Prescription
        fields = ["id", "appointment", "appointment_id", "notes"]
        read_only_fields = ["appointment"]