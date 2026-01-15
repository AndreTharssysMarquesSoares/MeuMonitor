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
    path('disciplina/<str:codigo_disciplina>/', views.disciplina_view, name='disciplina'),
    path('notificacoes/', views.notificacoes_view, name='notificacoes'),
    path('notificacoes/marcar-lida/<int:notificacao_id>/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),
    path('notificacoes/marcar-todas-lidas/', views.marcar_todas_notificacoes_lidas, name='marcar_todas_lidas'),

    path('gerenciar/monitores/', views.admin_monitores_view, name='admin_monitores'),
    path('gerenciar/disciplinas/', views.admin_disciplinas_view, name='admin_disciplinas'),
    path('moderacao/', views.admin_moderacao_view, name='admin_moderacao'),
    path('moderacao/<str:codigo_disciplina>/', views.admin_moderacao_forum_view, name='admin_moderacao_forum'),
] 