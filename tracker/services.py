import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64


def calculate_fuel_consumption(vehicle_id):
    from .models import Refueling
    qs = Refueling.objects.filter(vehicle_id=vehicle_id).order_by('odometer')
    if qs.count() < 2:
        return None

    data = list(qs.values('odometer', 'fuel_amount'))
    df = pd.DataFrame(data)
    df['distance'] = df['odometer'].diff()
    df['consumption'] = (df['fuel_amount'] / df['distance']) * 100
    return round(df['consumption'].mean(), 2)


def get_consumption_chart(vehicle_id):
    from .models import Refueling
    qs = Refueling.objects.filter(vehicle_id=vehicle_id).order_by('odometer')
    if qs.count() < 2:
        return None

    try:
        data = list(qs.values('odometer', 'fuel_amount'))
        df = pd.DataFrame(data)
        df['distance'] = df['odometer'].diff()
        df['consumption'] = (df['fuel_amount'] / df['distance']) * 100
        df = df.dropna()

        plt.figure(figsize=(5, 3))
        plt.plot(df['odometer'], df['consumption'], marker='o', color='#0d6efd', linewidth=2)
        plt.title('Динамика расхода (л/100км)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.close()
        return image_base64
    except:
        return None