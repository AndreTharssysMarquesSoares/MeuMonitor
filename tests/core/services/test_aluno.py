import pytest
from core.services.aluno_service import AlunoService
from core.exceptions.usuario_exceptions import MatriculaInvalidaException, AlunoNaoCadastradoException, SenhaFracaException, AlunoJaCadastradoException, DadosInvalidoException, SenhaIncorretaException, AlunoInvalidoException, AlunoJaInteressadoException, AlunoNaoInteressadoException

def test_cadastrar_aluno_matricula_invalida(mocker):
    mocker.patch(
        "core.services.aluno_service.AlunoService.getAlunoValido",
        return_value=None
    )

    with pytest.raises(MatriculaInvalidaException):
        AlunoService.cadastrarAluno(
            matricula="2023001",
            senha="Senha@123",
            email="teste@email.com"
        )
        
def test_cadastrar_aluno_ja_cadastrado(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.nome_completo = "Joao Silva"

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAlunoValido",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.exist_aluno",
        return_value=True
    )

    with pytest.raises(AlunoJaCadastradoException):
        AlunoService.cadastrarAluno(
            matricula="2023001",
            senha="Senha@123",
            email="teste@email.com"
        )
        
def test_cadastrar_aluno_senha_fraca(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.nome_completo = "Joao Silva"

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAlunoValido",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.exist_aluno",
        return_value=False
    )

    with pytest.raises(SenhaFracaException):
        AlunoService.cadastrarAluno(
            matricula="2023001",
            senha="fraca",
            email="teste@email.com"
        )
        
def test_cadastrar_aluno_email_invalido(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.nome_completo = "Joao Silva"

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAlunoValido",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.exist_aluno",
        return_value=False
    )

    with pytest.raises(DadosInvalidoException):
        AlunoService.cadastrarAluno(
            matricula="2023001",
            senha="Senha@123",
            email=""
        )
        
def test_cadastrar_aluno_com_sucesso(mocker):
    aluno_valido_mock = mocker.Mock()
    aluno_valido_mock.nome_completo = "Joao Silva"

    user_mock = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAlunoValido",
        return_value=aluno_valido_mock
    )

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.exist_aluno",
        return_value=False
    )

    criar_mock = mocker.patch(
        "core.services.aluno_service.UsuarioRepository.criar_usuario",
        return_value=user_mock
    )

    user = AlunoService.cadastrarAluno(
        matricula="2023001",
        senha="Senha@123",
        email="teste@email.com"
    )

    assert user == user_mock
    criar_mock.assert_called_once()
    
def test_alterar_aluno_nao_cadastrado(mocker):
    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=None
    )

    with pytest.raises(AlunoNaoCadastradoException):
        AlunoService.alterarAluno("2023001", "Senha@123")
        
def test_alterar_aluno_senha_incorreta(mocker):
    aluno_mock = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.UsuarioService.validarSenha",
        return_value=False
    )

    with pytest.raises(SenhaIncorretaException):
        AlunoService.alterarAluno("2023001", "errada")
        
def test_alterar_aluno_email_vazio(mocker):
    aluno_mock = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.UsuarioService.validarSenha",
        return_value=True
    )

    with pytest.raises(DadosInvalidoException):
        AlunoService.alterarAluno(
            "2023001",
            "Senha@123",
            email=""
        )
        
def test_alterar_aluno_nova_senha_fraca(mocker):
    aluno_mock = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.UsuarioService.validarSenha",
        return_value=True
    )

    with pytest.raises(SenhaFracaException):
        AlunoService.alterarAluno(
            "2023001",
            "Senha@123",
            nova_senha="fraca"
        )
        
