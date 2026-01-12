from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db.models import Case, When, IntegerField
from core.services.aluno_service import AlunoService
from django.contrib.auth.decorators import login_required
from core.services.disciplina_service import DisciplinaService
from core.services.aluno_service import AlunoService
from core.repositories.usuario_repository import UsuarioRepository
from core.exceptions.usuario_exceptions import (
    MatriculaInvalidaException, 
    AlunoJaCadastradoException, 
    SenhaFracaException, 
    DadosInvalidoException,
    SenhaIncorretaException, 
    AlunoNaoCadastradoException, 
    AlunoInvalidoException,
    MonitorJaCadastradoException,
    MonitorNaoCadastradoException    
)
from core.services.admin_service import AdminService
from core.exceptions.disciplina_exceptions import DisciplinaJaCadastradaException, CodigoDisciplinaInvalidoException
from core.services.horario_atendimento_service import HorarioAtendimentoService
from core.services.mensagem_service import MensagemForumService
from core.exceptions.mensagem_exceptions import TopicosAindaNaoCadastradosException
from core.exceptions.horario_atendimento_exceptions import HorarioNaoExisteException
    


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


def login_view(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_disciplinas')
        return redirect('dashboard')

    # Consumir logs não exibidos
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    storage.used = True

    if request.method == 'POST':
        usuario_login = request.POST.get('username_login') 
        senha = request.POST.get('senha')
        tipo_usuario = request.POST.get('tipo_usuario')

        try:
            if tipo_usuario == 'admin':
                user = authenticate(request, username=usuario_login, password=senha)
                
                if user is not None:
                    if user.is_staff:
                        login(request, user)
                        return redirect('admin_disciplinas')
                    else:
                         return render(request, 'core/login.html', {
                             'erro': "Este usuário não tem permissão de administrador.",
                             'matricula': usuario_login
                         })
                else:

                    raise SenhaIncorretaException("Usuário ou senha inválidos.")

            else: 
                if AlunoService.validarAcessoAluno(matricula=usuario_login, senha=senha):
                    user_aluno = UsuarioRepository.get_aluno(matricula=usuario_login)
                    
                    if user_aluno and user_aluno.is_active:
                        login(request, user_aluno)
                        return redirect('dashboard')
                    else:
                        return render(request, 'core/login.html', {
                            'erro': "Usuário inativo.",
                            'matricula': usuario_login
                        })

        except (SenhaIncorretaException, AlunoNaoCadastradoException, AlunoInvalidoException) as e:
            return render(request, 'core/login.html', {
                'erro': f"Erro de acesso: {str(e)}",
                'matricula': usuario_login
            })
            
        except Exception as e:
            return render(request, 'core/login.html', {
                'erro': "Erro interno ou credenciais inválidas.",
                'matricula': usuario_login
            })

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login') 
def dashboard(request): 
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


@login_required(login_url='login')
def perfil_view(request):
    aluno = request.user
    erro = None
    sucesso = None
    
    if request.method == 'POST':
        senha_atual = request.POST.get('senha_antiga')
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        novo_email = request.POST.get('email')
        
        # Verificar se a senha atual está correta
        if not aluno.check_password(senha_atual):
            erro = "Senha atual incorreta."
        elif nova_senha != confirmar_senha:
            erro = "As senhas não coincidem."
        elif len(nova_senha) < 8:
            erro = "A nova senha deve ter no mínimo 8 caracteres."
        else:
            try:
                # Atualizar senha
                aluno.set_password(nova_senha)
                
                # Atualizar email se foi alterado
                if novo_email and novo_email != aluno.email:
                    aluno.email = novo_email
                
                aluno.save()
                
                # Re-autenticar o usuário para manter a sessão
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, aluno)
                
                sucesso = "Alterações salvas com sucesso!"
                
            except Exception as e:
                erro = f"Erro ao salvar alterações: {str(e)}"

    context = {
        'aluno': {
            'nome_completo': aluno.get_full_name() or aluno.username,
            'matricula': aluno.username,
            'email': aluno.email or ''
        },
        'aluno_nome': aluno.first_name,
        'sucesso': sucesso,
        'erro': erro
    }
    return render(request, 'core/perfil.html', context)


