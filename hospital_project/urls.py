
from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctors_list'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('', views.home, name='home'),
    path('appointment/success/', views.appointment_success, name='appoinment_success'),
    path('patients/', views.patients_list, name='patients_list'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('appointments/update-status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('login/', views.login_view, name='login'),  # add this
    path('logout/', views.logout_view, name='logout')

]

