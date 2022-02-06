from re import template
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView ,LogoutView

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', LoginView.as_view(template_name='app/login.html'), name="login"),
    path('logout/',LogoutView.as_view(template_name='app/logout.html'), name="logout"),
]