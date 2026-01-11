from core.models import Disciplina, Usuario, HorarioAtendimento

class HorarioAtendimentoRepository:
    
    @staticmethod
    def criar_Horario(**data):
        return HorarioAtendimento.objects.create(**data) 
    
    @staticmethod
    def removeHorario(id):
        HorarioAtendimento.objects.filter(id=id).delete()
    
    @staticmethod
    def getHorariosDoMonitor(matricula):
        return HorarioAtendimento.objects.filter(monitor__username=matricula)
    
    @staticmethod
    def getHorariosDaSala(local):
        return HorarioAtendimento.objects.filter(local=local)
    
    @staticmethod
    def getHorariosDaDisciplina(codigoDisciplina):
        return HorarioAtendimento.objects.filter(disciplina__codigo=codigoDisciplina)
    
    @staticmethod
    def getHoraInicio(id):
        horario = HorarioAtendimento.objects.filter(id=id).first()
        return horario.hora_inicio if horario else None
    
    @staticmethod
    def getHoraFim(id):
        horario = HorarioAtendimento.objects.filter(id=id).first()
        return horario.hora_fim if horario else None
    
    @staticmethod
    def getDiaSemana(id):
        horario = HorarioAtendimento.objects.filter(id=id).first()
        return horario.dia_semana if horario else None
    
    @staticmethod
    def getMonitor(id):
        horario = HorarioAtendimento.objects.filter(id=id).first()
        return horario.monitor if horario else None
    
    @staticmethod
    def getDisciplina(id):
        horario = HorarioAtendimento.objects.filter(id=id).first()
        return horario.disciplina if horario else None
    
    @staticmethod
    def getLocal(id):
        horario = HorarioAtendimento.objects.filter(id=id).first()
        return horario.local if horario else None
    
    @staticmethod
    def getHorario(id):
        return HorarioAtendimento.objects.filter(id=id).first()
    
    @staticmethod
    def salvar(horario):
        horario.save()