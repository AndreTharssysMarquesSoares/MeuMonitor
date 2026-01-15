from core.exceptions.suspensao_exceptions import SuspensaoComDadosInvalidosException, SuspensaoNaoExisteException, AlunoComSuspensaoJaAtivadaNessaDisciplinaException
from core.exceptions.usuario_exceptions import AlunoInvalidoException
from core.exceptions.disciplina_exceptions import CodigoDisciplinaInvalidoException
from core.repositories.suspensao_repository import SuspensaoRepository
from core.services.aluno_service import AlunoService
from core.services.usuario_service import UsuarioService
from core.services.disciplina_service import DisciplinaService
from django.utils import timezone

class SuspensaoService:
    
    @staticmethod
    def criarSuspensao(dataFim, motivo, aluno, disciplina):
        
        from core.models import Usuario, Disciplina
        
        if isinstance(aluno, str):
            aluno = AlunoService.getAluno(aluno)
        if isinstance(disciplina, str):
            disciplina = DisciplinaService.get_Disciplina(disciplina)

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
        
        from core.models import Usuario, Disciplina
        
        if isinstance(matricula, str):
            aluno = AlunoService.getAluno(matricula)
        else:
            aluno = matricula
            
        if isinstance(codigo, str):
            disciplina = DisciplinaService.get_Disciplina(codigo)
        else:
            disciplina = codigo
        
        return SuspensaoRepository.getSuspensoesMatriculaDisciplina(aluno, disciplina)
    
    @staticmethod
    def verificarSuspensaoAtiva(matricula, codigo_disciplina):
        """
        Verifica se um aluno está suspenso em uma disciplina.
        Retorna True se estiver suspenso, False caso contrário.
        """
        from core.models import Suspensao
        
        hoje = timezone.now().date()
        
        # Se for string, buscar objetos
        if isinstance(matricula, str):
            aluno = AlunoService.getAluno(matricula)
        else:
            aluno = matricula
            
        if isinstance(codigo_disciplina, str):
            disciplina = DisciplinaService.get_Disciplina(codigo_disciplina)
        else:
            disciplina = codigo_disciplina
        
        return Suspensao.objects.filter(
            aluno=aluno,
            disciplina=disciplina,
            data_inicio__lte=hoje,
            data_fim__gte=hoje
        ).exists()
    
    @staticmethod
    def getSuspensaoAtiva(matricula, codigo_disciplina):
        """
        Retorna a suspensão ativa de um aluno em uma disciplina, se existir.
        """
        from core.models import Suspensao
        
        hoje = timezone.now().date()
        
        if isinstance(matricula, str):
            aluno = AlunoService.getAluno(matricula)
        else:
            aluno = matricula
            
        if isinstance(codigo_disciplina, str):
            disciplina = DisciplinaService.get_Disciplina(codigo_disciplina)
        else:
            disciplina = codigo_disciplina
        
        return Suspensao.objects.filter(
            aluno=aluno,
            disciplina=disciplina,
            data_inicio__lte=hoje,
            data_fim__gte=hoje
        ).first()
    