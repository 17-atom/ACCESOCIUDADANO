from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='Usuarios:login'), name='logout'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
]

