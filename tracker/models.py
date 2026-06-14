from django.db import models
from django.contrib.auth.models import User

class FuelNetwork(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название сети")
    price_92 = models.FloatField(default=50.0, verbose_name="Цена 92")
    price_95 = models.FloatField(default=55.0, verbose_name="Цена 95")
    price_diesel = models.FloatField(default=60.0, verbose_name="Цена ДТ")

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    brand = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")
    def __str__(self):
        return f"{self.brand} {self.model}"

class Refueling(models.Model):
    FUEL_CHOICES = [
        ('92', 'АИ-92'),
        ('95', 'АИ-95'),
        ('DT', 'Дизель'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='refuelings', verbose_name="Автомобиль")
    network = models.ForeignKey(FuelNetwork, on_delete=models.SET_NULL, null=True, verbose_name="Сеть АЗС")
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES, default='95', verbose_name="Тип топлива")
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    odometer = models.PositiveIntegerField(verbose_name="Пробег (км)")
    fuel_amount = models.FloatField(verbose_name="Количество литров")
    price_per_liter = models.FloatField(verbose_name="Цена за 1 литр")
    price_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    latitude = models.FloatField(verbose_name="Широта", blank=True, null=True)
    longitude = models.FloatField(verbose_name="Долгота", blank=True, null=True)

    class Meta:
        ordering = ['-odometer']

    def __str__(self):
        return f"{self.date} - {self.vehicle.brand} ({self.fuel_type})"