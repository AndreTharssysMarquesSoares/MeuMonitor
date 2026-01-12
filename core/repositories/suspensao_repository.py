from core.models import Suspensao

class SuspensaoRepository:
    
    @staticmethod
    def criarSuspensao(**data):
        return Suspensao.objects.create(**data)
    
    @staticmethod
    def removerSuspensaoId(id):
        Suspensao.objects.filter(id=id).first().delete()
        
    @staticmethod
    def removerSuspensaoMatriculaDisciplina(matricula, disciplina):
        Suspensao.objects.filter(aluno=matricula, disciplina=disciplina).first().delete()
        
    @staticmethod
    def getSuspensaoMatricula(matricula):
        return Suspensao.objects.filter(aluno=matricula).first()
        
    @staticmethod
    def getSuspensaoDisciplina(disciplina):
        return Suspensao.objects.filter(disciplina=disciplina)
    
    @staticmethod
    def getSuspensaoMatriculaDisciplina(matricula, disciplina):
        return Suspensao.objects.filter(aluno=matricula, disciplina=disciplina).first()
    
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