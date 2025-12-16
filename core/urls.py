from django.urls import path
from . import views  # Importa o arquivo views.py que criamos

urlpatterns = [
    # Rota da Home (chama a função 'home' do views.py)
    path('', views.home, name='home'),

    # Rota de Cadastro (chama a função 'cadastro' do views.py)
    path('cadastro/', views.cadastro, name='cadastro'),

    # Rota de Disciplinas (chama a função 'listar_disciplinas' do views.py)
    path('disciplinas/', views.listar_disciplinas, name='listar_disciplinas'),
]