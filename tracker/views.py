import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Refueling, Vehicle, FuelNetwork
from .forms import RefuelingForm
from .services import get_advanced_analytics, update_fuel_prices


@login_required
def dashboard(request):
    vehicle = Vehicle.objects.filter(owner=request.user).first()
    refuelings = Refueling.objects.none()
    stats, chart = None, None

    if vehicle:
        refuelings = Refueling.objects.filter(vehicle=vehicle).order_by('-odometer')
        if refuelings.count() >= 2:
            stats, chart = get_advanced_analytics(vehicle.id)

    return render(request, 'tracker/dashboard.html', {
        'refuelings': refuelings, 'vehicle': vehicle, 'stats': stats,
        'chart': chart, 'dg_key': settings.DG_API_KEY
    })


@login_required
def add_refueling(request):
    update_fuel_prices()  # Синхронизация цен при загрузке страницы

    if request.method == 'POST':
        form = RefuelingForm(request.POST)
        if form.is_valid():
            ref = form.save(commit=False)
            if ref.vehicle.owner == request.user:
                ref.save()
                return redirect('dashboard')
    else:
        form = RefuelingForm()
        form.fields['vehicle'].queryset = Vehicle.objects.filter(owner=request.user)

    # Матрица цен для JS
    networks = FuelNetwork.objects.all()
    price_matrix = {n.id: {'92': n.price_92, '95': n.price_95, 'DT': n.price_diesel} for n in networks}

    return render(request, 'tracker/add_refueling.html', {
        'form': form, 'dg_key': settings.DG_API_KEY, 'price_matrix_json': json.dumps(price_matrix)
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})