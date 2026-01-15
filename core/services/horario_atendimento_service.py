from core.services.aluno_service import AlunoService
from core.services.usuario_service import UsuarioService
from core.services.disciplina_service import DisciplinaService
from core.repositories.horario_atendimento_repository import HorarioAtendimentoRepository
from core.exceptions.horario_atendimento_exceptions import *
from core.exceptions.usuario_exceptions import AlunoNaoMonitorException, SenhaIncorretaException
from core.exceptions.disciplina_exceptions import CodigoDisciplinaInvalidoException
from enum import Enum
from datetime import datetime

class DiaSemana(Enum):
    SEG = 1
    TER = 2
    QUA = 3
    QUI = 4
    SEX = 5
    SAB = 6
    DOM = 7

class HorarioAtendimentoService: 
    
    @staticmethod
    def verificarHorariosSobrepostos(novoHorarioInicio, novoHorarioFim, matricula, diaSemana):
        horariosDoMonitor = HorarioAtendimentoService.getHorariosMonitor(matricula)
        existeHorarioSobreposto = False
        
        for h in horariosDoMonitor:
            # Só verifica sobreposição se for no mesmo dia da semana
            if h.dia_semana != diaSemana:
                continue
    
            horarioInicioExistente = h.hora_inicio
            horarioFimExistente = h.hora_fim
            
            existeHorarioSobreposto = novoHorarioInicio < horarioFimExistente and novoHorarioFim > horarioInicioExistente
            
            if existeHorarioSobreposto: 
                break
            
        return existeHorarioSobreposto
    
    @staticmethod
    def verificarSalaOcupada(novoHorarioInicio, novoHorarioFim, local, diaSemana, horarioIdExcluir=None):
        horariosDaSala = HorarioAtendimentoRepository.getHorariosDaSala(local)
        salaOcupada = False
        
        for h in horariosDaSala:
            if horarioIdExcluir and h.id == int(horarioIdExcluir):
                continue
        
            if h.dia_semana != diaSemana:
                continue
                
            horarioInicioExistente = h.hora_inicio
            horarioFimExistente = h.hora_fim
            
            salaOcupada = novoHorarioInicio < horarioFimExistente and novoHorarioFim > horarioInicioExistente
            
            if salaOcupada: 
                break
            
        return salaOcupada
    
    @staticmethod
    def cadastrarHorario(matricula, diaSemana, horarioInicio, horarioFim, local):
        
        monitor = AlunoService.getAluno(matricula=matricula)
        
        if not AlunoService.isMonitor(matricula): 
            raise AlunoNaoMonitorException()
        
        horarioInicio = datetime.strptime(horarioInicio, "%H:%M").time()
        horarioFim = datetime.strptime(horarioFim, "%H:%M").time()

        if horarioFim <= horarioInicio: 
            raise HorarioInvalidoException()
        
        if HorarioAtendimentoService.verificarHorariosSobrepostos(horarioInicio, horarioFim, matricula, diaSemana): 
            raise HorariosSobrepostosException()
        
        try:
            dia_enum = DiaSemana[diaSemana]
        except KeyError:
            raise DiaSemanaInvalidoException()

        if dia_enum.value > 6:
            raise DiaSemanaInvalidoException()
        
        local_normalizado = local.strip()
     
        if HorarioAtendimentoService.verificarSalaOcupada(horarioInicio, horarioFim, local_normalizado, diaSemana): 
            raise SalaOcupadaException()
        
        disciplina = monitor.monitor_de
        
        horario = HorarioAtendimentoRepository.criar_Horario(
            dia_semana=diaSemana,
            hora_inicio=horarioInicio,
            hora_fim=horarioFim,
            disciplina=disciplina,
            monitor=monitor,
            local=local_normalizado
        )
        
        return horario
    
    @staticmethod
    def removerHorario(matriculaMonitor, senhaMonitor, idHorario):

        if not AlunoService.isMonitor(matriculaMonitor): 
            raise AlunoNaoMonitorException() 

        if not UsuarioService.validarSenha(matriculaMonitor, senhaMonitor): 
            raise SenhaIncorretaException()
        
        horario = HorarioAtendimentoRepository.getHorario(idHorario)
        if not horario:
            raise HorarioNaoExisteException()

        if horario.monitor.username != matriculaMonitor: 
            raise HorarioNaoPertenceAoMonitorException()
        
        HorarioAtendimentoRepository.removeHorario(idHorario)
        
        return True
    
    @staticmethod
    def removerHorarioWeb(idHorario, matriculaMonitor):
        """Versão simplificada para uso na web (usuário já autenticado)"""
        horario = HorarioAtendimentoRepository.getHorario(idHorario)
        if not horario:
            raise HorarioNaoExisteException()

        if horario.monitor.username != matriculaMonitor: 
            raise HorarioNaoPertenceAoMonitorException()
        
        HorarioAtendimentoRepository.removeHorario(idHorario)
        return True

    @staticmethod
    def editarHorarioWeb(idHorario, matriculaMonitor, diaSemana, horarioInicio, horarioFim, local):
        """Versão simplificada para edição na web (usuário já autenticado)"""
        
        horario = HorarioAtendimentoRepository.getHorario(idHorario)
        if not horario:
            raise HorarioNaoExisteException()

        if horario.monitor.username != matriculaMonitor: 
            raise HorarioNaoPertenceAoMonitorException()

        horarioInicio = datetime.strptime(horarioInicio, "%H:%M").time()
        horarioFim = datetime.strptime(horarioFim, "%H:%M").time()

        if horarioFim <= horarioInicio: 
            raise HorarioInvalidoException()

        try:
            dia_enum = DiaSemana[diaSemana]
        except KeyError:
            raise DiaSemanaInvalidoException()

        if dia_enum.value > 6:
            raise DiaSemanaInvalidoException()
        
        local_normalizado = local.strip()

        horariosDoMonitor = HorarioAtendimentoService.getHorariosMonitor(matriculaMonitor)
        for h in horariosDoMonitor:
            if h.id == int(idHorario):
                continue  # Ignora o próprio horário
            if h.dia_semana != diaSemana:
                continue  # Só verifica no mesmo dia
            if horarioInicio < h.hora_fim and horarioFim > h.hora_inicio:
                raise HorariosSobrepostosException()

        if HorarioAtendimentoService.verificarSalaOcupada(horarioInicio, horarioFim, local_normalizado, diaSemana, idHorario): 
            raise SalaOcupadaException()

        horario.dia_semana = diaSemana
        horario.hora_inicio = horarioInicio
        horario.hora_fim = horarioFim
        horario.local = local_normalizado
        
        HorarioAtendimentoRepository.salvar(horario)
        
        return horario
    
    @staticmethod
    def getHorariosMonitor(matricula):
        """Retorna os horários de um monitor específico"""
        from core.models import HorarioAtendimento
        return HorarioAtendimento.objects.filter(monitor__username=matricula)
    
    @staticmethod
    def getHorariosDisciplina(codigo):
        """Retorna os horários de uma disciplina"""
        from core.models import HorarioAtendimento, Disciplina
        disciplina = Disciplina.objects.filter(codigo=codigo).first()
        if not disciplina: 
            raise CodigoDisciplinaInvalidoException()
        return HorarioAtendimento.objects.filter(disciplina=disciplina)
    
    @staticmethod
    def getHorariosLocal(local):
        horarios = HorarioAtendimentoRepository.getHorariosDaSala(local)
        if not horarios: 
            raise HorarioNaoExisteException()
        return horarios
    
    @staticmethod
    def getHorario(id):
        horario = HorarioAtendimentoRepository.getHorario(id)
        if not horario: 
            raise HorarioNaoExisteException()
        return horario