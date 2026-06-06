from django import forms
from .models import Refueling, Vehicle

class RefuelingForm(forms.ModelForm):
    class Meta:
        model = Refueling
        fields = ['vehicle', 'network', 'odometer', 'fuel_amount', 'price_total', 'latitude', 'longitude']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'network': forms.Select(attrs={'class': 'form-control'}),
            'odometer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Текущий пробег'}),
            'fuel_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Литров заправлено'}),
            'price_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сумма в рублях'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }