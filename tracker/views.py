import json  # Добавь импорт json в самое начало
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Refueling, Vehicle, FuelNetwork  # Добавь FuelNetwork
from .forms import RefuelingForm
from .services import get_advanced_analytics


@login_required
def dashboard(request):
    vehicle = Vehicle.objects.filter(owner=request.user).first()
    refuelings = Refueling.objects.none()
    stats = None
    chart = None

    if vehicle:
        refuelings = Refueling.objects.filter(vehicle=vehicle).order_by('-odometer')
        if refuelings.count() >= 2:
            analytics = get_advanced_analytics(vehicle.id)
            if analytics:
                stats, chart = analytics

    context = {
        'refuelings': refuelings,
        'vehicle': vehicle,
        'stats': stats,
        'chart': chart,
        'dg_key': settings.DG_API_KEY,
    }
    return render(request, 'tracker/dashboard.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})


@login_required
def add_refueling(request):
    if request.method == 'POST':
        form = RefuelingForm(request.POST)
        if form.is_valid():
            refueling = form.save(commit=False)
            if refueling.vehicle.owner == request.user:
                refueling.save()
                return redirect('dashboard')
    else:
        form = RefuelingForm()
        form.fields['vehicle'].queryset = Vehicle.objects.filter(owner=request.user)

    # СОЗДАЕМ СЛОВАРЬ ЦЕН: {id_заправки: цена}
    networks = FuelNetwork.objects.all()
    price_map = {n.id: n.default_price for n in networks}

    context = {
        'form': form,
        'dg_key': settings.DG_API_KEY,
        'price_map_json': json.dumps(price_map)  # Превращаем в строку для JS
    }
    return render(request, 'tracker/add_refueling.html', context)