import pytest
from datetime import datetime, time

from core.services.horario_atendimento_service import *
from core.exceptions.horario_atendimento_exceptions import *

def criar_horario_mock(dia, inicio, fim, mocker):
    h = mocker.Mock()
    h.dia_semana = dia
    h.hora_inicio = inicio
    h.hora_fim = fim
    return h

def test_verificar_horarios_sem_horarios_cadastrados(mocker):
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.getHorariosMonitor",
        return_value=[]
    )

    resultado = HorarioAtendimentoService.verificarHorariosSobrepostos(
        novoHorarioInicio=time(10, 0),
        novoHorarioFim=time(11, 0),
        matricula="123",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is False

def test_verificar_horarios_dia_diferente_nao_sobrepoe(mocker):
    horarios = [
        criar_horario_mock(DiaSemana.TER, time(9, 0), time(10, 0), mocker)
    ]

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.getHorariosMonitor",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarHorariosSobrepostos(
        novoHorarioInicio=time(9, 0),
        novoHorarioFim=time(10, 0),
        matricula="123",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is False

def test_verificar_horarios_com_sobreposicao_total(mocker):
    horarios = [
        criar_horario_mock(DiaSemana.SEG, time(9, 0), time(11, 0), mocker)
    ]

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.getHorariosMonitor",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarHorariosSobrepostos(
        novoHorarioInicio=time(10, 0),
        novoHorarioFim=time(10, 30),
        matricula="123",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is True

def test_verificar_horarios_com_sobreposicao_parcial_inicio(mocker):
    horarios = [
        criar_horario_mock(DiaSemana.SEG, time(9, 0), time(10, 0), mocker)
    ]

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.getHorariosMonitor",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarHorariosSobrepostos(
        novoHorarioInicio=time(9, 30),
        novoHorarioFim=time(10, 30),
        matricula="123",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is True

def test_verificar_horarios_com_sobreposicao_parcial_fim(mocker):
    horarios = [
        criar_horario_mock(DiaSemana.SEG, time(9, 30), time(10, 30), mocker)
    ]

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.getHorariosMonitor",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarHorariosSobrepostos(
        novoHorarioInicio=time(9, 0),
        novoHorarioFim=time(10, 0),
        matricula="123",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is True


def test_verificar_horarios_encostando_sem_sobreposicao(mocker):
    horarios = [
        criar_horario_mock(DiaSemana.SEG, time(10, 0), time(11, 0), mocker)
    ]

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.getHorariosMonitor",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarHorariosSobrepostos(
        novoHorarioInicio=time(9, 0),
        novoHorarioFim=time(10, 0),
        matricula="123",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is False

def test_verificar_horarios_varios_horarios_um_sobreposto(mocker):
    horarios = [
        criar_horario_mock(DiaSemana.SEG, time(8, 0), time(9, 0), mocker),
        criar_horario_mock(DiaSemana.SEG, time(10, 0), time(11, 0), mocker),
    ]

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.getHorariosMonitor",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarHorariosSobrepostos(
        novoHorarioInicio=time(10, 30),
        novoHorarioFim=time(11, 30),
        matricula="123",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is True

import pytest
from datetime import time

from core.services.horario_atendimento_service import (
    HorarioAtendimentoService,
    DiaSemana
)

def criar_horario_sala_mock(id, dia, inicio, fim, mocker):
    h = mocker.Mock()
    h.id = id
    h.dia_semana = dia
    h.hora_inicio = inicio
    h.hora_fim = fim
    return h

def test_verificar_sala_sem_horarios(mocker):
    mocker.patch(
        "core.repositories.horario_atendimento_repository.HorarioAtendimentoRepository.getHorariosDaSala",
        return_value=[]
    )

    resultado = HorarioAtendimentoService.verificarSalaOcupada(
        novoHorarioInicio=time(10, 0),
        novoHorarioFim=time(11, 0),
        local="Sala 01",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is False

def test_verificar_sala_dia_diferente_nao_ocupada(mocker):
    horarios = [
        criar_horario_sala_mock(1, DiaSemana.TER, time(9, 0), time(10, 0), mocker)
    ]

    mocker.patch(
        "core.repositories.horario_atendimento_repository.HorarioAtendimentoRepository.getHorariosDaSala",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarSalaOcupada(
        novoHorarioInicio=time(9, 0),
        novoHorarioFim=time(10, 0),
        local="Sala 01",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is False


def test_verificar_sala_ocupada_sobreposicao_total(mocker):
    horarios = [
        criar_horario_sala_mock(1, DiaSemana.SEG, time(9, 0), time(11, 0), mocker)
    ]

    mocker.patch(
        "core.repositories.horario_atendimento_repository.HorarioAtendimentoRepository.getHorariosDaSala",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarSalaOcupada(
        novoHorarioInicio=time(10, 0),
        novoHorarioFim=time(10, 30),
        local="Sala 01",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is True

def test_verificar_sala_ocupada_sobreposicao_parcial(mocker):
    horarios = [
        criar_horario_sala_mock(1, DiaSemana.SEG, time(9, 0), time(10, 0), mocker)
    ]

    mocker.patch(
        "core.repositories.horario_atendimento_repository.HorarioAtendimentoRepository.getHorariosDaSala",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarSalaOcupada(
        novoHorarioInicio=time(9, 30),
        novoHorarioFim=time(10, 30),
        local="Sala 01",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is True


def test_verificar_sala_encostando_sem_ocupacao(mocker):
    horarios = [
        criar_horario_sala_mock(1, DiaSemana.SEG, time(10, 0), time(11, 0), mocker)
    ]

    mocker.patch(
        "core.repositories.horario_atendimento_repository.HorarioAtendimentoRepository.getHorariosDaSala",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarSalaOcupada(
        novoHorarioInicio=time(9, 0),
        novoHorarioFim=time(10, 0),
        local="Sala 01",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is False


def test_verificar_sala_ocupada_ignorando_horario_excluido(mocker):
    horarios = [
        criar_horario_sala_mock(5, DiaSemana.SEG, time(9, 0), time(11, 0), mocker)
    ]

    mocker.patch(
        "core.repositories.horario_atendimento_repository.HorarioAtendimentoRepository.getHorariosDaSala",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarSalaOcupada(
        novoHorarioInicio=time(10, 0),
        novoHorarioFim=time(10, 30),
        local="Sala 01",
        diaSemana=DiaSemana.SEG,
        horarioIdExcluir="5"
    )

    assert resultado is False

def test_verificar_sala_varios_horarios_um_conflitante(mocker):
    horarios = [
        criar_horario_sala_mock(1, DiaSemana.SEG, time(8, 0), time(9, 0), mocker),
        criar_horario_sala_mock(2, DiaSemana.SEG, time(10, 0), time(11, 0), mocker),
    ]

    mocker.patch(
        "core.repositories.horario_atendimento_repository.HorarioAtendimentoRepository.getHorariosDaSala",
        return_value=horarios
    )

    resultado = HorarioAtendimentoService.verificarSalaOcupada(
        novoHorarioInicio=time(10, 30),
        novoHorarioFim=time(11, 30),
        local="Sala 01",
        diaSemana=DiaSemana.SEG
    )

    assert resultado is True

def mock_monitor(mocker):
    monitor = mocker.Mock()
    monitor.monitor_de = mocker.Mock()
    return monitor


def test_cadastrar_horario_sucesso(mocker):
    monitor = mock_monitor(mocker)
    horario_criado = mocker.Mock()

    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=monitor
    )
    mocker.patch(
        "core.services.aluno_service.AlunoService.isMonitor",
        return_value=True
    )
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.verificarHorariosSobrepostos",
        return_value=False
    )
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.verificarSalaOcupada",
        return_value=False
    )
    criar = mocker.patch(
        "core.repositories.horario_atendimento_repository.HorarioAtendimentoRepository.criar_Horario",
        return_value=horario_criado
    )

    resultado = HorarioAtendimentoService.cadastrarHorario(
        matricula="2023001",
        diaSemana="SEG",
        horarioInicio="09:00",
        horarioFim="10:00",
        local="  Sala 01  "
    )

    assert resultado == horario_criado
    criar.assert_called_once()
    args, kwargs = criar.call_args

    assert kwargs["hora_inicio"] == time(9, 0)
    assert kwargs["hora_fim"] == time(10, 0)
    assert kwargs["local"] == "Sala 01"


def test_cadastrar_horario_aluno_nao_monitor(mocker):
    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=mocker.Mock()
    )
    mocker.patch(
        "core.services.aluno_service.AlunoService.isMonitor",
        return_value=False
    )

    with pytest.raises(AlunoNaoMonitorException):
        HorarioAtendimentoService.cadastrarHorario(
            matricula="1",
            diaSemana="SEG",
            horarioInicio="09:00",
            horarioFim="10:00",
            local="Sala"
        )


def test_cadastrar_horario_horario_invalido(mocker):
    mocker.patch(
        "core.services.aluno_service.AlunoService.getAluno",
        return_value=mocker.Mock()
    )
    mocker.patch(
        "core.services.aluno_service.AlunoService.isMonitor",
        return_value=True
    )

    with pytest.raises(HorarioInvalidoException):
        HorarioAtendimentoService.cadastrarHorario(
            matricula="1",
            diaSemana="SEG",
            horarioInicio="10:00",
            horarioFim="09:00",
            local="Sala"
        )


def test_cadastrar_horario_sobreposto(mocker):
    mocker.patch("core.services.aluno_service.AlunoService.getAluno", return_value=mocker.Mock())
    mocker.patch("core.services.aluno_service.AlunoService.isMonitor", return_value=True)
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.verificarHorariosSobrepostos",
        return_value=True
    )

    with pytest.raises(HorariosSobrepostosException):
        HorarioAtendimentoService.cadastrarHorario(
            matricula="1",
            diaSemana="SEG",
            horarioInicio="09:00",
            horarioFim="10:00",
            local="Sala"
        )


def test_cadastrar_horario_dia_semana_invalido_nome(mocker):
    mocker.patch("core.services.aluno_service.AlunoService.getAluno", return_value=mocker.Mock())
    mocker.patch("core.services.aluno_service.AlunoService.isMonitor", return_value=True)
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.verificarHorariosSobrepostos",
        return_value=False
    )

    with pytest.raises(DiaSemanaInvalidoException):
        HorarioAtendimentoService.cadastrarHorario(
            matricula="1",
            diaSemana="XXX",
            horarioInicio="09:00",
            horarioFim="10:00",
            local="Sala"
        )


def test_cadastrar_horario_dia_semana_domingo(mocker):
    mocker.patch("core.services.aluno_service.AlunoService.getAluno", return_value=mocker.Mock())
    mocker.patch("core.services.aluno_service.AlunoService.isMonitor", return_value=True)
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.verificarHorariosSobrepostos",
        return_value=False
    )

    with pytest.raises(DiaSemanaInvalidoException):
        HorarioAtendimentoService.cadastrarHorario(
            matricula="1",
            diaSemana="DOM",
            horarioInicio="09:00",
            horarioFim="10:00",
            local="Sala"
        )


def test_cadastrar_horario_sala_ocupada(mocker):
    mocker.patch("core.services.aluno_service.AlunoService.getAluno", return_value=mocker.Mock())
    mocker.patch("core.services.aluno_service.AlunoService.isMonitor", return_value=True)
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.verificarHorariosSobrepostos",
        return_value=False
    )
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.verificarSalaOcupada",
        return_value=True
    )

    with pytest.raises(SalaOcupadaException):
        HorarioAtendimentoService.cadastrarHorario(
            matricula="1",
            diaSemana="SEG",
            horarioInicio="09:00",
            horarioFim="10:00",
            local="Sala"
        )

def mock_horario(mocker, username, horario_id=1, dia="SEG", inicio=time(8, 0), fim=time(9, 0), local="Sala 1"):
    horario = mocker.Mock()
    horario.id = horario_id
    horario.dia_semana = dia
    horario.hora_inicio = inicio
    horario.hora_fim = fim
    horario.local = local

    monitor = mocker.Mock()
    monitor.username = username
    horario.monitor = monitor

    return horario

def test_remover_horario_web_sucesso(mocker):
    horario = mock_horario(mocker, username="2023001", horario_id=10)

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoRepository.getHorario",
        return_value=horario
    )
    remover = mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoRepository.removeHorario"
    )

    resultado = HorarioAtendimentoService.removerHorarioWeb(
        idHorario=10,
        matriculaMonitor="2023001"
    )

    assert resultado is True
    remover.assert_called_once_with(10)

