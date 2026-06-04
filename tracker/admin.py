from django.contrib import admin
from .models import FuelNetwork, Vehicle, Refueling

@admin.register(FuelNetwork)
class FuelNetworkAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'owner')
    list_filter = ('brand', 'owner')
    search_fields = ('brand', 'model')

@admin.register(Refueling)
class RefuelingAdmin(admin.ModelAdmin):
    # Что отображать в списке записей
    list_display = ('date', 'vehicle', 'network', 'odometer', 'fuel_amount', 'price_total')
    # По каким полям можно фильтровать (справа появится панель)
    list_filter = ('network', 'vehicle', 'date')
    # По каким полям искать
    search_fields = ('vehicle__brand', 'network__name')
    # Возможность редактировать прямо из списка
    list_editable = ('fuel_amount', 'price_total')