def test_alterar_aluno_alterar_email(mocker):
    aluno_mock = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.UsuarioService.validarSenha",
        return_value=True
    )

    salvar_mock = mocker.patch(
        "core.services.aluno_service.UsuarioRepository.salvar"
    )

    aluno = AlunoService.alterarAluno(
        "2023001",
        "Senha@123",
        email="novo@email.com"
    )

    assert aluno.email == "novo@email.com"
    salvar_mock.assert_called_once_with(aluno)
    
def test_alterar_aluno_alterar_senha(mocker):
    aluno_mock = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.UsuarioService.validarSenha",
        return_value=True
    )

    salvar_mock = mocker.patch(
        "core.services.aluno_service.UsuarioRepository.salvar"
    )

    aluno = AlunoService.alterarAluno(
        "2023001",
        "Senha@123",
        nova_senha="NovaSenha@123"
    )

    aluno.set_password.assert_called_once_with("NovaSenha@123")
    salvar_mock.assert_called_once_with(aluno)

def test_alterar_aluno_email_e_senha(mocker):
    aluno_mock = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.UsuarioService.validarSenha",
        return_value=True
    )

    salvar_mock = mocker.patch(
        "core.services.aluno_service.UsuarioRepository.salvar"
    )

    aluno = AlunoService.alterarAluno(
        "2023001",
        "Senha@123",
        email="novo@email.com",
        nova_senha="NovaSenha@123"
    )

    assert aluno.email == "novo@email.com"
    aluno.set_password.assert_called_once_with("NovaSenha@123")
    salvar_mock.assert_called_once_with(aluno)

def test_add_interesse_aluno_invalido(mocker):
    mocker.patch(
        "core.services.aluno_service.AlunoService.validarAcessoAluno",
        return_value=False
    )

    with pytest.raises(AlunoInvalidoException):
        AlunoService.addInteresseDisciplina("2023001", "senha", "MAT001")
        
def test_add_interesse_aluno_ja_interessado(mocker):
    aluno_mock = mocker.Mock()
    disciplina_mock = mocker.Mock()
    disciplina_mock.codigo = "MAT001"

    interesses_mock = mocker.Mock()
    interesses_mock.filter.return_value.exist.return_value = True
    aluno_mock.interesses = interesses_mock

    mocker.patch(
        "core.services.aluno_service.AlunoService.validarAcessoAluno",
        return_value=True
    )

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.DisciplinaService.get_Disciplina",
        return_value=disciplina_mock
    )

    with pytest.raises(AlunoJaInteressadoException):
        AlunoService.addInteresseDisciplina("2023001", "senha", "MAT001")
        
def test_add_interesse_com_sucesso(mocker):
    aluno_mock = mocker.Mock()
    disciplina_mock = mocker.Mock()
    disciplina_mock.codigo = "MAT001"

    interesses_mock = mocker.Mock()
    interesses_mock.filter.return_value.exist.return_value = False
    aluno_mock.interesses = interesses_mock

    mocker.patch(
        "core.services.aluno_service.AlunoService.validarAcessoAluno",
        return_value=True
    )

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.DisciplinaService.get_Disciplina",
        return_value=disciplina_mock
    )

    AlunoService.addInteresseDisciplina("2023001", "senha", "MAT001")

    aluno_mock.interesses.add.assert_called_once_with(disciplina_mock)
    
def test_remove_interesse_aluno_invalido(mocker):
    mocker.patch(
        "core.services.aluno_service.AlunoService.validarAcessoAluno",
        return_value=False
    )

    with pytest.raises(AlunoInvalidoException):
        AlunoService.removeInteresseDisciplina("2023001", "senha", "MAT001")
        
def test_remove_interesse_aluno_nao_interessado(mocker):
    aluno_mock = mocker.Mock()
    disciplina_mock = mocker.Mock()
    disciplina_mock.codigo = "MAT001"

    interesses_mock = mocker.Mock()
    interesses_mock.filter.return_value.exist.return_value = False
    aluno_mock.interesses = interesses_mock

    mocker.patch(
        "core.services.aluno_service.AlunoService.validarAcessoAluno",
        return_value=True
    )

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.DisciplinaService.get_Disciplina",
        return_value=disciplina_mock
    )

    with pytest.raises(AlunoNaoInteressadoException):
        AlunoService.removeInteresseDisciplina("2023001", "senha", "MAT001")
        
