import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64


def get_advanced_analytics(vehicle_id):
    from .models import Refueling
    qs = Refueling.objects.filter(vehicle_id=vehicle_id).order_by('odometer')

    if qs.count() < 2:
        return None

    # Обработка данных через Pandas
    data = list(qs.values('odometer', 'fuel_amount', 'price_total'))
    df = pd.DataFrame(data)
    df['price_total'] = df['price_total'].astype(float)

    # Математика
    df['distance'] = df['odometer'].diff()
    df['consumption'] = (df['fuel_amount'] / df['distance']) * 100
    df['cost_per_km'] = df['price_total'] / df['distance']

    stats = {
        'avg_consumption': round(df['consumption'].mean(), 2),
        'total_spent': round(df['price_total'].sum(), 2),
        'avg_cost_km': round(df['cost_per_km'].mean(), 2),
        'total_distance': int(df['distance'].sum())
    }

    # Красивый график Matplotlib
    plt.figure(figsize=(6, 4))
    plt.plot(df['odometer'].tail(10), df['consumption'].tail(10), marker='o', color='#ffc107', linewidth=3)
    plt.fill_between(df['odometer'].tail(10), df['consumption'].tail(10), color='#ffc107', alpha=0.2)
    plt.title('Динамика расхода топлива')
    plt.xlabel('Пробег')
    plt.ylabel('Л/100км')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return stats, image_base64