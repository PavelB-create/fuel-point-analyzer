from django.db import models
from django.contrib.auth.models import User


class FuelNetwork(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название сети")

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    brand = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")

    def __str__(self):
        return f"{self.brand} {self.model}"


class Refueling(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='refuelings')
    network = models.ForeignKey(FuelNetwork, on_delete=models.SET_NULL, null=True, verbose_name="Сеть АЗС")
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    odometer = models.PositiveIntegerField(verbose_name="Пробег (км)")
    fuel_amount = models.FloatField(verbose_name="Количество литров")

    # НОВОЕ ПОЛЕ: Цена за 1 литр
    price_per_liter = models.FloatField(verbose_name="Цена за 1 литр", default=55.0)

    price_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    latitude = models.FloatField(verbose_name="Широта", blank=True, null=True)
    longitude = models.FloatField(verbose_name="Долгота", blank=True, null=True)

    class Meta:
        ordering = ['-odometer']

    def __str__(self):
        return f"{self.date} - {self.vehicle.brand}"