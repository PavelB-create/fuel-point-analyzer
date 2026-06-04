from django.urls import path
from .views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
]
from django.urls import path
from .views import dashboard, add_refueling # Добавь импорт

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('add/', add_refueling, name='add_refueling'), # Новый путь
]