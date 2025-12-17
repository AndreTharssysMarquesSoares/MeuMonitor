from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('definir-senha/', views.definir_senha_view, name='definir_senha'),
    path('concluir-cadastro/', views.concluir_cadastro_view, name='concluir_cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
]