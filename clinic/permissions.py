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



class IsDoctorOwnPatient(BasePermission):
    """
    Doctors can access only patients they have appointments with.
    Admins can access all.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser or user.is_staff:
            return True

        if not hasattr(user, 'doctorprofile'):
            return False  # Not a doctor

        doctor_profile = user.doctorprofile

        # Check if this patient has an appointment with this doctor
        return obj.appointments.filter(doctor=doctor_profile).exists()


class IsOwnerProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user



class PrescriptionPermission(BasePermission):
    """
    - Doctors: can create prescriptions for their patients and read them
    - Patients: can only read their own prescriptions
    - Admin/Staff: full access
    """

    def has_permission(self, request, view):
        # Admin/staff can do everything
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Doctors can do GET, POST
        if hasattr(request.user, "doctorprofile"):
            return request.method in SAFE_METHODS + ("POST",)

        # Patients can only GET
        if hasattr(request.user, "patientprofile"):
            return request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser or user.is_staff:
            return True

        # Doctors: can only access prescriptions of their patients
        if hasattr(user, "doctorprofile"):
            return obj.appointment.doctor == user.doctorprofile

        # Patients: can only access prescriptions of their own appointments
        if hasattr(user, "patientprofile"):
            return obj.appointment.patient == user.patientprofile

        return False



class IsOwnerPatientProfile(BasePermission):
    """
    بیماران فقط می‌توانند پروفایل خودشان را ببینند / ویرایش کنند.
    دکترها فقط مریض‌های خودشون و Admin/Staff همه
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True
        if hasattr(user, "doctorprofile"):
            return obj.appointments.filter(doctor=user.doctorprofile).exists()
        if hasattr(user, "patientprofile"):
            return obj.user == user
        return False