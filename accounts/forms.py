from django import forms
from .models import User, PatientProfile


class PatientRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'phone', 'wilaya', 'commune'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")

        return cleaned_data


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = [
            'date_of_birth',
            'gender',
            'blood_group',
            'allergies',
            'chronic_diseases'
        ]