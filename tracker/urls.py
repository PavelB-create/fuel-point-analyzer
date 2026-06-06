from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard, add_refueling, register

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('add/', add_refueling, name='add_refueling'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]