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


class ReadOnlyForDoctors(BasePermission):
    """
    Doctors can only view (GET, LIST).
    Admin/staff can do everything.
    """

    def has_permission(self, request, view):
        # Admin & staff can do everything
        if request.user.is_superuser or request.user.is_staff:
            return True

        # If the user is a doctor → allow only safe methods (GET, HEAD, OPTIONS)
        if hasattr(request.user, "is_doctor") and request.user.is_doctor:
            return request.method in SAFE_METHODS

        # Patients should not access Doctor list at all
        return False


