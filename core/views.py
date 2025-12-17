from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from core.services.aluno_service import AlunoService
from core.repositories.usuario_repository import UsuarioRepository
from core.exceptions.usuario_exceptions import (
    MatriculaInvalidaException, 
    AlunoJaCadastradoException, 
    SenhaFracaException, 
    DadosInvalidoException,
    SenhaIncorretaException, 
    AlunoNaoCadastradoException, 
    AlunoInvalidoException
)

def cadastro_view(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        
        try:
            aluno_valido = AlunoService.getAlunoValido(matricula)
            
            if UsuarioRepository.exist_aluno(matricula):
                raise AlunoJaCadastradoException()

            return render(request, 'core/confirmar_identidade.html', {
                'matricula': matricula,
                'nome': aluno_valido.nome_completo
            })

        except (MatriculaInvalidaException, AlunoJaCadastradoException) as e:
            return render(request, 'core/cadastro.html', {'erro_geral': str(e)})

    return render(request, 'core/cadastro.html')

def definir_senha_view(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        return render(request, 'core/definir_senha.html', {'matricula': matricula})

    return redirect('cadastro')

def concluir_cadastro_view(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        try:
            AlunoService.cadastrarAluno(
                matricula=matricula,
                email=email,
                senha=senha
            )
            messages.success(request, "Cadastro concluído com sucesso! Faça login.")
            return redirect('login')

        except (SenhaFracaException, DadosInvalidoException) as e:
            return render(request, 'core/definir_senha.html', {
                'matricula': matricula,
                'erro_geral': str(e)
            })
            
    return redirect('cadastro')

def home(request):
    # Retorna apenas texto, sem buscar template, para não dar erro
    return HttpResponse("<h1>Página Inicial (Aguardando Merge da Branch de Front-end)</h1>")

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')

        if not matricula or len(matricula) != 9 or not matricula.isdigit():
            return render(request, 'core/login.html', {
                'erro': "Formato inválido: A matrícula deve conter exatamente 9 números.",
                'matricula': matricula
            })

        try:
            if AlunoService.validarAcessoAluno(matricula=matricula, senha=senha):
                user = UsuarioRepository.get_aluno(matricula=matricula)
                
                if user and user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'core/login.html', {
                        'erro': "Usuário inativo.",
                        'matricula': matricula
                    })

        except (SenhaIncorretaException, AlunoNaoCadastradoException, AlunoInvalidoException) as e:
            return render(request, 'core/login.html', {
                'erro': f"Erro de acesso: {str(e)}",
                'matricula': matricula
            })
            
        except Exception as e:
            return render(request, 'core/login.html', {
                'erro': "Erro interno.",
                'matricula': matricula
            })

    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')