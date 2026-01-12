from core.models import Suspensao
from django.db.models import QuerySet

class SuspensaoRepository:
    
    @staticmethod
    def criarSuspensao(**data):
        return Suspensao.objects.create(**data)
    
    @staticmethod
    def removerSuspensaoId(id):
        Suspensao.objects.filter(id=id).first().delete()
        
    @staticmethod
    def getSuspensaoId(id):
        return Suspensao.objects.filter(id=id)
    
    @staticmethod
    def getSuspensoesMatricula(matricula) -> QuerySet[Suspensao]:
        return Suspensao.objects.filter(aluno=matricula)
        
    @staticmethod
    def getSuspensoesDisciplina(disciplina) -> QuerySet[Suspensao]:
        return Suspensao.objects.filter(disciplina=disciplina)
    
    @staticmethod
    def getSuspensoesMatriculaDisciplina(matricula, disciplina)-> QuerySet[Suspensao]:
        return Suspensao.objects.filter(aluno=matricula, disciplina=disciplina)
    
    @staticmethod
    def getDataFim(id):
        return Suspensao.objects.filter(id=id).first().data_fim
    
    @staticmethod
    def getDataInicio(id):
        return Suspensao.objects.filter(id=id).first().data_inicio
    
    @staticmethod
    def getAluno(id):
        return Suspensao.objects.filter(id=id).first().aluno
    
    @staticmethod
    def getDisciplina(id):
        return Suspensao.objects.filter(id=id).first().disciplina
    
    @staticmethod
    def getMotivo(id):
        return Suspensao.objects.filter(id=id).first().motivo
    
    @staticmethod
    def salvar(Suspensao):
        Suspensao.save(Suspensao)