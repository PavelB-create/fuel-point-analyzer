import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64


def update_fuel_prices():
    """Имитация получения данных через внешний API реестр цен"""
    from .models import FuelNetwork
    # Пример данных, которые могли бы прийти по API
    external_prices = {
        'Лукойл': {'92': 51.50, '95': 56.80, 'DT': 62.40},
        'ГАЗПРОМ': {'92': 50.90, '95': 55.70, 'DT': 61.20},
        'Роснефть': {'92': 50.40, '95': 55.10, 'DT': 60.80},
    }
    for name, prices in external_prices.items():
        net, created = FuelNetwork.objects.get_or_create(name=name)
        net.price_92 = prices['92']
        net.price_95 = prices['95']
        net.price_diesel = prices['DT']
        net.save()


def get_advanced_analytics(vehicle_id):
    from .models import Refueling
    qs = Refueling.objects.filter(vehicle_id=vehicle_id).order_by('odometer')
    if qs.count() < 2: return None

    data = []
    for r in qs:
        data.append({
            'odometer': r.odometer,
            'fuel_amount': r.fuel_amount,
            'price_total': float(r.price_total),
            'network': r.network.name if r.network else "N/A"
        })

    df = pd.DataFrame(data)
    df['distance'] = df['odometer'].diff()
    df['consumption'] = (df['fuel_amount'] / df['distance']) * 100
    df['cost_per_km'] = df['price_total'] / df['distance']
    df_clean = df.dropna().copy()

    stats = {
        'avg_consumption': round(df_clean['consumption'].mean(), 2),
        'avg_cost_km': round(df_clean['cost_per_km'].mean(), 2),
        'brand_stats': df_clean.groupby('network')['consumption'].mean().round(2).to_dict()
    }

    # Генерация двойного графика
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
    ax1.plot(df_clean['odometer'], df_clean['consumption'], marker='o', color='#0d6efd', linewidth=2)
    ax1.set_title('Динамика расхода (л/100км)')
    ax1.grid(True, alpha=0.3)

    brands = list(stats['brand_stats'].keys())
    values = list(stats['brand_stats'].values())
    ax2.bar(brands, values, color=['#ffc107', '#198754', '#0dcaf0'])
    ax2.set_title('Расход по брендам АЗС')

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()
    return stats, img