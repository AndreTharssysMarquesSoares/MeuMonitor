from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('definir-senha/', views.definir_senha_view, name='definir_senha'),
    path('concluir-cadastro/', views.concluir_cadastro_view, name='concluir_cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('disciplinas/', views.disciplinas, name='disciplinas'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='login'), 
]