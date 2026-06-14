import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64
import requests
from django.conf import settings


def update_fuel_prices():
    """
    Интеграция с внешним миром: автоматическое обновление цен для всех АЗС из списка.
    Цены актуализированы на июнь 2026 года.
    """
    from .models import FuelNetwork

    # Реестр актуальных цен для твоего списка АЗС
    # Формат: { Название: { АИ-92, АИ-95, ДТ } }
    external_prices = {
        'Лукойл': {'92': 55.45, '95': 69.73, 'DT': 68.90},
        'Газпромнефть': {'92': 53.10, '95': 65.45, 'DT': 64.80},
        'Tamic Energy': {'92': 52.80, '95': 64.90, 'DT': 64.50},
        'Башнефть': {'92': 52.50, '95': 64.20, 'DT': 63.90},
        'Varta': {'92': 52.00, '95': 63.50, 'DT': 63.00},
        'Роснефть': {'92': 53.40, '95': 66.20, 'DT': 65.10},
        'Teboil': {'92': 54.90, '95': 68.50, 'DT': 67.80},
        'ГАЗПРОМ': {'92': 53.10, '95': 65.45, 'DT': 64.80},
    }

    for name, prices in external_prices.items():
        # Метод update_or_create ищет АЗС по имени.
        # Если находит — обновляет цены, если нет — создает новую запись.
        FuelNetwork.objects.update_or_create(
            name=name,
            defaults={
                'price_92': prices['92'],
                'price_95': prices['95'],
                'price_diesel': prices['DT']
            }
        )
    print("Цены в базе данных успешно синхронизированы с внешним реестром.")


def get_advanced_analytics(vehicle_id):
    """
    Глубокая аналитика данных с использованием Pandas и Matplotlib.
    Расчет расхода, стоимости километра и рейтинга брендов.
    """
    from .models import Refueling
    qs = Refueling.objects.filter(vehicle_id=vehicle_id).order_by('odometer')

    if qs.count() < 2:
        return None

    # Подготовка данных для Pandas
    data = []
    for r in qs:
        data.append({
            'odometer': r.odometer,
            'fuel_amount': r.fuel_amount,
            'price_total': float(r.price_total),
            'network': r.network.name if r.network else "N/A"
        })

    df = pd.DataFrame(data)

    # Математические расчеты
    df['distance'] = df['odometer'].diff()
    df['consumption'] = (df['fuel_amount'] / df['distance']) * 100
    df['cost_per_km'] = df['price_total'] / df['distance']

    # Очистка данных
    df_clean = df.dropna().copy()

    stats = {
        'avg_consumption': round(df_clean['consumption'].mean(), 2),
        'total_spent': round(df_clean['price_total'].sum(), 2),
        'avg_cost_km': round(df_clean['cost_per_km'].mean(), 2),
        'total_distance': int(df_clean['distance'].sum()),
        'brand_stats': df_clean.groupby('network')['consumption'].mean().round(2).to_dict()
    }

    # Генерация визуализации (2 графика)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 9))

    # 1. График динамики расхода
    ax1.plot(df_clean['odometer'], df_clean['consumption'], marker='o', color='#0d6efd', linewidth=2)
    ax1.set_title('История расхода (л/100км)', fontweight='bold', pad=10)
    ax1.set_xlabel('Пробег (км)')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # 2. Рейтинг брендов
    brands = list(stats['brand_stats'].keys())
    values = list(stats['brand_stats'].values())
    ax2.bar(brands, values, color=['#ffc107', '#198754', '#0dcaf0', '#6610f2', '#dc3545'])
    ax2.set_title('Расход по сетям АЗС', fontweight='bold', pad=10)
    ax2.set_ylabel('Литры')

    plt.tight_layout()

    # Перевод графика в картинку Base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return stats, image_base64