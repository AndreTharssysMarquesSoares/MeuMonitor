from core.services.aluno_service import AlunoService
from core.services.usuario_service import UsuarioService
from core.services.disciplina_service import DisciplinaService
from core.repositories.horario_atendimento_repository import HorarioAtendimentoRepository
from core.exceptions.horarios_atendimento_exceptions import HorarioInvalidoException, HorariosSobrepostosException, DiaSemanaInvalidoException, HorarioNaoExisteException, HorarioNaoPertenceAoMonitorException, DadosHorarioInvalidoException
from core.exceptions.usuario_exceptions import AlunoNaoMonitorException, SenhaIncorretaException
from enum import Enum
from datetime import datetime

class DiaSemana(Enum):
    SEGUNDA = 1
    TERCA = 2
    QUARTA = 3
    QUINTA = 4
    SEXTA = 5
    
class HorarioAtendimentoService: 
    
    @staticmethod
    def verificarHorariosSobrepostos(novoHorarioInicio, novoHorarioFim, matricula):
        horariosDoMonitor =  HorarioAtendimentoService.getHorariosMonitor(matricula)
        existeHorarioSobreposto = False
        
        for h in horariosDoMonitor:
            horarioInicioExistente = HorarioAtendimentoRepository.getHorarioInicio(h.id)
            horarioFimExistente = HorarioAtendimentoRepository.getHorarioFim(h.id)
            
            existeHorarioSobreposto = HorarioAtendimentoService.verificarHorarioSobreposto(novoHorarioInicio, novoHorarioFim, horarioInicioExistente, horarioFimExistente)
            
            if existeHorarioSobreposto: break
            
        return existeHorarioSobreposto
        
    @staticmethod
    def verificarHorarioSobreposto(novoHorarioInicio, novoHorarioFim, horarioInicioExistente, horarioFimExistente):
        return novoHorarioInicio < horarioFimExistente and novoHorarioFim > horarioInicioExistente
    
    @staticmethod
    def getHorario(id):
        horario = HorarioAtendimentoRepository.getHorario(id)
        if not horario: raise HorarioNaoExisteException()
        return horario
    
    @staticmethod
    def cadastrarHorario(matricula, diaSemana, horarioInicio, horarioFim):
        
        monitor = AlunoService.getAluno(matricula=matricula)
        
        # Verifica se o aluno é monitor
        if not AlunoService.isMonitor(matricula): raise AlunoNaoMonitorException()
        
        inicio = datetime.strptime(horarioInicio, "%H:%M").time()
        fim = datetime.strptime(horarioFim, "%H:%M").time()

        # Verifica se os horarios nao estao "Trocados"
        if fim <= inicio: raise HorarioInvalidoException()
        
        # Verifica Se há horarios sobrepostos
        if HorarioAtendimentoService.verificarHorariosSobrepostos(inicio, fim, matricula): raise HorariosSobrepostosException()
            
        # Verifica se o dia da semana selecionado esta entre segunda e sexta
        if diaSemana < 1 or diaSemana > 5: raise DiaSemanaInvalidoException()
        
        disciplina_codigo = monitor.monitor_de.codigo
        
        horario = HorarioAtendimentoRepository.criar_Horario(
            dia_semana = diaSemana,
            hora_inicio = inicio,
            hora_fim = fim,
            disciplina_id = disciplina_codigo,
            monitor_id = monitor.matricula
        )
        
        return horario
        
    @staticmethod
    def removerHorario(matriculaMonitor, senhaMonitor, idHorario):
        
        # Verifica se o aluno é monitor
        if not AlunoService.isMonitor(matriculaMonitor): raise AlunoNaoMonitorException() 
        
        # Verifica acesso do monitor
        if not UsuarioService.validarSenha(matriculaMonitor, senhaMonitor): raise SenhaIncorretaException()
        
        # Verifica se o horario é do monitor
        if HorarioAtendimentoRepository.getHorarioMonitor(idHorario) != matriculaMonitor: raise HorarioNaoPertenceAoMonitorException()
        
        HorarioAtendimentoRepository.removeHorario(idHorario)
        
        return True
        
    @staticmethod
    def alterarHorario(matriculaMonitor, senhaMonitor, idHorario, **payload):
        
        """
        payload opcional:
        - dia_semana
        - horario_inicio
        - horario_fim
        """
        
        # Verifica se o aluno é monitor
        if not AlunoService.isMonitor(matriculaMonitor): raise AlunoNaoMonitorException() 
        
        # Verifica o acesso do monitor
        if not UsuarioService.validarSenha(matriculaMonitor, senhaMonitor): raise SenhaIncorretaException()
        
        horario = HorarioAtendimentoService.getHorario(idHorario)
        
        # verifica se o horario é do monitor
        if HorarioAtendimentoRepository.getHorarioMonitor(idHorario) != matriculaMonitor: raise HorarioNaoPertenceAoMonitorException()
        
        dia_semana = payload.get("dia_semana") 
        if dia_semana is not None:
            if dia_semana == "":
                raise DadosHorarioInvalidoException()
            if dia_semana < 1 or dia_semana > 5: raise DiaSemanaInvalidoException()
            horario.dia_semana = dia_semana
            
        horario_inicio = payload.get("horario_inicio") 
        if horario_inicio is not None:
            if horario_inicio == "":
                raise DadosHorarioInvalidoException()
            else:
                horario_inicio = datetime.strptime(horario_inicio, "%H:%M").time()
        else:
            horario_inicio = HorarioAtendimentoRepository.getHorarioInicio(idHorario)
        
        horario_fim = payload.get("horario_fim") 
        if horario_fim is not None:
            if horario_fim == "":
                raise DadosHorarioInvalidoException()
            else:
                horario_fim = datetime.strptime(horario_fim, "%H:%M").time()
        else:
            horario_fim = HorarioAtendimentoRepository.getHorarioFim(idHorario)
        
        # Verifica se os horarios nao estao "Trocados"
        if horario_fim <= horario_inicio: raise HorarioInvalidoException()
        
        # Verifica Se há horarios sobrepostos
        if HorarioAtendimentoService.verificarHorariosSobrepostos(horario_inicio, horario_fim, matriculaMonitor): raise HorariosSobrepostosException()
        
        horario.hora_inicio = horario_inicio
        horario.hora_fim = horario_fim
        
        HorarioAtendimentoRepository.salvar(horario)
        
        return horario
              
    @staticmethod
    def getHorariosMonitor(matricula):
        if not AlunoService.isMonitor(matricula): raise AlunoNaoMonitorException() 
        horarios = HorarioAtendimentoRepository.getHorariosDoMonitor(matricula)
        return horarios