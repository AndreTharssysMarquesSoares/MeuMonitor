from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Home Provisória</h1>")

def cadastro(request):
    return HttpResponse("<h1>Tela de Cadastro</h1>")

def listar_disciplinas(request):
    return HttpResponse("<h1>Lista de Disciplinas</h1>")