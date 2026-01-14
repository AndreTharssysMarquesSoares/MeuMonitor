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
    def getSuspensoesMatricula(aluno) -> QuerySet[Suspensao]:
        if isinstance(aluno, str):
            return Suspensao.objects.filter(aluno__username=aluno)
        return Suspensao.objects.filter(aluno=aluno)
        
    @staticmethod
    def getSuspensoesDisciplina(disciplina) -> QuerySet[Suspensao]:
        if isinstance(disciplina, str):
            return Suspensao.objects.filter(disciplina__codigo=disciplina)
        return Suspensao.objects.filter(disciplina=disciplina)
    
    @staticmethod
    def getSuspensoesMatriculaDisciplina(aluno, disciplina)-> QuerySet[Suspensao]:
        filtro = {}
        
        if isinstance(aluno, str):
            filtro['aluno__username'] = aluno
        else:
            filtro['aluno'] = aluno
            
        if isinstance(disciplina, str):
            filtro['disciplina__codigo'] = disciplina
        else:
            filtro['disciplina'] = disciplina
        
        return Suspensao.objects.filter(**filtro)
    
    @staticmethod
    def getDataFim(id):
        suspensao = Suspensao.objects.filter(id=id).first()
        return suspensao.data_fim if suspensao else None
    
    @staticmethod
    def getDataInicio(id):
        suspensao = Suspensao.objects.filter(id=id).first()
        return suspensao.data_inicio if suspensao else None
    
    @staticmethod
    def getAluno(id):
        suspensao = Suspensao.objects.filter(id=id).first()
        return suspensao.aluno if suspensao else None
    
    @staticmethod
    def getDisciplina(id):
        suspensao = Suspensao.objects.filter(id=id).first()
        return suspensao.disciplina if suspensao else None
    
    @staticmethod
    def getMotivo(id):
        suspensao = Suspensao.objects.filter(id=id).first()
        return suspensao.motivo if suspensao else None
    
    @staticmethod
    def salvar(suspensao):
        suspensao.save()
        return suspensao