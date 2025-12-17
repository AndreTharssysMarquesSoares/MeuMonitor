from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from core.services.aluno_service import AlunoService
from django.contrib.auth.decorators import login_required
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
        return redirect('dashboard')

    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')

        try:
            if AlunoService.validarAcessoAluno(matricula=matricula, senha=senha):
                user = UsuarioRepository.get_aluno(matricula=matricula)
                
                if user and user.is_active:
                    login(request, user)
                    return redirect('dashboard')
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

@login_required(login_url='login') 
def dashboard(request):
    # Dados Fakes (Mocados) para a Sprint 1 
    mock_horarios = [
        {
            'disciplina': 'Cálculo Numérico',
            'dia': 'Segunda-feira',
            'hora': '14:00 - 16:00',
            'monitor': 'Ana Silva',
            'sala': 'B-102'
        },
        {
            'disciplina': 'Algoritmos e Estrutura de Dados',
            'dia': 'Quarta-feira',
            'hora': '10:00 - 12:00',
            'monitor': 'Carlos Eduardo',
            'sala': 'Lab 3'
        },
        {
            'disciplina': 'Circuitos Digitais',
            'dia': 'Sexta-feira',
            'hora': '08:00 - 10:00',
            'monitor': 'Beatriz Lima',
            'sala': 'Sala 204'
        }
    ]

    mock_topicos = [
        {
            'titulo': 'Como resolver o erro de segmentação no Lab 2?',
            'disciplina_cod': 'AED-2025',
            'autor': 'João Santos',
            'respostas': 3,
            'data': '17 Dez'
        },
        {
            'titulo': 'Dúvida sobre Transformada de Laplace',
            'disciplina_cod': 'CALC-NUM',
            'autor': 'Maria Oliveira',
            'respostas': 0,
            'data': '16 Dez'
        },
        {
            'titulo': 'Data da prova final alterada?',
            'disciplina_cod': 'CIRC-DIG',
            'autor': 'Pedro Alencar',
            'respostas': 12,
            'data': '15 Dez'
        }
    ]

    context = {
        'aluno_nome': request.user.first_name if request.user.is_authenticated else 'Aluno Visitante',
        'horarios': mock_horarios,
        'topicos': mock_topicos,
    }
    return render(request, 'core/dashboard.html', context)

def disciplinas(request):
    # Retorna apenas texto, sem buscar template, para não dar erro
    return HttpResponse("<h1>Disciplinas (Aguardando Merge da Branch de Front-end)</h1>")

def logout_view(request):
    logout(request)
    return redirect('login')