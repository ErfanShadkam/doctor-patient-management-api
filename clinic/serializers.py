from rest_framework import serializers
from .models import DoctorProfile, PatientProfile, Appointment,Prescription

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["id","user","specialization","bio","available_from","available_to"]

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"

class PrescriptionSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"