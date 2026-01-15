import pytest
from types import SimpleNamespace

from core.services.notificacao_service import *
from core.exceptions.notificacao_exceptions import *

def test_gerar_notificacao_tipo_invalido():
    with pytest.raises(TipoNotificaoInvalidaException):
        NotificacaoService.gerarNotificacao(
            tipo="ADMIN",
            titulo="Aviso",
            texto="Texto",
            destinatario="2023001"
        )


def test_gerar_notificacao_forum_sem_mensagem():
    with pytest.raises(NotificacaoInvalidaException):
        NotificacaoService.gerarNotificacao(
            tipo=TipoNotificacao.FORUM,
            titulo="Forum",
            texto="Mensagem",
            destinatario="2023001",
            mensagem_forum=None
        )


def test_gerar_notificacao_nao_forum_com_mensagem():
    with pytest.raises(NotificacaoInvalidaException):
        NotificacaoService.gerarNotificacao(
            tipo=TipoNotificacao.ADMIN,
            titulo="Aviso",
            texto="Texto",
            destinatario="2023001",
            mensagem_forum="Mensagem indevida"
        )


def test_gerar_notificacao_titulo_ou_texto_invalidos():
    with pytest.raises(NotificacaoInvalidaException):
        NotificacaoService.gerarNotificacao(
            tipo=TipoNotificacao.ADMIN,
            titulo="",
            texto="",
            destinatario="2023001"
        )


def test_gerar_notificacao_admin_sucesso(mocker):
    notif_fake = SimpleNamespace(id=1)

    notificar_mock = mocker.patch(
        "core.services.notificacao_service.NotificacaoRepository.notificar",
        return_value=notif_fake
    )

    result = NotificacaoService.gerarNotificacao(
        tipo=TipoNotificacao.ADMIN,
        titulo="Aviso",
        texto="Texto",
        destinatario="2023001"
    )

    notificar_mock.assert_called_once_with(
        tipo=TipoNotificacao.ADMIN,
        titulo="Aviso",
        texto="Texto",
        destinatario="2023001",
        mensagem_forum=None
    )

    assert result == notif_fake


def test_gerar_notificacao_sistema_sucesso(mocker):
    mocker.patch(
        "core.services.notificacao_service.NotificacaoRepository.notificar",
        return_value=object()
    )

    NotificacaoService.gerarNotificacao(
        tipo=TipoNotificacao.SISTEMA,
        titulo="Sistema",
        texto="Mensagem",
        destinatario="2023001"
    )


def test_gerar_notificacao_forum_sucesso(mocker):
    msg_forum = object()

    notificar_mock = mocker.patch(
        "core.services.notificacao_service.NotificacaoRepository.notificar",
        return_value=object()
    )

    NotificacaoService.gerarNotificacao(
        tipo=TipoNotificacao.FORUM,
        titulo="Forum",
        texto="Mensagem",
        destinatario="2023001",
        mensagem_forum=msg_forum
    )

    notificar_mock.assert_called_once()
    
def test_marcar_lida_notificacao_nao_existe(mocker):
    mocker.patch(
        "core.services.notificacao_service.NotificacaoService.getNotificacao",
        return_value=None
    )

    with pytest.raises(NotificaoNaoExisteException):
        NotificacaoService.marcarLida(1)


def test_marcar_lida_sucesso(mocker):
    notificacao_fake = SimpleNamespace(lida=False)

    get_mock = mocker.patch(
        "core.services.notificacao_service.NotificacaoService.getNotificacao",
        return_value=notificacao_fake
    )

    salvar_mock = mocker.patch(
        "core.services.notificacao_service.NotificacaoRepository.salvar"
    )

    result = NotificacaoService.marcarLida(1)

    get_mock.assert_called_once_with(1)
    assert notificacao_fake.lida is True
    salvar_mock.assert_called_once_with(notificacao_fake)
    assert result is True
