from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    return render(request, 'core/login.html')

def cadastro_view(request):
    return render(request, 'core/cadastro.html')

def confirmar_identidade_view(request):
    return render(request, 'core/confirmar_identidade.html')

def concluir_cadastro_view(request):
    return render(request, 'core/definir_senha.html')
  
def home(request):
    return HttpResponse("<h1>Home Provisória</h1>")

def cadastro(request):
    return HttpResponse("<h1>Tela de Cadastro</h1>")

def listar_disciplinas(request):
    return HttpResponse("<h1>Lista de Disciplinas</h1>")