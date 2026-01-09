from core.services.aluno_service import AlunoService
from core.services.usuario_service import UsuarioService
from core.services.disciplina_service import DisciplinaService
from core.repositories.horario_atendimento_repository import HorarioAtendimentoRepository
from core.exceptions.horarios_atendimento_exceptions import HorarioInvalidoException, HorariosSobrepostosException, DiaSemanaInvalidoException, HorarioNaoExisteException, HorarioNaoPertenceAoMonitorException, DadosHorarioInvalidoException, SalaOcupadaException
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
    def verificarHorariosSobrepostos(novoHorarioInicio, novoHorarioFim, matricula):
        horariosDoMonitor =  HorarioAtendimentoService.getHorariosDoMonitor(matricula)
        existeHorarioSobreposto = False
        
        for h in horariosDoMonitor:
            horarioInicioExistente = HorarioAtendimentoRepository.getHoraInicio(h.id)
            horarioFimExistente = HorarioAtendimentoRepository.getHoraFim(h.id)
            
            existeHorarioSobreposto = novoHorarioInicio < horarioFimExistente and novoHorarioFim > horarioInicioExistente
            
            if existeHorarioSobreposto: break
            
        return existeHorarioSobreposto
    
    def verificarSalaOcupada(novoHorarioInicio, novoHorarioFim, local):
        horariosDaSala = HorarioAtendimentoRepository.getHorariosDaSala(local)
        salaOcupada = False
        
        for h in horariosDaSala:
            
            horarioInicioExistente = HorarioAtendimentoRepository.getHoraInicio(h.id)
            horarioFimExistente = HorarioAtendimentoRepository.getHoraFim(h.id)
            
            salaOcupada = novoHorarioInicio < horarioFimExistente and novoHorarioFim > horarioInicioExistente
            
            if salaOcupada: break
            
        return salaOcupada
    
    
    @staticmethod
    def cadastrarHorario(matricula, diaSemana, horarioInicio, horarioFim, local):
        
        monitor = AlunoService.getAluno(matricula=matricula)
        
        # Verifica se o aluno é monitor
        if not AlunoService.isMonitor(matricula): raise AlunoNaoMonitorException()
        
        horarioInicio = datetime.strptime(horarioInicio, "%H:%M").time()
        horarioFim = datetime.strptime(horarioFim, "%H:%M").time()

        # Verifica se os horarios nao estao "Trocados"
        if horarioFim <= horarioInicio: raise HorarioInvalidoException()
        
        # Verifica Se há horarios sobrepostos
        if HorarioAtendimentoService.verificarHorariosSobrepostos(horarioInicio, horarioFim, matricula): raise HorariosSobrepostosException()
            
        # Verifica se o dia da semana selecionado esta entre segunda e sexta
        try:
            dia_enum = DiaSemana(diaSemana)
        except ValueError:
            raise DiaSemanaInvalidoException()

        if dia_enum.value > 5:
            raise DiaSemanaInvalidoException()
        
        local = local.replace(" ", "").replace("-", "")
        
        if HorarioAtendimentoService.verificarSalaOcupada(horarioInicio, horarioFim, local): raise SalaOcupadaException()
        
        disciplina_codigo = monitor.monitor_de
        
        horario = HorarioAtendimentoRepository.criar_Horario(
            dia_semana = dia_enum,
            hora_inicio = horarioInicio,
            hora_fim = horarioFim,
            disciplina_id = disciplina_codigo,
            monitor_id = monitor.matricula,
            local = local
        )
        
        return horario
        
    @staticmethod
    def removerHorario(matriculaMonitor, senhaMonitor, idHorario):
        
        # Verifica se o aluno é monitor
        if not AlunoService.isMonitor(matriculaMonitor): raise AlunoNaoMonitorException() 
        
        # Verifica acesso do monitor
        if not UsuarioService.validarSenha(matriculaMonitor, senhaMonitor): raise SenhaIncorretaException()
        
        # Verifica se o horario é do monitor
        if HorarioAtendimentoRepository.getMonitor(idHorario) != matriculaMonitor: raise HorarioNaoPertenceAoMonitorException()
        
        HorarioAtendimentoRepository.removeHorario(idHorario)
        
        return True
        
    @staticmethod
    def alterarHorario(matriculaMonitor, senhaMonitor, idHorario, **payload):
        
        """
        payload opcional:
        - dia_semana
        - horario_inicio
        - horario_fim
        - local
        """
        
        # Verifica se o aluno é monitor
        if not AlunoService.isMonitor(matriculaMonitor): raise AlunoNaoMonitorException() 
        
        # Verifica o acesso do monitor
        if not UsuarioService.validarSenha(matriculaMonitor, senhaMonitor): raise SenhaIncorretaException()
        
        horario = HorarioAtendimentoService.getHorario(idHorario)
        
        # verifica se o horario é do monitor
        if HorarioAtendimentoRepository.getMonitor(idHorario) != matriculaMonitor: raise HorarioNaoPertenceAoMonitorException()
        
        dia_semana = payload.get("dia_semana") 
        if dia_semana is not None:
            if dia_semana == "":
                raise DadosHorarioInvalidoException()
            
            try:
                dia_enum = DiaSemana(dia_semana)
            except ValueError:
                raise DiaSemanaInvalidoException()
            
            if dia_enum.value > 5: raise DiaSemanaInvalidoException()
            horario.dia_semana = dia_enum
            
        horario_inicio = payload.get("horario_inicio") 
        if horario_inicio is not None:
            if horario_inicio == "":
                raise DadosHorarioInvalidoException()
            else:
                horario_inicio = datetime.strptime(horario_inicio, "%H:%M").time()
        else:
            horario_inicio = HorarioAtendimentoRepository.getHoraInicio(idHorario)
        
        horario_fim = payload.get("horario_fim") 
        if horario_fim is not None:
            if horario_fim == "":
                raise DadosHorarioInvalidoException()
            else:
                horario_fim = datetime.strptime(horario_fim, "%H:%M").time()
        else:
            horario_fim = HorarioAtendimentoRepository.getHoraFim(idHorario)
        
        # Verifica se os horarios nao estao "Trocados"
        if horario_fim <= horario_inicio: raise HorarioInvalidoException()
        
        # Verifica Se há horarios sobrepostos
        if HorarioAtendimentoService.verificarHorariosSobrepostos(horario_inicio, horario_fim, matriculaMonitor): raise HorariosSobrepostosException()
        
        horario.hora_inicio = horario_inicio
        horario.hora_fim = horario_fim
        
        local = payload.get("local") 
        if local is not None:
            if local == "":
                raise DadosHorarioInvalidoException()
            else:
                local = local.replace(" ", "").replace("-", "")
            
            if HorarioAtendimentoService.verificarSalaOcupada(horario_inicio, horario_fim, local): raise SalaOcupadaException()
            
            horario.local = local
        
        HorarioAtendimentoRepository.salvar(horario)
        
        return horario
              
    @staticmethod
    def getHorariosMonitor(matricula):
        if not AlunoService.isMonitor(matricula): raise AlunoNaoMonitorException() 
        horarios = HorarioAtendimentoRepository.getHorariosDoMonitor(matricula)
        return horarios
    
    @staticmethod
    def getHorariosDisciplina(codigo):
        disciplina = DisciplinaService.get_Disciplina(codigo)
        if not disciplina: raise CodigoDisciplinaInvalidoException()
        return HorarioAtendimentoRepository.getHorariosDaDisciplina(codigo)
    
    @staticmethod
    def getHorariosLocal(local):
        horarios = HorarioAtendimentoRepository.getHorariosDaSala(local)
        if not horarios: raise HorarioNaoExisteException()
        return horarios
    
    @staticmethod
    def getHorario(id):
        horario = HorarioAtendimentoRepository.getHorario(id)
        if not horario: raise HorarioNaoExisteException()
        return horario