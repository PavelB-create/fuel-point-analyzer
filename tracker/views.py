from django.shortcuts import render, redirect
from django.conf import settings
from .models import Refueling, Vehicle
from .forms import RefuelingForm
from .services import get_advanced_analytics


def dashboard(request):
    # Берем первую машину из базы
    vehicle = Vehicle.objects.first()

    # Инициализируем переменные
    refuelings = Refueling.objects.none()
    stats = None
    chart = None

    if vehicle:
        # Получаем заправки только для этой машины
        refuelings = Refueling.objects.filter(vehicle=vehicle).order_by('-odometer')

        # Если заправок 2 и более — запускаем аналитику Pandas
        if refuelings.count() >= 2:
            analytics = get_advanced_analytics(vehicle.id)
            if analytics:
                stats, chart = analytics  # Получаем кортеж (статистика, график)

    context = {
        'refuelings': refuelings,
        'vehicle': vehicle,
        'stats': stats,
        'chart': chart,
        'yandex_key': settings.YANDEX_MAPS_API_KEY,  # Передаем ключ из настроек
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

    context = {
        'form': form,
        'yandex_key': settings.YANDEX_MAPS_API_KEY,
    }
    return render(request, 'tracker/add_refueling.html', context)