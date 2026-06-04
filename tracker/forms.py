from django import forms
from .models import Refueling, Vehicle


class RefuelingForm(forms.ModelForm):
    class Meta:
        model = Refueling
        # Поля, которые пользователь будет заполнять в форме
        fields = ['vehicle', 'network', 'odometer', 'fuel_amount', 'price_total', 'latitude', 'longitude']

        # Добавим красивые стили Bootstrap для полей (чтобы формы не были "голыми")
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'network': forms.Select(attrs={'class': 'form-control'}),
            'odometer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Текущий пробег'}),
            'fuel_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Литров заправлено'}),
            'price_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сумма в чеке'}),
            'latitude': forms.HiddenInput(),  # Скроем координаты, будем заполнять их через карту
            'longitude': forms.HiddenInput(),
        }