# FuelPoint Analyzer 🚗⛽

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-orange.svg)](https://pandas.pydata.org/)

**FuelPoint Analyzer** — это интеллектуальный веб-сервис для автовладельцев, позволяющий вести точный мониторинг топливной эффективности. В отличие от штатных бортовых компьютеров, сервис анализирует данные методом «от бака до бака», выявляет реальный расход в зависимости от бренда АЗС и визуализирует географию заправок.

---

## ✨ Ключевые возможности

*   **🗺️ Интерактивные карты 2ГИС:** Визуализация истории заправок на современной карте (MapGL). Удобный выбор местоположения кликом.
*   **🔍 Умный поиск АЗС:** Интеграция с **2GIS Places API** позволяет находить конкретные станции по названию или адресу прямо в интерфейсе.
*   **📊 Глубокая аналитика (Pandas):** 
    *   Расчет среднего расхода (л/100км).
    *   Оценка стоимости одного километра пути.
    *   Рейтинг эффективности топливных сетей (сравнение брендов).
*   **📈 Визуализация трендов (Matplotlib):** Автоматическая генерация графиков динамики расхода и диаграмм эффективности.
*   **🤖 Автоматизация ввода:** Цены на топливо (АИ-92, АИ-95, ДТ) синхронизируются с внешним реестром и подставляются в форму автоматически.
*   **🔐 Безопасность:** Персональные личные кабинеты. Все секретные ключи API изолированы через переменные окружения (`.env`).

---

## 🛠 Технологический стек

*   **Backend:** Python 3.x, Django 5.0.6
*   **Анализ данных:** Pandas, Matplotlib
*   **Геоданные:** 2GIS MapGL JS API, 2GIS Search API
*   **Frontend:** JavaScript (ES6), Bootstrap 5, HTML5/CSS3
*   **Окружение:** python-dotenv (управление секретами), requests

---

## 🚀 Быстрый запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/PavelB-create/fuel-point-analyzer.git
cd fuel-point-analyzer

```

---

### 2. Настройка виртуального окружения
```bash
python -m venv venv

# Для Windows:
venv\Scripts\activate

# Для Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

---

### 3. Настройка переменных окружения
```bash
DEBUG=True
SECRET_KEY='ваш_секретный_ключ_django'
DG_API_KEY='ваш_api_ключ_2gis'
```

---

### 4. Инициализация базы данных
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

### 5. Запуск сервера
```bash
python manage.py runserver
```
## 📂 Структура проекта

*   **core/** — Настройки Django проекта.
*   **tracker/** — Приложение мониторинга (модели, логика).
*   **tracker/services.py** — Аналитика Pandas и Matplotlib.
*   **templates/** — HTML-шаблоны страниц.

