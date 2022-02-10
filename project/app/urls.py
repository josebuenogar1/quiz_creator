from re import template
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView ,LogoutView

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', LoginView.as_view(template_name='app/login.html'), name="login"),
    path('logout/',LogoutView.as_view(template_name='app/logout.html'), name="logout"),
    path('quiz/<str:quiz_name>/',views.quiz, name="quiz"),
    path('student/<str:profile>/<str:quiz_name>/<str:token>',views.student_quiz, name="student_quiz"),
    path('generate_link/<str:quiz_name>',views.generate_link, name="generate_link"),  
]