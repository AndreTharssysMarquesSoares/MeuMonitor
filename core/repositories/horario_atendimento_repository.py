from core.models import Disciplina, Usuario, HorarioAtendimento

class HorarioAtendimentoRepository:
    
    @staticmethod
    def criar_Horario(**data):
        return HorarioAtendimento.objects.create(**data) 
    
    @staticmethod
    def removeHorario(id):
        HorarioAtendimento.objects.filter(id = id).delete()
    
    @staticmethod
    def getHorariosDoMonitor(matricula):
        return HorarioAtendimento.objects.filter(matricula=matricula)
    
    @staticmethod
    def getHorarioInicio(id):
        return HorarioAtendimento.objects.filter(id = id).first().hora_inicio
    
    @staticmethod
    def getHorarioFim(id):
        return HorarioAtendimento.objects.filter(id = id).first().hora_fim
    
    @staticmethod
    def getHorarioDiaSemana(id):
        return HorarioAtendimento.objects.filter(id = id).first().dia_semana
    
    @staticmethod
    def getHorarioMonitor(id):
        return HorarioAtendimento.objects.filter(id = id).first().monitor
    
    @staticmethod
    def getHorarioDisciplina(id):
        return HorarioAtendimento.objects.filter(id = id).first().disciplina
    
    @staticmethod
    def getHorario(id):
        return HorarioAtendimento.objects.filter(id = id).first
    
    @staticmethod
    def salvar(horario):
        horario.save()