# forms.py
from django import forms
from .models import Reservation, Space, UserProfile
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


class EditProfileForm(UserChangeForm):
    password = None  # Exclude the password field

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'profile_picture']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class SpaceFilterForm(forms.Form):
    office_type = forms.ChoiceField(choices=[('', 'All Types')] + Space.OFFICE_TYPES, required=False, label="Office Type")
    capacity = forms.IntegerField(required=False, label="Capacity", widget=forms.NumberInput(attrs={'placeholder': 'Minimum capacity'}))
    location = forms.CharField(required=False, label="Location", widget=forms.TextInput(attrs={'placeholder': 'Enter location'}))
    price_per_hour = forms.DecimalField(required=False, max_digits=6, decimal_places=2, label="Max Price per Hour", widget=forms.NumberInput(attrs={'placeholder': 'Enter max price'}))
