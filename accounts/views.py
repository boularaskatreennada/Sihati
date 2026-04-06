from reviews.models import DoctorReview
from django.shortcuts import render
from django.contrib import messages
from .forms import *
from django.views import View
from django.shortcuts import redirect
from .models import User, PatientProfile, DoctorProfile
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from marketplace.models import Product
from pharmacy.models import PharmacyStock
from django.db.models import Q
from doctors.models import *


def home(request):
    reviews = DoctorReview.objects.all().order_by('-created_at')[:3]
    return render(request, 'patient/home.html', {'reviews': reviews})




def register_patient(request):

    if request.method == "POST":
        user_form = PatientRegisterForm(request.POST)
        profile_form = PatientProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            email = user_form.cleaned_data["email"]

            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email déjà utilisé")
                return redirect("register_patient")

            try:
                with transaction.atomic():

                    
                    user = user_form.save(commit=False)
                    user.username = email
                    user.role = "patient"
                    user.set_password(user_form.cleaned_data["password"])
                    user.save()

                 
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()

                messages.success(request, "Compte créé avec succès")
                login(request, user)
                return redirect("patient_dashboard")

            except Exception as e:
                messages.error(request, "Erreur lors de la création du compte")

        else:
            messages.error(request, "Veuillez corriger les erreurs")

    else:
        user_form = PatientRegisterForm()
        profile_form = PatientProfileForm()

    return render(request, "patient/register.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })

def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == "patient":
                return redirect("patient_home")

            """elif user.role == "doctor":
                return redirect("doctor_dashboard")

            elif user.role == "seller":
                return redirect("seller_dashboard")

            elif user.role == "admin":
                return redirect("/admin/")"""

        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, "patient/login.html")



def logout_view(request):
    logout(request)
    return redirect("login")



@login_required
def patient_home(request):

    if request.user.role != "patient":
        return redirect("login")

    user = request.user

    
    doctors = DoctorProfile.objects.filter(
        wilaya=user.wilaya,
        commune=user.commune,
        is_validated=True
    )[:3]

  
    pharmacies = PharmacyStock.objects.select_related('seller')[:3]

    products = Product.objects.filter(status="active")[:3]

    context = {
        "user": user,
        "doctors": doctors,
        "pharmacies": pharmacies,
        "products": products,
    }

    return render(request, "patient/patient_home.html", context)

@login_required
def patient_dashboard(request):

    if request.user.role != "patient":
        return redirect("login")

    user = request.user

    context = {
        "user": user,
        "appointments": user.appointments_as_patient.all() if hasattr(user, 'appointments_as_patient') else [],
        "orders": user.orders.all() if hasattr(user, 'orders') else [],
        "reservations": user.medicine_reservations.all() if hasattr(user, 'medicine_reservations') else [],
    }

    return render(request, "patient/dash.html", context)




def doctor_list(request):

    doctors = DoctorProfile.objects.filter(is_validated=True)

    query = request.GET.get("q")
    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )


    speciality = request.GET.get("speciality")
    if speciality:
        doctors = doctors.filter(speciality__icontains=speciality)

    wilaya = request.GET.get("wilaya")
    commune = request.GET.get("commune")

    if wilaya:
        doctors = doctors.filter(wilaya__icontains=wilaya)

    if commune:
        doctors = doctors.filter(commune__icontains=commune)

   
    rating = request.GET.get("rating")
    if rating:
        doctors = doctors.filter(rating__gte=rating)

    context = {
        "doctors": doctors
    }

    return render(request, "patient/doctors_list.html", context)

def doctor_profile(request, id):
    doctor = DoctorProfile.objects.select_related('user', 'speciality').get(id=id)

    return render(request, "patient/doctor_profile.html", {
        "doctor": doctor
    })