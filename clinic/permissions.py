from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True

        return bool(request.user and request.user.is_doctor and request.user.is_authenticated)
    
    
class IsPatient(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return bool(request.user and request.user.is_patient and request.user.is_authenticated)
    
    
class IsAppointmentOwnerOrDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        # obj is Appointment
        return request.user == obj.patient.user or request.user == obj.doctor.user or request.user.is_staff