@login_required(login_url='login')
def disciplinas_view(request):
    aluno_logado = request.user 

    if request.method == 'POST':
        codigo = request.POST.get('disciplina_codigo')
        acao = request.POST.get('acao')

        try:
            if acao == 'remover':
                if aluno_logado.monitor_de and aluno_logado.monitor_de.codigo == codigo:
                     messages.error(request, "Monitores não podem remover interesse da sua própria disciplina.")
                     return redirect('disciplinas')

                AlunoService.removerInteresseWeb(aluno_logado, codigo)
                messages.warning(request, "Disciplina removida.")
            
            elif acao == 'adicionar':
                AlunoService.adicionarInteresseWeb(aluno_logado, codigo)
                messages.success(request, "Disciplina adicionada!")
                
        except Exception as e:
            messages.error(request, f"Erro: {str(e)}")
        
        return redirect('disciplinas')

    todas = DisciplinaService.get_todas_disciplinas()
    meus_interesses = set(aluno_logado.interesses.values_list('codigo', flat=True))

    lista_final = []
    for d in todas:
        tem_monitores = d.monitores.exists()
        sou_monitor_desta = (aluno_logado.monitor_de == d)

        lista_final.append({
            'codigo': d.codigo,
            'nome': d.nome,
            'selecionada': d.codigo in meus_interesses,

            'tem_monitores': tem_monitores,
            'sou_monitor_desta': sou_monitor_desta
        })

    context = {
        'aluno_nome': aluno_logado.first_name,
        'disciplinas': lista_final
    }
    return render(request, 'core/lista_disciplina.html', context)


@login_required(login_url='login')
def meus_interesses_view(request):
    aluno = request.user
    
    interesses = aluno.interesses.all()

    return render(request, 'core/meus_interesses.html', {
        'interesses': interesses,
        'aluno_nome': aluno.first_name
    })

 
