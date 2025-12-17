from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('definir-senha/', views.definir_senha_view, name='definir_senha'),
    path('concluir-cadastro/', views.concluir_cadastro_view, name='concluir_cadastro'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('disciplinas/', views.disciplinas_view, name='disciplinas'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('interesses/', views.meus_interesses_view, name='meus_interesses'),

    path('admin/monitores/', views.admin_monitores_view, name='admin_monitores'),
    path('admin/disciplinas/', views.admin_disciplinas_view, name='admin_disciplinas'),
]