from django.contrib import admin
from .models import DoctorProfile, PatientProfile, Appointment, Prescription


# --------------------------
# Prescription Inline (One-to-One)
# --------------------------
class PrescriptionInline(admin.StackedInline):
    model = Prescription
    extra = 0
    max_num = 1   # One-to-One
    can_delete = True


# --------------------------
# Doctor Admin
# --------------------------
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "specialization", "available_from", "available_to")
    search_fields = ("user__username", "full_name", "specialization")
    list_filter = ("specialization",)


# --------------------------
# Patient Admin
# --------------------------
@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "birth_date")
    search_fields = ("user__username", "full_name")
    list_filter = ("birth_date",)


# --------------------------
# Appointment Admin + Inline Prescription
# --------------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "doctor", "patient", "scheduled_at", "status")
    list_filter = ("status", "doctor", "scheduled_at")
    search_fields = ("doctor__user__username", "patient__user__username")
    inlines = [PrescriptionInline]   # <--- SHOW PRESCRIPTION INSIDE APPOINTMENT
    readonly_fields = ("created_at",)


# --------------------------
# Prescription Admin
# --------------------------
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "appointment", "notes")
    search_fields = ("appointment__doctor__user__username", "appointment__patient__user__username")