def test_remover_horario_web_horario_inexistente(mocker):
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoRepository.getHorario",
        return_value=None
    )

    with pytest.raises(HorarioNaoExisteException):
        HorarioAtendimentoService.removerHorarioWeb(
            idHorario=1,
            matriculaMonitor="2023001"
        )

def test_remover_horario_web_nao_pertence_monitor(mocker):
    horario = mock_horario(mocker, username="OUTRO")

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoRepository.getHorario",
        return_value=horario
    )

    with pytest.raises(HorarioNaoPertenceAoMonitorException):
        HorarioAtendimentoService.removerHorarioWeb(
            idHorario=1,
            matriculaMonitor="2023001"
        )

def test_editar_horario_web_sucesso(mocker):
    horario = mock_horario(mocker, username="2023001", horario_id=1)

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoRepository.getHorario",
        return_value=horario
    )
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.getHorariosMonitor",
        return_value=[horario]
    )
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.verificarSalaOcupada",
        return_value=False
    )
    salvar = mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoRepository.salvar"
    )

    resultado = HorarioAtendimentoService.editarHorarioWeb(
        idHorario=1,
        matriculaMonitor="2023001",
        diaSemana="SEG",
        horarioInicio="09:00",
        horarioFim="10:00",
        local=" Sala 2 "
    )

    assert resultado == horario
    assert horario.local == "Sala 2"
    salvar.assert_called_once_with(horario)

