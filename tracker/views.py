from django.shortcuts import render, redirect
from .models import Refueling, Vehicle
from .forms import RefuelingForm
from .services import calculate_fuel_consumption, get_consumption_chart


def dashboard(request):
    # Данные из базы
    refuelings = Refueling.objects.all().order_by('-odometer')
    vehicle = Vehicle.objects.first()

    # Расчеты
    avg_consumption = None
    chart = None
    if vehicle:
        avg_consumption = calculate_fuel_consumption(vehicle.id)
        chart = get_consumption_chart(vehicle.id)

    # Словарь контекста для шаблона
    context = {
        'refuelings': refuelings,
        'avg_consumption': avg_consumption,
        'vehicle': vehicle,
        'chart': chart,
    }
    return render(request, 'tracker/dashboard.html', context)


def add_refueling(request):
    if request.method == 'POST':
        form = RefuelingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RefuelingForm()
    return render(request, 'tracker/add_refueling.html', {'form': form})