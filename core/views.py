from django.shortcuts import render


def login_view(request):
    return render(request, 'core/login.html')


def cadastro_view(request):
    return render(request, 'core/cadastro.html')
