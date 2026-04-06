from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'start_time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

from .models import MedicalNote

class MedicalNoteForm(forms.ModelForm):
    class Meta:
        model = MedicalNote
        fields = ['content', 'diagnosis', 'prescription']