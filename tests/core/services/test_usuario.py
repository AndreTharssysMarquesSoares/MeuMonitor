import pytest
from core.services.usuario_service import UsuarioService
from core.exceptions.usuario_exceptions import UsuarioNaoExisteException, SenhaIncorretaException, SenhaFracaException

def test_alterar_senha_usuario_nao_existe(mocker):
    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_usuario",
        return_value=None
    )

    with pytest.raises(UsuarioNaoExisteException):
        UsuarioService.alterarSenha(1, "senha123", "NovaSenha@123")

def test_alterar_senha_senha_atual_incorreta(mocker):
    user_mock = mocker.Mock()
    user_mock.check_password.return_value = False

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_usuario",
        return_value=user_mock
    )

    with pytest.raises(SenhaIncorretaException):
        UsuarioService.alterarSenha(1, "errada", "NovaSenha@123")

def test_alterar_senha_senha_fraca(mocker):
    user_mock = mocker.Mock()
    user_mock.check_password.return_value = True

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_usuario",
        return_value=user_mock
    )

    with pytest.raises(SenhaFracaException):
        UsuarioService.alterarSenha(1, "SenhaAtual@123", "fraca")

def test_alterar_senha_sucesso(mocker):
    user_mock = mocker.Mock()
    user_mock.check_password.return_value = True

    salvar_mock = mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.salvar"
    )

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_usuario",
        return_value=user_mock
    )

    result = UsuarioService.alterarSenha(
        1,
        "SenhaAtual@123",
        "NovaSenha@123"
    )

    user_mock.set_password.assert_called_once_with("NovaSenha@123")
    salvar_mock.assert_called_once()
    assert result == user_mock

@pytest.mark.parametrize("senha", [
    "abc",                # muito curta
    "abcdefgh",           # sem maiúscula, número, especial
    "Abcdefgh",           # sem número e especial
    "Abcdefg1",           # sem especial
    "abcdefg1@",          # sem maiúscula
])

def test_auth_password_validators_invalidas(senha):
    assert not UsuarioService.auth_password_validators(senha)

def test_auth_password_validators_valida():
    assert UsuarioService.auth_password_validators("SenhaForte@123")
    
def test_username_valido():
    assert UsuarioService.username_valido("andre123")

def test_username_invalido_vazio():
    assert not UsuarioService.username_valido("")

def test_username_invalido_com_espaco():
    assert not UsuarioService.username_valido("andre soares")

def test_username_invalido_none():
    assert not UsuarioService.username_valido(None)