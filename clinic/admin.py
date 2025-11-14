from django.contrib import admin

from clinic.models import DoctorProfile,PatientProfile,Appointment,Prescription

# Register your models here.


admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(Appointment)
admin.site.register(Prescription)