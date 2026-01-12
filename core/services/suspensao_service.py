from core.exceptions.suspensao_exceptions import SuspensaoComDadosInvalidosException, SuspensaoNaoExisteException, AlunoComSuspensaoJaAtivadaNessaDisciplinaException
from core.exceptions.usuario_exceptions import AlunoInvalidoException
from core.exceptions.disciplina_exceptions import CodigoDisciplinaInvalidoException
from core.repositories.suspensao_repository import SuspensaoRepository
from core.services.aluno_service import AlunoService
from core.services.usuario_service import UsuarioService
from core.services.admin_service import AdminService
from core.services.disciplina_service import DisciplinaService
from django.utils import timezone

class SuspensaoService:
    
    #Verificação se Aluno existe ou disciplina existe feita em admin
    #Verificação da corretude dos dados em admin
    @staticmethod
    def criarSuspensao(dataFim, motivo, aluno, disciplina):
        
        hoje = timezone.now().date()
        suspensoes = SuspensaoService.getSuspensoesAlunoDisciplina(aluno, disciplina)
        
        for s in suspensoes:
            if s.data_fim >= hoje: raise AlunoComSuspensaoJaAtivadaNessaDisciplinaException()
            
        return SuspensaoRepository.criarSuspensao(
            aluno = aluno,
            disciplina = disciplina,
            data_fim = dataFim,
            motivo = motivo
        )
        
    @staticmethod
    def removerSuspensaoId(id):
        suspensao = SuspensaoService.getSuspensaoId(id)
        if not suspensao: raise SuspensaoNaoExisteException()
        suspensao.delete()
    
    @staticmethod
    def removerSuspensoesMatricula(matricula):
        suspensoes = SuspensaoService.getSuspensoesAluno(matricula)
        
        for s in suspensoes:
            s.delete()
    
    @staticmethod
    def removerSuspensoesMatriculaDisciplina(matricula, codDisciplina):
        suspensoes = SuspensaoService.getSuspensoesAlunoDisciplina(matricula, codDisciplina)
        
        for s in suspensoes:
            s.delete()
        
    @staticmethod
    def getSuspensaoId(id):
        return SuspensaoRepository.getSuspensaoId(id)
        
    @staticmethod
    def getSuspensoesAluno(matricula):
        
        aluno = AlunoService.getAluno(matricula)
        if not aluno: raise AlunoInvalidoException()
        
        return SuspensaoRepository.getSuspensoesMatricula(matricula)
    
    @staticmethod
    def getSuspensoesDisciplina(codigo):
        disciplina = DisciplinaService.get_Disciplina(codigo)
        if not disciplina: raise CodigoDisciplinaInvalidoException()
        
        return SuspensaoRepository.getSuspensoesDisciplina(codigo)
    
    @staticmethod
    def getSuspensoesAlunoDisciplina(matricula, codigo):
        
        aluno = AlunoService.getAluno(matricula)
        if not aluno: raise AlunoInvalidoException()
        
        disciplina = DisciplinaService.get_Disciplina(codigo)
        if not disciplina: raise CodigoDisciplinaInvalidoException()
        
        return SuspensaoRepository.getSuspensoesMatriculaDisciplina(matricula, codigo)
    