@login_required(login_url='login')
def disciplina_view(request, codigo_disciplina):
    """
    Tela de Disciplina: Exibe Horários e Fórum.
    - Monitor da disciplina: Template com controles de edição
    - Aluno comum: Template somente leitura
    """
    aluno = request.user

    # Verificar se a disciplina existe
    try:
        disciplina = DisciplinaService.get_Disciplina(codigo_disciplina)
    except CodigoDisciplinaInvalidoException:
        messages.error(request, "Esta disciplina não existe no sistema.")
        return redirect('meus_interesses')

    eh_monitor_desta = (aluno.monitor_de == disciplina)
    
    # 1. PROCESSAR FORMULÁRIOS (POST)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        try:
            # --- Tópicos do Fórum ---
            if form_type == 'novo_topico':
                MensagemForumService.criarTopicoWeb(
                    matricula=aluno.username,
                    codigoDisciplina=codigo_disciplina,
                    titulo=request.POST.get('titulo'),
                    texto=request.POST.get('texto')
                )
                messages.success(request, "Tópico criado com sucesso!")

            elif form_type == 'responder_topico':
                id_msg = request.POST.get('id_mensagem')
                MensagemForumService.responderTopicoWeb(
                    matricula=aluno.username,
                    idMensagem=id_msg,
                    texto=request.POST.get('texto')
                )
                messages.success(request, "Resposta enviada!")
                
                # Redirecionar mantendo o tópico expandido
                from core.models import MensagemForum
                mensagem = MensagemForum.objects.get(id=id_msg)
                topico_raiz = mensagem
                while topico_raiz.resposta_para is not None:
                    topico_raiz = topico_raiz.resposta_para
                    
                return redirect(f"{request.path}?expandir={topico_raiz.id}")

            # --- Horários (apenas monitor) ---
            elif form_type == 'novo_horario':
                if not eh_monitor_desta:
                    messages.error(request, "Você não é monitor desta disciplina.")
                else:
                    HorarioAtendimentoService.cadastrarHorario(
                        matricula=aluno.username,
                        diaSemana=request.POST.get('dia_semana'),
                        horarioInicio=request.POST.get('hora_inicio'),
                        horarioFim=request.POST.get('hora_fim'),
                        local=request.POST.get('local')
                    )
                    messages.success(request, "Horário cadastrado!")

            elif form_type == 'editar_horario':
                if not eh_monitor_desta:
                    messages.error(request, "Você não é monitor desta disciplina.")
                else:
                    HorarioAtendimentoService.editarHorarioWeb(
                        idHorario=request.POST.get('horario_id'),
                        matriculaMonitor=aluno.username,
                        diaSemana=request.POST.get('dia_semana'),
                        horarioInicio=request.POST.get('hora_inicio'),
                        horarioFim=request.POST.get('hora_fim'),
                        local=request.POST.get('local')
                    )
                    messages.success(request, "Horário atualizado!")

            elif form_type == 'deletar_horario':
                if not eh_monitor_desta:
                    messages.error(request, "Você não é monitor desta disciplina.")
                else:
                    HorarioAtendimentoService.removerHorarioWeb(
                        idHorario=request.POST.get('horario_id'),
                        matriculaMonitor=aluno.username
                    )
                    messages.success(request, "Horário removido!")

        except Exception as e:
            messages.error(request, f"Erro: {str(e)}")
        
        return redirect('disciplina_monitor', codigo_disciplina=codigo_disciplina)

    # 2. CARREGAR DADOS (GET)
    
    # Ordenação de dias da semana
    ordem_dias = Case(
        When(dia_semana='SEG', then=1),
        When(dia_semana='TER', then=2),
        When(dia_semana='QUA', then=3),
        When(dia_semana='QUI', then=4),
        When(dia_semana='SEX', then=5),
        When(dia_semana='SAB', then=6),
        When(dia_semana='DOM', then=7),
        output_field=IntegerField()
    )
    
    # Buscar Horários
    horarios = []
    meus_horarios = []
    horarios_outros = []
    horarios_agrupados = []
    
    try:
        todos_horarios = HorarioAtendimentoService.getHorariosDisciplina(codigo_disciplina)
        horarios = todos_horarios  # Para o calendário
        
        if eh_monitor_desta:
            meus_horarios = todos_horarios.filter(monitor=aluno).annotate(
                ordem_dia=ordem_dias
            ).order_by('ordem_dia', 'hora_inicio')
            
            horarios_outros = todos_horarios.exclude(monitor=aluno).annotate(
                ordem_dia=ordem_dias
            ).order_by('monitor', 'ordem_dia', 'hora_inicio')
        else:
            horarios_agrupados = todos_horarios.annotate(
                ordem_dia=ordem_dias
            ).order_by('monitor', 'ordem_dia', 'hora_inicio')
    except:
        pass  # Mantém listas vazias

    # Buscar Tópicos do Fórum
    topicos_lista = []
    try:
        objs_topicos = MensagemForumService.getTopicosDaDisciplina(codigo_disciplina).order_by('-data_envio')
        
        for t in objs_topicos:
            respostas_aninhadas = MensagemForumService.getRespostasComAninhamento(t.id)
            topicos_lista.append({
                'objeto': t,
                'respostas': respostas_aninhadas,
                'total_respostas': MensagemForumService.contarRespostasTotal(respostas_aninhadas)
            })
    except TopicosAindaNaoCadastradosException:
        pass  # Mantém lista vazia
    except Exception as e:
        print(f"Erro ao buscar tópicos: {e}")

    # 3. RENDERIZAR
    context = {
        'disciplina': disciplina,
        'horarios': horarios,
        'meus_horarios': meus_horarios,
        'horarios_outros': horarios_outros,
        'horarios_agrupados': horarios_agrupados,
        'topicos': topicos_lista,
        'aluno': aluno,
        'eh_monitor_desta': eh_monitor_desta
    }

    template = 'core/disciplina_monitor.html' if eh_monitor_desta else 'core/disciplina.html'
    return render(request, template, context)


# Views para Administradores

