from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DoctorProfile, PatientProfile, Appointment, Prescription
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer, PrescriptionSerializer
from .permissions import IsDoctor, IsPatient, IsAppointmentOwnerOrDoctor,ReadOnlyForDoctors,IsDoctorOwnPatient
from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models import Q


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, ReadOnlyForDoctors]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated,IsDoctorOwnPatient]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:

            return PatientProfile.objects.all()

        if hasattr(user, 'doctorprofile'):
            return PatientProfile.objects.filter(
                appointments__doctor=user.doctorprofile
            ).distinct()

        if hasattr(user, 'patientprofile'):

            return PatientProfile.objects.filter(user=user)


        return PatientProfile.objects.none()

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

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            # ادمین همه appointment ها را می‌بیند
            return Appointment.objects.all()

        if hasattr(user, 'doctorprofile'):
            # دکتر فقط appointmentهایی که خودش داره یا دکتر ندارد
            return Appointment.objects.filter(
                models.Q(doctor=None) | models.Q(doctor=user.doctorprofile)
            )

        if hasattr(user, 'patientprofile'):
            # بیمار فقط appointment خودش
            return Appointment.objects.filter(patient=user.patientprofile)

        return Appointment.objects.none()

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        appointment_id = serializer.validated_data.pop("appointment_id")

        appointment = get_object_or_404(Appointment, id=appointment_id)

        user = self.request.user
        if not hasattr(user, "doctorprofile") or appointment.doctor != user.doctorprofile:
            raise ValidationError("You can only create prescriptions for your own patients.")


        if hasattr(appointment, "prescription"):
            raise ValidationError("Prescription already exists")

        serializer.save(appointment=appointment)
