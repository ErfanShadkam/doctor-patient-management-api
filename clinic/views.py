from rest_framework import viewsets,permissions
from .models import DoctorProfile, PatientProfile, Appointment
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer



class DoctorViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorSerializer
    
    
class PatientViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    
    def perform_create(self, serializer):
        profile = PatientProfile.objects.get(user=self.request.user)
        serializer.save(patient=profile)
    
    
    @action(detail=True, methods=["post"], permission_classes=[IsDoctor])
    def confirm(self, request, pk=None):
        appt = self.get_object()
        appt.status = "confirmed"
        appt.save()
        return Response({"status":"confirmed"})