@login_required(login_url='login')
def admin_monitores_view(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    monitores_db = AdminService.getTodosMonitoresWeb()
    todas_disciplinas = DisciplinaService.get_todas_disciplinas()
    
    aluno_verificado = None
    mostrar_modal_add = False 
    matricula_input = ""
    erro_modal = None 

    if request.method == 'POST':
        acao = request.POST.get('acao')
        
        if acao == 'verificar_aluno':
            matricula_input = request.POST.get('matricula')
            mostrar_modal_add = True
            
            try:
                aluno_verificado = AlunoService.getAluno(matricula=matricula_input)

                if aluno_verificado.monitor_de:
                    disc_nome = aluno_verificado.monitor_de.nome
                    erro_modal = f"Este aluno já está cadastrado como monitor de '{disc_nome}'."
                    aluno_verificado = None 
                    
            except AlunoNaoCadastradoException:
                erro_modal = f"A matrícula '{matricula_input}' não foi encontrada na base de usuários."
                aluno_verificado = None 
            except Exception:
                erro_modal = "Erro inesperado ao buscar aluno."

        elif acao == 'adicionar_confirmado':
            matricula = request.POST.get('matricula')
            codigo_disciplina = request.POST.get('codigo_disciplina')
            
            try:
                AdminService.criarMonitorWeb(matricula, codigo_disciplina)
                messages.success(request, "Monitor adicionado com sucesso!")
                return redirect('admin_monitores')
            except Exception as e:
                messages.error(request, f"Erro ao salvar: {str(e)}")
                mostrar_modal_add = False

        elif acao == 'desassociar':
            matricula_confirmacao = request.POST.get('matricula_confirmacao')
            try:
                AdminService.removerMonitorWeb(matricula_confirmacao)
                messages.success(request, "Monitor removido com sucesso.")
            except Exception as e:
                messages.error(request, f"Erro: {str(e)}")
            return redirect('admin_monitores')

    lista_monitores = []
    for m in monitores_db:
        nome_disc = m.monitor_de.nome if m.monitor_de else "-"
        cod_disc = m.monitor_de.codigo if m.monitor_de else "-"
        lista_monitores.append({
            'nome': m.first_name or m.username,
            'matricula': m.username,
            'disciplina_nome': nome_disc,
            'disciplina_cod': cod_disc
        })

    context = {
        'monitores': lista_monitores,
        'disciplinas': todas_disciplinas,
        'admin_nome': request.user.first_name,
        'aluno_verificado': aluno_verificado,
        'mostrar_modal_add': mostrar_modal_add,
        'matricula_preenchida': matricula_input,
        'erro_modal': erro_modal
    }

    return render(request, 'core/monitores_admin.html', context)
 
@login_required(login_url='login')
def admin_disciplinas_view(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    
    
    confirmacao_dados = None 
    erro_modal_disciplina = None   
    mostrar_modal_cadastro = False
    codigo_pesquisado = ""

    if request.method == 'POST':
        acao = request.POST.get('acao') 
        
        try:
            if acao == 'deletar':
                codigo = request.POST.get('codigo')
                AdminService.deletarDisciplinaWeb(codigo)
                messages.success(request, "Disciplina removida com sucesso!")
                return redirect('admin_disciplinas')

            elif acao == 'buscar':
                codigo = request.POST.get('codigo')
                codigo_pesquisado = codigo
                mostrar_modal_cadastro = True

                if DisciplinaService.exist_Disciplina(codigo):
                    raise DisciplinaJaCadastradaException()
 
                disc_valida = AdminService.buscarDisciplinaValida(codigo)

                if not disc_valida:
                    raise CodigoDisciplinaInvalidoException("Disciplina não encontrada ou retorno nulo.")

                confirmacao_dados = {
                    'codigo': disc_valida.codigo,
                    'nome': disc_valida.nome
                }
                mostrar_modal_cadastro = False

            elif acao == 'criar': 
                codigo = request.POST.get('codigo')
                if codigo:
                    nova_disc = AdminService.criarDisciplinaWeb(codigo=codigo)
                    messages.success(request, f"Disciplina '{nova_disc.nome}' adicionada com sucesso!")
                    return redirect('admin_disciplinas')

        except DisciplinaJaCadastradaException:
            erro_modal_disciplina = "Esta disciplina já está cadastrada no sistema."
        except CodigoDisciplinaInvalidoException:
            erro_modal_disciplina = "Código inválido ou não encontrado na base oficial."
        except Exception as e:
            erro_modal_disciplina = f"Erro ao buscar: {str(e)}"

    try:
        todas_disciplinas = DisciplinaService.get_todas_disciplinas()
    except:
        todas_disciplinas = []

    lista_formatada = []
    for d in todas_disciplinas:
        lista_formatada.append({
            'codigo': d.codigo,
            'nome': d.nome,
            'curso': 'Geral', 
            'monitores_count': d.monitores.count() 
        })

    context = {
        'admin_nome': request.user.first_name or "Administrador",
        'disciplinas': lista_formatada,
        'confirmacao': confirmacao_dados,
    
        'erro_modal_disciplina': erro_modal_disciplina,
        'mostrar_modal_cadastro': mostrar_modal_cadastro,
        'codigo_pesquisado': codigo_pesquisado
    }
    return render(request, 'core/disciplinas_admin.html', context)