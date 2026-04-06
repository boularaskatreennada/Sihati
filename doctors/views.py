from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from accounts.models import DoctorProfile
from .models import Appointment
from .forms import AppointmentForm

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor

            # calcul end_time automatiquement
            duration = 30  # ou depuis availability
            start = datetime.combine(appointment.date, appointment.start_time)
            end = start + timedelta(minutes=duration)

            appointment.end_time = end.time()
            appointment.status = "pending"

            # check conflit
            conflict = Appointment.objects.filter(
                doctor=doctor,
                date=appointment.date,
                start_time=appointment.start_time
            ).exists()

            if conflict:
                return render(request, "appointments/book.html", {
                    "form": form,
                    "doctor": doctor,
                    "error": "Créneau déjà réservé"
                })

            appointment.save()
            return redirect("patient_appointments")

    else:
        form = AppointmentForm()

    return render(request, "appointments/book.html", {
        "form": form,
        "doctor": doctor
    })