def test_editar_horario_web_horario_inexistente(mocker):
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoRepository.getHorario",
        return_value=None
    )

    with pytest.raises(HorarioNaoExisteException):
        HorarioAtendimentoService.editarHorarioWeb(
            idHorario=1,
            matriculaMonitor="2023001",
            diaSemana="SEG",
            horarioInicio="08:00",
            horarioFim="09:00",
            local="Sala"
        )

def test_editar_horario_web_nao_pertence_monitor(mocker):
    horario = mock_horario(mocker, username="OUTRO")

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoRepository.getHorario",
        return_value=horario
    )

    with pytest.raises(HorarioNaoPertenceAoMonitorException):
        HorarioAtendimentoService.editarHorarioWeb(
            idHorario=1,
            matriculaMonitor="2023001",
            diaSemana="SEG",
            horarioInicio="08:00",
            horarioFim="09:00",
            local="Sala"
        )

def test_editar_horario_web_horarios_sobrepostos(mocker):
    horario_atual = mock_horario(mocker, username="2023001", horario_id=1)
    outro_horario = mock_horario(
        mocker,
        username="2023001",
        horario_id=2,
        inicio=time(9, 0),
        fim=time(11, 0)
    )

    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoRepository.getHorario",
        return_value=horario_atual
    )
    mocker.patch(
        "core.services.horario_atendimento_service.HorarioAtendimentoService.getHorariosMonitor",
        return_value=[horario_atual, outro_horario]
    )

    with pytest.raises(HorariosSobrepostosException):
        HorarioAtendimentoService.editarHorarioWeb(
            idHorario=1,
            matriculaMonitor="2023001",
            diaSemana="SEG",
            horarioInicio="10:00",
            horarioFim="12:00",
            local="Sala"
        )
