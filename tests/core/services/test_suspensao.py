import pytest
from datetime import date, timedelta
from types import SimpleNamespace

from django.utils import timezone

from core.services.suspensao_service import SuspensaoService
from core.exceptions.suspensao_exceptions import *

def test_criar_suspensao_sucesso(mocker):
    hoje = timezone.now().date()

    aluno_fake = object()
    disciplina_fake = object()

    # Nenhuma suspensão ativa
    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensoesAlunoDisciplina",
        return_value=[]
    )

    repo_mock = mocker.patch(
        "core.services.suspensao_service.SuspensaoRepository.criarSuspensao",
        return_value="SUSPENSAO_CRIADA"
    )

    resultado = SuspensaoService.criarSuspensao(
        dataFim=hoje + timedelta(days=5),
        motivo="Indisciplina",
        aluno=aluno_fake,
        disciplina=disciplina_fake
    )

    assert resultado == "SUSPENSAO_CRIADA"
    repo_mock.assert_called_once_with(
        aluno=aluno_fake,
        disciplina=disciplina_fake,
        data_fim=hoje + timedelta(days=5),
        motivo="Indisciplina"
    )


def test_criar_suspensao_aluno_ja_possui_suspensao_ativa(mocker):
    hoje = timezone.now().date()

    aluno_fake = object()
    disciplina_fake = object()

    suspensao_ativa = SimpleNamespace(
        data_fim=hoje + timedelta(days=2)
    )

    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensoesAlunoDisciplina",
        return_value=[suspensao_ativa]
    )

    with pytest.raises(AlunoComSuspensaoJaAtivadaNessaDisciplinaException):
        SuspensaoService.criarSuspensao(
            dataFim=hoje + timedelta(days=5),
            motivo="Indisciplina",
            aluno=aluno_fake,
            disciplina=disciplina_fake
        )
        
def test_remover_suspensao_id_sucesso(mocker):
    suspensao_fake = mocker.Mock()

    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensaoId",
        return_value=suspensao_fake
    )

    SuspensaoService.removerSuspensaoId(1)

    suspensao_fake.delete.assert_called_once()


def test_remover_suspensao_id_nao_existe(mocker):
    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensaoId",
        return_value=None
    )

    with pytest.raises(SuspensaoNaoExisteException):
        SuspensaoService.removerSuspensaoId(1)

def test_remover_suspensoes_matricula_com_suspensoes(mocker):
    suspensao1 = mocker.Mock()
    suspensao2 = mocker.Mock()

    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensoesAluno",
        return_value=[suspensao1, suspensao2]
    )

    SuspensaoService.removerSuspensoesMatricula("2023001")

    suspensao1.delete.assert_called_once()
    suspensao2.delete.assert_called_once()


def test_remover_suspensoes_matricula_sem_suspensoes(mocker):
    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensoesAluno",
        return_value=[]
    )

    # Não deve lançar exceção
    SuspensaoService.removerSuspensoesMatricula("2023001")


def test_remover_suspensoes_matricula_disciplina_com_suspensoes(mocker):
    suspensao1 = mocker.Mock()
    suspensao2 = mocker.Mock()

    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensoesAlunoDisciplina",
        return_value=[suspensao1, suspensao2]
    )

    SuspensaoService.removerSuspensoesMatriculaDisciplina(
        "2023001",
        "MAT001"
    )

    suspensao1.delete.assert_called_once()
    suspensao2.delete.assert_called_once()


def test_remover_suspensoes_matricula_disciplina_sem_suspensoes(mocker):
    mocker.patch(
        "core.services.suspensao_service.SuspensaoService.getSuspensoesAlunoDisciplina",
        return_value=[]
    )

    # Não deve lançar exceção
    SuspensaoService.removerSuspensoesMatriculaDisciplina(
        "2023001",
        "MAT001"
    )