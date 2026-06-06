from django.shortcuts import render, redirect
from .models import Refueling, Vehicle
from .forms import RefuelingForm
from .services import get_advanced_analytics  # Импортируем новую функцию


def dashboard(request):
    refuelings = Refueling.objects.all().order_by('-odometer')
    vehicle = Vehicle.objects.first()

    stats = None
    chart = None

    if vehicle:
        analytics = get_advanced_analytics(vehicle.id)
        if analytics:
            stats, chart = analytics  # Получаем кортеж (статистика, график)

    return render(request, 'tracker/dashboard.html', {
        'refuelings': refuelings,
        'vehicle': vehicle,
        'stats': stats,
        'chart': chart,
    })


def add_refueling(request):
    if request.method == 'POST':
        form = RefuelingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RefuelingForm()
    return render(request, 'tracker/add_refueling.html', {'form': form})