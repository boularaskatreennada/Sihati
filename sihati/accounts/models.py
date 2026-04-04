from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        DOCTOR = 'doctor', 'Médecin'
        SELLER = 'seller', 'Vendeur'
        ADMIN = 'admin', 'Administrateur'

    role = models.CharField(max_length=20, choices=Role.choices)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    wilaya = models.CharField(max_length=100, blank=True)
    commune = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"


class PatientProfile(models.Model):
    class BloodGroup(models.TextChoices):
        A_POS = 'A+', 'A+'
        A_NEG = 'A-', 'A-'
        B_POS = 'B+', 'B+'
        B_NEG = 'B-', 'B-'
        AB_POS = 'AB+', 'AB+'
        AB_NEG = 'AB-', 'AB-'
        O_POS = 'O+', 'O+'
        O_NEG = 'O-', 'O-'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Homme'), ('female', 'Femme')], blank=True)
    blood_group = models.CharField(max_length=5, choices=BloodGroup.choices, blank=True)
    allergies = models.TextField(blank=True)
    chronic_diseases = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    speciality = models.ForeignKey('doctors.Speciality', on_delete=models.SET_NULL, null=True)
    license_number = models.CharField(max_length=100, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    clinic_name = models.CharField(max_length=200, blank=True)
    clinic_address = models.TextField(blank=True)
    wilaya = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_validated = models.BooleanField(default=False)
    validated_at = models.DateTimeField(null=True, blank=True)
    validated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='validated_doctors'
    )

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"


class DoctorDocument(models.Model):
    class DocType(models.TextChoices):
        DIPLOMA = 'diploma', 'Diplôme'
        LICENSE = 'license', 'Numéro de registre'
        OTHER = 'other', 'Autre'

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DocType.choices)
    file = models.FileField(upload_to='doctor_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_type} – {self.doctor}"


class SellerProfile(models.Model):
    class SellerType(models.TextChoices):
        PHARMACY = 'pharmacy', 'Pharmacie'
        PARAPHARMACY = 'parapharmacy', 'Parapharmacie'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    seller_type = models.CharField(max_length=20, choices=SellerType.choices)
    business_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True)
    wilaya = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    opening_hours = models.JSONField(default=dict)   # {"monday": {"open":"08:00","close":"20:00"}, ...}
    logo = models.ImageField(upload_to='seller_logos/', null=True, blank=True)
    is_validated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    validated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='validated_sellers'
    )

    def __str__(self):
        return f"{self.business_name} ({self.get_seller_type_display()})"


class SellerDocument(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='seller_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_type} – {self.seller}"
