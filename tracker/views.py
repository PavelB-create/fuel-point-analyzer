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


from django.shortcuts import render, redirect
from .forms import RefuelingForm


# ... (остальные импорты)

def add_refueling(request):
    if request.method == 'POST':
        form = RefuelingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # После сохранения возвращаемся на главную
    else:
        form = RefuelingForm()

    return render(request, 'tracker/add_refueling.html', {'form': form})