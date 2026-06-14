from django import forms
from .models import Refueling

class RefuelingForm(forms.ModelForm):
    class Meta:
        model = Refueling
        fields = ['vehicle', 'network', 'fuel_type', 'odometer', 'fuel_amount', 'price_per_liter', 'price_total', 'latitude', 'longitude']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'network': forms.Select(attrs={'class': 'form-select'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'odometer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Текущий пробег'}),
            'fuel_amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_fuel_amount', 'step': '0.01'}),
            'price_per_liter': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_price_per_liter', 'step': '0.01'}),
            'price_total': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_price_total', 'readonly': 'readonly'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }