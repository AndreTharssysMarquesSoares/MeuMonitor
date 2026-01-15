import pytest
from types import SimpleNamespace
from core.services.mensagem_service import *
from core.exceptions.usuario_exceptions import *
from core.exceptions.mensagem_exceptions import *
from core.services.notificacao_service import *
from datetime import timedelta


def test_criar_topico_admin_senha_incorreta(mocker):
    admin_fake = SimpleNamespace(username="admin")

    mocker.patch(
        "core.services.admin_service.AdminService.getAdmin",
        return_value=admin_fake
    )
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.get_Disciplina",
        return_value=object()
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=False
    )

    with pytest.raises(SenhaIncorretaException):
        MensagemForumService.criarTopicoAdmin(
            username="admin",
            senha="errada",
            titulo="Titulo",
            texto="Texto",
            codigoDisciplina="MAT001"
        )

def test_criar_topico_admin_dados_invalidos(mocker):
    admin_fake = SimpleNamespace(username="admin")

    mocker.patch(
        "core.services.admin_service.AdminService.getAdmin",
        return_value=admin_fake
    )
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.get_Disciplina",
        return_value=object()
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=True
    )

    with pytest.raises(DadosInválidosException):
        MensagemForumService.criarTopicoAdmin(
            username="admin",
            senha="123",
            titulo="",
            texto="Texto",
            codigoDisciplina="MAT001"
        )

def test_criar_topico_admin_sucesso(mocker):
    admin_fake = SimpleNamespace(username="admin")

    aluno1 = SimpleNamespace(matricula="2023001")
    aluno2 = SimpleNamespace(matricula="2023002")

    alunos_interessados = SimpleNamespace(
        all=lambda: [aluno1, aluno2]
    )

    disciplina_fake = SimpleNamespace(
        codigo="MAT001",
        alunos_interessados=alunos_interessados
    )

    monitor1 = SimpleNamespace(matricula="3001")
    monitor2 = SimpleNamespace(matricula="3002")

    topico_fake = SimpleNamespace(id=10)

    mocker.patch(
        "core.services.admin_service.AdminService.getAdmin",
        return_value=admin_fake
    )
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.get_Disciplina",
        return_value=disciplina_fake
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=True
    )
    criar_topico_mock = mocker.patch(
        "core.repositories.mensagem_repository.MensagemForumRepository.criarMensagem",
        return_value=topico_fake
    )
    mocker.patch(
        "core.services.aluno_service.AlunoService.getMonitoresDisciplina",
        return_value=[monitor1, monitor2]
    )
    gerar_notificacao_mock = mocker.patch(
        "core.services.notificacao_service.NotificacaoService.gerarNotificacao"
    )

    result = MensagemForumService.criarTopicoAdmin(
        username="admin",
        senha="123",
        titulo="Titulo",
        texto="Texto",
        codigoDisciplina="MAT001"
    )

    criar_topico_mock.assert_called_once_with(
        titulo="Titulo",
        texto="Texto",
        autor="admin",
        disciplina="MAT001",
        resposta_para=None
    )

    assert gerar_notificacao_mock.call_count == 4

    gerar_notificacao_mock.assert_any_call(
        TipoNotificacao.FORUM,
        "Titulo",
        "Texto",
        "2023001",
        topico_fake.id
    )

    assert result == topico_fake

def test_criar_mensagem_admin_senha_incorreta(mocker):
    admin_fake = SimpleNamespace(username="admin")

    mocker.patch(
        "core.services.admin_service.AdminService.getAdmin",
        return_value=admin_fake
    )
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.get_Disciplina",
        return_value=object()
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=False
    )

    with pytest.raises(SenhaIncorretaException):
        MensagemForumService.criarMensagemAdmin(
            username="admin",
            senha="errada",
            texto="Texto",
            codigoDisciplina="MAT001",
            idMensagemRespondida=1
        )

def test_criar_mensagem_admin_dados_invalidos(mocker):
    admin_fake = SimpleNamespace(username="admin")

    mocker.patch(
        "core.services.admin_service.AdminService.getAdmin",
        return_value=admin_fake
    )
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.get_Disciplina",
        return_value=object()
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=True
    )

    with pytest.raises(DadosInválidosException):
        MensagemForumService.criarMensagemAdmin(
            username="admin",
            senha="123",
            texto="",
            codigoDisciplina="MAT001",
            idMensagemRespondida=1
        )

def test_criar_mensagem_admin_mensagem_pai_nao_encontrada(mocker):
    admin_fake = SimpleNamespace(username="admin")
    disciplina_fake = SimpleNamespace(codigo="MAT001")

    mocker.patch(
        "core.services.admin_service.AdminService.getAdmin",
        return_value=admin_fake
    )
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.get_Disciplina",
        return_value=disciplina_fake
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=True
    )
    mocker.patch(
        "core.repositories.mensagem_repository.MensagemForumRepository.getMensagem",
        return_value=None
    )

    with pytest.raises(MensagemNaoEncontradaException):
        MensagemForumService.criarMensagemAdmin(
            username="admin",
            senha="123",
            texto="Resposta",
            codigoDisciplina="MAT001",
            idMensagemRespondida=99
        )

def test_criar_mensagem_admin_sucesso(mocker):
    admin_fake = SimpleNamespace(username="admin")

    aluno1 = SimpleNamespace(matricula="2023001")
    aluno2 = SimpleNamespace(matricula="2023002")

    alunos_interessados = SimpleNamespace(
        all=lambda: [aluno1, aluno2]
    )

    disciplina_fake = SimpleNamespace(
        codigo="MAT001",
        alunos_interessados=alunos_interessados
    )

    monitor1 = SimpleNamespace(matricula="3001")
    monitor2 = SimpleNamespace(matricula="3002")

    mensagem_pai = SimpleNamespace(id=1)
    mensagem_fake = SimpleNamespace(id=10)

    mocker.patch(
        "core.services.admin_service.AdminService.getAdmin",
        return_value=admin_fake
    )
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.get_Disciplina",
        return_value=disciplina_fake
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=True
    )
    mocker.patch(
        "core.repositories.mensagem_repository.MensagemForumRepository.getMensagem",
        return_value=mensagem_pai
    )
    criar_mensagem_mock = mocker.patch(
        "core.repositories.mensagem_repository.MensagemForumRepository.criarMensagem",
        return_value=mensagem_fake
    )
    mocker.patch(
        "core.services.aluno_service.AlunoService.getMonitoresDisciplina",
        return_value=[monitor1, monitor2]
    )
    gerar_notificacao_mock = mocker.patch(
        "core.services.notificacao_service.NotificacaoService.gerarNotificacao"
    )

    result = MensagemForumService.criarMensagemAdmin(
        username="admin",
        senha="123",
        texto="Resposta",
        codigoDisciplina="MAT001",
        idMensagemRespondida=1
    )

    criar_mensagem_mock.assert_called_once_with(
        titulo=None,
        texto="Resposta",
        autor="admin",
        disciplina="MAT001",
        resposta_para=1
    )

    assert gerar_notificacao_mock.call_count == 4

    gerar_notificacao_mock.assert_any_call(
        TipoNotificacao.FORUM,
        None,
        "Resposta",
        "2023001",
        mensagem_fake.id
    )

    assert result == mensagem_fake

def test_criar_topico_aluno_sucesso(mocker):
    aluno = mocker.Mock(matricula="2023001")
    disciplina = mocker.Mock(codigo="MAT01")
    disciplina.alunos_interessados.all.return_value = [
        mocker.Mock(matricula="2023002"),
        mocker.Mock(matricula="2023003"),
    ]

    topico = mocker.Mock(id=10)

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=aluno
    )
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.get_Disciplina",
        return_value=disciplina
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=True
    )
    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensoesAlunoDisciplina",
        return_value=[]
    )
    criar_msg = mocker.patch(
        "core.services.mensagem_service.MensagemForumRepository.criarMensagem",
        return_value=topico
    )
    gerar_notificacao = mocker.patch(
        "core.services.notificacao_service.NotificacaoService.gerarNotificacao"
    )
    mocker.patch(
        "core.services.aluno_service.AlunoService.getMonitoresDisciplina",
        return_value=[mocker.Mock(matricula="999")]
    )

    resultado = MensagemForumService.criarTopicoAluno(
        matricula="2023001",
        senha="123",
        titulo="Título",
        texto="Texto do tópico",
        codigoDisciplina="MAT01"
    )

    assert resultado == topico
    criar_msg.assert_called_once()
    assert gerar_notificacao.call_count == 3  # 2 interessados + 1 monitor


def test_criar_topico_aluno_senha_incorreta(mocker):
    mocker.patch("core.services.aluno_service.AlunoService.getAluno", return_value=mocker.Mock())
    mocker.patch("core.services.disciplina_service.DisciplinaService.get_Disciplina", return_value=mocker.Mock())
    mocker.patch("core.services.usuario_service.UsuarioService.validarSenha", return_value=False)

    with pytest.raises(SenhaIncorretaException):
        MensagemForumService.criarTopicoAluno(
            matricula="1",
            senha="errada",
            titulo="t",
            texto="x",
            codigoDisciplina="D1"
        )


def test_criar_topico_aluno_dados_invalidos(mocker):
    mocker.patch("core.services.aluno_service.AlunoService.getAluno", return_value=mocker.Mock())
    mocker.patch("core.services.disciplina_service.DisciplinaService.get_Disciplina", return_value=mocker.Mock())
    mocker.patch("core.services.usuario_service.UsuarioService.validarSenha", return_value=True)
    mocker.patch("core.services.suspensao_service.SuspensaoService.getSuspensoesAlunoDisciplina", return_value=[])

    with pytest.raises(DadosInválidosException):
        MensagemForumService.criarTopicoAluno(
            matricula="1",
            senha="123",
            titulo="",
            texto="texto",
            codigoDisciplina="D1"
        )


def test_criar_topico_aluno_suspenso(mocker):
    suspensao = mocker.Mock(data_fim=timezone.now().date() + timedelta(days=1))

    mocker.patch("core.services.aluno_service.AlunoService.getAluno", return_value=mocker.Mock())
    mocker.patch("core.services.disciplina_service.DisciplinaService.get_Disciplina", return_value=mocker.Mock())
    mocker.patch("core.services.usuario_service.UsuarioService.validarSenha", return_value=True)
    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensoesAlunoDisciplina",
        return_value=[suspensao]
    )

    with pytest.raises(AlunoSuspensoNesseForumException):
        MensagemForumService.criarTopicoAluno(
            matricula="1",
            senha="123",
            titulo="t",
            texto="x",
            codigoDisciplina="D1"
        )

def test_criar_mensagem_aluno_sucesso(mocker):
    aluno = mocker.Mock(matricula="2023001")
    disciplina = mocker.Mock(codigo="MAT01")
    disciplina.alunos_interessados.all.return_value = [
        mocker.Mock(matricula="2023002"),
    ]

    mensagem_pai = mocker.Mock(id=1)
    mensagem = mocker.Mock(id=20)

    mocker.patch("core.services.aluno_service.AlunoService.getAluno", return_value=aluno)
    mocker.patch("core.services.disciplina_service.DisciplinaService.get_Disciplina", return_value=disciplina)
    mocker.patch("core.services.usuario_service.UsuarioService.validarSenha", return_value=True)
    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensoesAlunoDisciplina",
        return_value=[]
    )
    mocker.patch(
        "core.services.mensagem_service.MensagemForumRepository.getMensagem",
        return_value=mensagem_pai
    )
    criar_msg = mocker.patch(
        "core.services.mensagem_service.MensagemForumRepository.criarMensagem",
        return_value=mensagem
    )
    gerar_notificacao = mocker.patch(
        "core.services.notificacao_service.NotificacaoService.gerarNotificacao"
    )
    mocker.patch(
        "core.services.aluno_service.AlunoService.getMonitoresDisciplina",
        return_value=[]
    )

    resultado = MensagemForumService.criarMensagemAluno(
        matricula="2023001",
        senha="123",
        texto="Resposta",
        codigoDisciplina="MAT01",
        idMensagemRespondida=1
    )

    assert resultado == mensagem
    criar_msg.assert_called_once()
    gerar_notificacao.assert_called_once()


def test_criar_mensagem_aluno_mensagem_nao_encontrada(mocker):
    mocker.patch("core.services.aluno_service.AlunoService.getAluno", return_value=mocker.Mock())
    mocker.patch("core.services.disciplina_service.DisciplinaService.get_Disciplina", return_value=mocker.Mock())
    mocker.patch("core.services.usuario_service.UsuarioService.validarSenha", return_value=True)
    mocker.patch("core.services.suspensao_service.SuspensaoService.getSuspensoesAlunoDisciplina", return_value=[])
    mocker.patch(
        "core.services.mensagem_service.MensagemForumRepository.getMensagem",
        return_value=None
    )

    with pytest.raises(MensagemNaoEncontradaException):
        MensagemForumService.criarMensagemAluno(
            matricula="1",
            senha="123",
            texto="x",
            codigoDisciplina="D1",
            idMensagemRespondida=99
        )


def test_criar_mensagem_aluno_dados_invalidos(mocker):
    mocker.patch("core.services.aluno_service.AlunoService.getAluno", return_value=mocker.Mock())
    mocker.patch("core.services.disciplina_service.DisciplinaService.get_Disciplina", return_value=mocker.Mock())
    mocker.patch("core.services.usuario_service.UsuarioService.validarSenha", return_value=True)

    with pytest.raises(DadosInválidosException):
        MensagemForumService.criarMensagemAluno(
            matricula="1",
            senha="123",
            texto="",
            codigoDisciplina="D1",
            idMensagemRespondida=1
        )

def test_remover_mensagem_admin_sucesso(mocker):
    admin = mocker.Mock()
    mensagem = mocker.Mock()

    mocker.patch(
        "core.services.admin_service.AdminService.getAdmin",
        return_value=admin
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=True
    )
    mocker.patch(
        "core.services.mensagem_service.MensagemForumService.getMensagem",
        return_value=mensagem
    )

    resultado = MensagemForumService.removerMensagemAdmin(
        username="admin",
        senha="123",
        id=10
    )

    assert resultado is True
    mensagem.delete.assert_called_once()


def test_remover_mensagem_admin_senha_incorreta(mocker):
    admin = mocker.Mock()

    mocker.patch(
        "core.services.admin_service.AdminService.getAdmin",
        return_value=admin
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=False
    )

    with pytest.raises(SenhaIncorretaException):
        MensagemForumService.removerMensagemAdmin(
            username="admin",
            senha="errada",
            id=10
        )

def test_remover_mensagem_aluno_sucesso(mocker):
    aluno = mocker.Mock()
    mensagem = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=aluno
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=True
    )
    mocker.patch(
        "core.services.mensagem_service.MensagemForumService.getMensagem",
        return_value=mensagem
    )

    resultado = MensagemForumService.removerMensagemAluno(
        matricula="2023001",
        senha="123",
        id=5
    )

    assert resultado is True
    mensagem.delete.assert_called_once()


def test_remover_mensagem_aluno_senha_incorreta(mocker):
    aluno = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=aluno
    )
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=False
    )

    with pytest.raises(SenhaIncorretaException):
        MensagemForumService.removerMensagemAluno(
            matricula="2023001",
            senha="errada",
            id=5
        )

def test_criar_topico_web_sucesso(mocker):
    aluno = mocker.Mock()
    disciplina = mocker.Mock()
    topico = mocker.Mock()

    mocker.patch(
        "core.models.Usuario.objects.get",
        return_value=aluno
    )
    mocker.patch(
        "core.models.Disciplina.objects.get",
        return_value=disciplina
    )
    criar_msg = mocker.patch(
        "core.services.mensagem_service.MensagemForumRepository.criarMensagem",
        return_value=topico
    )

    resultado = MensagemForumService.criarTopicoWeb(
        matricula="2023001",
        codigoDisciplina="MAT01",
        titulo="  Título  ",
        texto="  Texto do tópico  "
    )

    assert resultado == topico
    criar_msg.assert_called_once_with(
        autor=aluno,
        disciplina=disciplina,
        titulo="Título",
        texto="Texto do tópico",
        resposta_para=None
    )


def test_criar_topico_web_aluno_nao_encontrado(mocker):
    mocker.patch(
        "core.models.Usuario.objects.get",
        side_effect=Exception("Aluno não encontrado.")
    )

    with pytest.raises(Exception):
        MensagemForumService.criarTopicoWeb(
            matricula="1",
            codigoDisciplina="D1",
            titulo="t",
            texto="x"
        )


def test_criar_topico_web_disciplina_nao_encontrada(mocker):
    mocker.patch(
        "core.models.Usuario.objects.get",
        return_value=mocker.Mock()
    )
    mocker.patch(
        "core.models.Disciplina.objects.get",
        side_effect=Exception("Disciplina não encontrada.")
    )

    with pytest.raises(Exception):
        MensagemForumService.criarTopicoWeb(
            matricula="1",
            codigoDisciplina="D1",
            titulo="t",
            texto="x"
        )


def test_criar_topico_web_titulo_invalido(mocker):
    mocker.patch("core.models.Usuario.objects.get", return_value=mocker.Mock())
    mocker.patch("core.models.Disciplina.objects.get", return_value=mocker.Mock())

    with pytest.raises(Exception):
        MensagemForumService.criarTopicoWeb(
            matricula="1",
            codigoDisciplina="D1",
            titulo="   ",
            texto="texto"
        )


def test_criar_topico_web_texto_invalido(mocker):
    mocker.patch("core.models.Usuario.objects.get", return_value=mocker.Mock())
    mocker.patch("core.models.Disciplina.objects.get", return_value=mocker.Mock())

    with pytest.raises(Exception):
        MensagemForumService.criarTopicoWeb(
            matricula="1",
            codigoDisciplina="D1",
            titulo="titulo",
            texto="   "
        )


def test_responder_topico_web_sucesso(mocker):
    aluno = mocker.Mock()
    mensagem_pai = mocker.Mock()
    mensagem_pai.disciplina = mocker.Mock()
    resposta = mocker.Mock()

    mocker.patch(
        "core.models.Usuario.objects.get",
        return_value=aluno
    )
    mocker.patch(
        "core.models.MensagemForum.objects.get",
        return_value=mensagem_pai
    )
    criar_msg = mocker.patch(
        "core.services.mensagem_service.MensagemForumRepository.criarMensagem",
        return_value=resposta
    )

    resultado = MensagemForumService.responderTopicoWeb(
        matricula="2023001",
        idMensagem=10,
        texto="  Resposta  "
    )

    assert resultado == resposta
    criar_msg.assert_called_once_with(
        autor=aluno,
        disciplina=mensagem_pai.disciplina,
        titulo=None,
        texto="Resposta",
        resposta_para=mensagem_pai
    )


def test_responder_topico_web_aluno_nao_encontrado(mocker):
    mocker.patch(
        "core.models.Usuario.objects.get",
        side_effect=Exception("Aluno não encontrado.")
    )

    with pytest.raises(Exception):
        MensagemForumService.responderTopicoWeb(
            matricula="1",
            idMensagem=10,
            texto="x"
        )


def test_responder_topico_web_topico_nao_encontrado(mocker):
    mocker.patch(
        "core.models.Usuario.objects.get",
        return_value=mocker.Mock()
    )
    mocker.patch(
        "core.models.MensagemForum.objects.get",
        side_effect=Exception("Tópico não encontrado.")
    )

    with pytest.raises(Exception):
        MensagemForumService.responderTopicoWeb(
            matricula="1",
            idMensagem=10,
            texto="x"
        )


def test_responder_topico_web_texto_invalido(mocker):
    mocker.patch(
        "core.models.Usuario.objects.get",
        return_value=mocker.Mock()
    )
    mocker.patch(
        "core.models.MensagemForum.objects.get",
        return_value=mocker.Mock()
    )

    with pytest.raises(Exception):
        MensagemForumService.responderTopicoWeb(
            matricula="1",
            idMensagem=10,
            texto="   "
        )
