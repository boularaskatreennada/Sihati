from django.db import models
from django.conf import settings


class Speciality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='specialities/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Specialities'

    def __str__(self):
        return self.name


class Availability(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, 'Lundi'
        TUESDAY = 1, 'Mardi'
        WEDNESDAY = 2, 'Mercredi'
        THURSDAY = 3, 'Jeudi'
        FRIDAY = 4, 'Vendredi'
        SATURDAY = 5, 'Samedi'
        SUNDAY = 6, 'Dimanche'

    doctor = models.ForeignKey(
        'accounts.DoctorProfile', on_delete=models.CASCADE, related_name='availabilities'
    )
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration_minutes = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'day_of_week', 'start_time')

    def __str__(self):
        return f"{self.doctor} – {self.get_day_of_week_display()} {self.start_time}–{self.end_time}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        CONFIRMED = 'confirmed', 'Confirmé'
        REFUSED = 'refused', 'Refusé'
        CANCELLED_BY_PATIENT = 'cancelled_patient', 'Annulé par le patient'
        CANCELLED_BY_DOCTOR = 'cancelled_doctor', 'Annulé par le médecin'
        COMPLETED = 'completed', 'Terminé'
        NO_SHOW = 'no_show', 'Absent'

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_patient'
    )
    doctor = models.ForeignKey(
        'accounts.DoctorProfile', on_delete=models.CASCADE, related_name='appointments'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    reason = models.TextField(blank=True)
    notes_by_doctor = models.TextField(blank=True)
    confirmation_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"RDV {self.patient} ↔ {self.doctor} le {self.date} à {self.start_time}"


class MedicalNote(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='medical_note')
    doctor = models.ForeignKey(
        'accounts.DoctorProfile', on_delete=models.CASCADE, related_name='medical_notes'
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medical_notes'
    )
    content = models.TextField()
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note médicale – {self.appointment}"