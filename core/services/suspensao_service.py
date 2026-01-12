from core.exceptions.suspensao_exceptions import SuspensaoComDadosInvalidosException, SuspensaoNaoExisteException, AlunoComSuspensaoJaAtivadaNessaDisciplinaException
from core.exceptions.usuario_exceptions import AlunoInvalidoException
from core.exceptions.disciplina_exceptions import CodigoDisciplinaInvalidoException
from core.repositories.suspensao_repository import SuspensaoRepository
from core.services.aluno_service import AlunoService
from core.services.usuario_service import UsuarioService
from core.services.admin_service import AdminService
from core.services.disciplina_service import DisciplinaService

class SuspensaoService:
    
    #Verificação se Aluno existe ou disciplina existe feita em admin
    @staticmethod
    def criarSuspensao(dataFim, motivo, aluno, disciplina):
        
    @staticmethod
    def removerSuspensaoId(id):
    
    @staticmethod
    def removerSuspensaoMatricula(matricula):
        
    @staticmethod
    def removerSuspensaoMatriculaDisciplina(matricula, codDisciplina):
        
    @staticmethod
    def getSuspensaoId(id):
        
    @staticmethod
    def getSuspensoesAluno(matricula):
    
    @staticmethod
    def getSuspensoesDisciplina(codigo):
    
    @staticmethod
    def getSuspensoesAlunoDisciplina(matricula, codigo):
    