def test_remove_interesse_com_sucesso(mocker):
    aluno_mock = mocker.Mock()
    disciplina_mock = mocker.Mock()
    disciplina_mock.codigo = "MAT001"

    interesses_mock = mocker.Mock()
    interesses_mock.filter.return_value.exist.return_value = True
    aluno_mock.interesses = interesses_mock

    mocker.patch(
        "core.services.aluno_service.AlunoService.validarAcessoAluno",
        return_value=True
    )

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.aluno_service.DisciplinaService.get_Disciplina",
        return_value=disciplina_mock
    )

    AlunoService.removeInteresseDisciplina("2023001", "senha", "MAT001")

    aluno_mock.interesses.remove.assert_called_once_with(disciplina_mock)
    
def test_get_interesse_aluno_invalido(mocker):
    mocker.patch(
        "core.services.aluno_service.AlunoService.validarAcessoAluno",
        return_value=False
    )

    with pytest.raises(AlunoInvalidoException):
        AlunoService.getInteresseAluno("2023001", "senha")
        
def test_get_interesse_aluno_sucesso(mocker):
    aluno_mock = mocker.Mock()

    interesses_mock = mocker.Mock()
    interesses_mock.all.return_value = ["MAT001", "MAT002"]
    aluno_mock.interesses = interesses_mock

    mocker.patch(
        "core.services.aluno_service.AlunoService.validarAcessoAluno",
        return_value=True
    )

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    result = AlunoService.getInteresseAluno("2023001", "senha")

    assert result == ["MAT001", "MAT002"]
    interesses_mock.all.assert_called_once()
    
def test_get_monitores_disciplina(mocker):
    mock_retorno = ["monitor1", "monitor2"]

    mock_get = mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_monitores_disciplina",
        return_value=mock_retorno
    )

    result = AlunoService.getMonitoresDisciplina("MAT001")

    assert result == mock_retorno
    mock_get.assert_called_once_with(disciplina="MAT001")
    
def test_get_aluno_valido_matricula_invalida(mocker):
    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno_valido",
        return_value=None
    )

    with pytest.raises(MatriculaInvalidaException):
        AlunoService.getAlunoValido("000000")
        
def test_get_aluno_valido_sucesso(mocker):
    aluno_mock = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno_valido",
        return_value=aluno_mock
    )

    result = AlunoService.getAlunoValido("2023001")

    assert result == aluno_mock
    
def test_get_aluno_nao_cadastrado(mocker):
    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=None
    )

    with pytest.raises(AlunoNaoCadastradoException):
        AlunoService.getAluno("2023001")
        
def test_get_aluno_sucesso(mocker):
    aluno_mock = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=aluno_mock
    )

    result = AlunoService.getAluno("2023001")

    assert result == aluno_mock
    
def test_validar_acesso_aluno_nao_cadastrado(mocker):
    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=None
    )

    with pytest.raises(AlunoNaoCadastradoException):
        AlunoService.validarAcessoAluno("2023001", "senha123")
    
def test_validar_acesso_aluno_senha_incorreta(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.check_password.return_value = False

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=aluno_mock
    )

    with pytest.raises(SenhaIncorretaException):
        AlunoService.validarAcessoAluno("2023001", "senha_errada")
        
def test_validar_acesso_aluno_sucesso(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.check_password.return_value = True

    mocker.patch(
        "core.services.aluno_service.UsuarioRepository.get_aluno",
        return_value=aluno_mock
    )

    result = AlunoService.validarAcessoAluno("2023001", "senha_correta")

    assert result is True
    aluno_mock.check_password.assert_called_once_with("senha_correta")
