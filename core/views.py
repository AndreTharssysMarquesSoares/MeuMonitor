from django.shortcuts import render


def login_view(request):
    return render(request, 'core/login.html')


def cadastro_view(request):
    return render(request, 'core/cadastro.html')


def confirmar_identidade_view(request):
    return render(request, 'core/confirmar_identidade.html')


def concluir_cadastro_view(request):
    return render(request, 'core/definir_senha.html')
