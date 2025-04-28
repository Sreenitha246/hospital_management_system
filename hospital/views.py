from django.shortcuts import render,redirect
from .models import Doctor, Appointment,Patient,Treatment
from django.utils import timezone
from django.shortcuts import get_object_or_404
def home(request):
    return render(request, 'hospital/home.html')


def doctor_list(request):
    doctors = Doctor.objects.select_related('user', 'specialization').all()
    return render(request, 'hospital/doctors_list.html', {'doctors': doctors})

def appointment_list(request):
    appointments = Appointment.objects.all()  # Fetch all appointments, or filter them based on the doctor having appointments
    return render(request, 'hospital/appointment_list.html', {'appointments': appointments})

from django.contrib.auth.models import User

def create_appointment(request):
    if request.method == 'POST':
        # 1. Get patient details from form
        name = request.POST.get('patient_name')
        age = request.POST.get('patient_age')
        gender = request.POST.get('patient_gender')
        address = request.POST.get('patient_address')
        phone = request.POST.get('patient_phone')

        # 2. Create Patient entry (no need to create User now)
        patient = Patient.objects.create(
            name=name,
            age=age,
            gender=gender,
            address=address,
            phone=phone
        )

        # 3. Get appointment data
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = request.POST.get('status')
        symptoms = request.POST.get('symptoms')  # if you add symptoms field in form

        # 4. Get Doctor object
        doctor = Doctor.objects.get(id=doctor_id)

        # 5. Create Appointment entry
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,   # NOT appointment_date anymore
            time=time,
            status=status,
            symptoms=symptoms
        )

        # 6. Redirect to success page
        return redirect('appoinment_success')  # careful: typo in URL name ('appoinment')

    # For GET request, display the form
    doctors = Doctor.objects.all()
    return render(request, 'hospital/create_appointment.html', {'doctors': doctors})

def appointment_success(request):
    return render(request, 'hospital/appoinment_success.html')  # Make sure the template exists

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Get all appointments for this patient
    appointments = Appointment.objects.filter(patient=patient)
    
    # Get all treatments related to the patient's appointments
    treatments = Treatment.objects.filter(appointment__in=appointments)
    
    return render(request, 'hospital/patient_detail.html', {
        'patient': patient,
        'appointments': appointments,
        'treatments': treatments,
    })


def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'hospital/patients_list.html', {'patients': patients})

from django.http import JsonResponse

def update_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Scheduled', 'Completed', 'Cancelled']:
            appointment.status = new_status
            appointment.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Patient, Appointment, Doctor  # import your models

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Appointment, Patient, Doctor

@login_required(login_url='login')  # Important
@user_passes_test(lambda user: user.is_staff)  # Only staff can access
def admin_dashboard(request):
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()
    total_doctors = Doctor.objects.count()
    recent_appointments = Appointment.objects.order_by('-date')[:5]

    context = {
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_doctors': total_doctors,
        'recent_appointments': recent_appointments,
    }
    return render(request, 'hospital/admin_dashboard.html', context) 

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')  # After login → go to dashboard
        else:
            error = "Invalid username or password"
            return render(request, 'hospital/login.html', {'error': error})
    return render(request, 'hospital/login.html')
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')
from hospital.models import Appointment

def appointment_stats(request):
    appointments = Appointment.objects.all()
    
    if not appointments:
        appointments_data = {'dates': [], 'values': []}  # Empty data
    else:
        appointments_data = {
            'dates': [appointment.date for appointment in appointments],
            'values': [appointment.count for appointment in appointments],  # Adjust as needed
        }
    
    return render(request, 'hospital/appointment_stats.html', {'appointments': appointments_data}) 