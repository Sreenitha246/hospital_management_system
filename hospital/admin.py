from django.contrib import admin
from .models import Specialization, Doctor, Patient, Appointment, Treatment

admin.site.register(Specialization)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Treatment)
