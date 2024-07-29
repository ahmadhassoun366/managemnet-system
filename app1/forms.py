# forms.py
from django import forms
from .models import Reservation, Space

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SpaceFilterForm(forms.Form):
    office_type = forms.ChoiceField(choices=Space.OFFICE_TYPES, required=False, label="Office Type")
