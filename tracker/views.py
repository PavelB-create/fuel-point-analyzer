from django.shortcuts import render, redirect
from .models import Refueling, Vehicle
from .forms import RefuelingForm
from .services import calculate_fuel_consumption


def dashboard(request):
    # Получаем все заправки
    refuelings = Refueling.objects.all()

    # Пример аналитики для первого авто в базе
    vehicle = Vehicle.objects.first()
    avg_consumption = None
    if vehicle:
        avg_consumption = calculate_fuel_consumption(vehicle.id)

    context = {
        'refuelings': refuelings,
        'avg_consumption': avg_consumption,
        'vehicle': vehicle
    }
    return render(request, 'tracker/dashboard.html', context)