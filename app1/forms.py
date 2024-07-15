from django import forms
from .models import Space

class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['name', 'capacity', 'amenities', 'location']  # Adjust fields according to your model attributes
