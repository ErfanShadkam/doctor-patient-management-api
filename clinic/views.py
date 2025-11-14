from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DoctorProfile, PatientProfile, Appointment, Prescription
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer, PrescriptionSerializer
from .permissions import IsDoctor, IsPatient, IsAppointmentOwnerOrDoctor
from django.shortcuts import get_object_or_404
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsPatient]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAppointmentOwnerOrDoctor]

    def perform_create(self, serializer):
        profile = get_object_or_404(PatientProfile, user=self.request.user)
        serializer.save(patient=profile)

    @action(detail=True, methods=["post"], permission_classes=[IsDoctor])
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = "confirmed"
        appointment.save()
        return Response({"status": "confirmed"})

    @action(detail=True, methods=["post"], permission_classes=[IsDoctor])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = "cancelled"
        appointment.save()
        return Response({"status": "cancelled"})

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctor]
