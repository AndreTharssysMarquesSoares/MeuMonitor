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
    def getHorariosDaSala(local):
        return HorarioAtendimento.objects.filter(local = local)
    
    @staticmethod
    def getHorariosDaDisciplina(codigoDisciplina):
        return HorarioAtendimento.objects.filter(disciplina=codigoDisciplina)
    
    @staticmethod
    def getHoraInicio(id):
        return HorarioAtendimento.objects.filter(id = id).first().hora_inicio
    
    @staticmethod
    def getHoraFim(id):
        return HorarioAtendimento.objects.filter(id = id).first().hora_fim
    
    @staticmethod
    def getDiaSemana(id):
        return HorarioAtendimento.objects.filter(id = id).first().dia_semana
    
    @staticmethod
    def getMonitor(id):
        return HorarioAtendimento.objects.filter(id = id).first().monitor
    
    @staticmethod
    def getDisciplina(id):
        return HorarioAtendimento.objects.filter(id = id).first().disciplina
    
    @staticmethod
    def getLocal(id):
        return HorarioAtendimento.objects.filter(id = id).first().local
    
    @staticmethod
    def getHorario(id):
        return HorarioAtendimento.objects.filter(id = id).first
    
    @staticmethod
    def salvar(horario):
        horario.save()