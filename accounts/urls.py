from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/patient/', register_patient, name='register_patient'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("home/", patient_home, name="patient_home"),
    path("profile/", patient_dashboard, name="patient_dashboard"), 
    path("doctors/", doctor_list, name="doctor_list"),
path("doctors/<int:id>/", doctor_profile, name="doctor_profile"),
]