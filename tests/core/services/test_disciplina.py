import pytest
from core.services.disciplina_service import DisciplinaService
from core.exceptions.disciplina_exceptions import DisciplinaJaCadastradaException, CodigoDisciplinaInvalidoException

def test_cadastrar_disciplina_ja_cadastrada(mocker):
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.exist_Disciplina",
        return_value=True
    )

    with pytest.raises(DisciplinaJaCadastradaException):
        DisciplinaService.cadastrarDisciplina("INF101")

def test_cadastrar_disciplina_codigo_invalido(mocker):
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.exist_Disciplina",
        return_value=False
    )

    mocker.patch(
        "core.services.disciplina_service.DisciplinaRepository.get_disciplinaValida",
        return_value=None
    )

    with pytest.raises(CodigoDisciplinaInvalidoException):
        DisciplinaService.cadastrarDisciplina("XXX999")
        
def test_cadastrar_disciplina_sucesso(mocker):
    disciplina_valida_mock = mocker.Mock()
    disciplina_valida_mock.nome = "Introdução à Programação"

    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.exist_Disciplina",
        return_value=False
    )

    mocker.patch(
        "core.services.disciplina_service.DisciplinaRepository.get_disciplinaValida",
        return_value=disciplina_valida_mock
    )

    disciplina_criada_mock = mocker.Mock()

    criar_mock = mocker.patch(
        "core.services.disciplina_service.DisciplinaRepository.criar_disciplina",
        return_value=disciplina_criada_mock
    )

    result = DisciplinaService.cadastrarDisciplina("INF101")

    assert result == disciplina_criada_mock
    criar_mock.assert_called_once_with(
        codigo="INF101",
        nome="Introdução à Programação"
    )
    
def test_exist_disciplina_true(mocker):
    mocker.patch(
        "core.services.disciplina_service.DisciplinaRepository.exist_disciplina",
        return_value=True
    )

    assert DisciplinaService.exist_Disciplina("INF101") is True
    
def test_exist_disciplina_false(mocker):
    mocker.patch(
        "core.services.disciplina_service.DisciplinaRepository.exist_disciplina",
        return_value=False
    )

    assert DisciplinaService.exist_Disciplina("INF101") is False

def test_exist_disciplina_valida(mocker):
    mocker.patch(
        "core.services.disciplina_service.DisciplinaRepository.exist_disciplinaValida",
        return_value=True
    )

    assert DisciplinaService.exist_DisciplinaValida("INF101") is True

def test_get_disciplina_invalida(mocker):
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.exist_Disciplina",
        return_value=False
    )

    with pytest.raises(CodigoDisciplinaInvalidoException):
        DisciplinaService.get_Disciplina("INF404")
        
def test_get_disciplina_sucesso(mocker):
    disciplina_mock = mocker.Mock()

    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.exist_Disciplina",
        return_value=True
    )

    mocker.patch(
        "core.services.disciplina_service.DisciplinaRepository.get_disciplina",
        return_value=disciplina_mock
    )

    result = DisciplinaService.get_Disciplina("INF101")

    assert result == disciplina_mock
    
def test_get_disciplina_valida_invalida(mocker):
    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.exist_DisciplinaValida",
        return_value=False
    )

    with pytest.raises(CodigoDisciplinaInvalidoException):
        DisciplinaService.get_disciplinaValida("XXX999")
        
def test_get_disciplina_valida_sucesso(mocker):
    disciplina_valida_mock = mocker.Mock()

    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.exist_DisciplinaValida",
        return_value=True
    )

    mocker.patch(
        "core.services.disciplina_service.DisciplinaRepository.get_disciplinaValida",
        return_value=disciplina_valida_mock
    )

    result = DisciplinaService.get_disciplinaValida("INF101")

    assert result == disciplina_valida_mock
    
def test_get_alunos_interessados(mocker):
    alunos_mock = mocker.Mock()
    alunos_mock.all.return_value = ["aluno1", "aluno2"]

    disciplina_mock = mocker.Mock()
    disciplina_mock.alunos_interessados = alunos_mock

    mocker.patch(
        "core.services.disciplina_service.DisciplinaService.get_Disciplina",
        return_value=disciplina_mock
    )

    result = DisciplinaService.get_alunosInteressados("INF101")

    assert result == ["aluno1", "aluno2"]
    
