import pandas as pd


def calculate_fuel_consumption(vehicle_id):
    """
    Функция берет все заправки авто и рассчитывает средний расход
    используя библиотеку Pandas (выполняем требование по аналитике).
    """
    from .models import Refueling

    # Получаем данные из БД
    qs = Refueling.objects.filter(vehicle_id=vehicle_id).order_by('odometer')

    if qs.count() < 2:
        return None  # Недостаточно данных для расчета

    # Преобразуем QuerySet в список словарей для Pandas
    data = list(qs.values('odometer', 'fuel_amount', 'price_total', 'network__name'))
    df = pd.DataFrame(data)

    # Считаем разницу в пробеге между заправками (метод diff)
    df['distance'] = df['odometer'].diff()

    # Расход на 100 км = (Литры / Дистанция) * 100
    # Берем литры из текущей заправки, а дистанцию пройденную ДО неё
    df['consumption'] = (df['fuel_amount'] / df['distance']) * 100

    # Считаем среднее, игнорируя первую строку (где distance = NaN)
    avg_consumption = df['consumption'].mean()

    return round(avg_consumption, 2)