from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_doctor and request.user.is_authenticated)
    
    
class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_patient and request.user.is_authenticated)
    
    
class IsAppointmentOwnerOrDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj is Appointment
        return request.user == obj.patient.user or request.user == obj.doctor.user or request.user.is_staff