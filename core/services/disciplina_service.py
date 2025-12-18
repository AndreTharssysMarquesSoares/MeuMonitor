from core.repositories.disciplina_repository import DisciplinaRepository
from core.exceptions.disciplina_exceptions import DisciplinaJaCadastradaException, CodigoDisciplinaInvalidoException

class DisciplinaService:
    
    @staticmethod
    def cadastrarDisciplina(codigo):
        if DisciplinaService.exist_Disciplina(codigo=codigo): raise DisciplinaJaCadastradaException()
        disciplinaValida = DisciplinaRepository.get_disciplinaValida(codigo=codigo)
        if not disciplinaValida: raise CodigoDisciplinaInvalidoException()
        disciplina = DisciplinaRepository.criar_disciplina(
            codigo = codigo,
            nome = disciplinaValida.nome
        )
        
        return disciplina

    @staticmethod
    def exist_Disciplina(codigo) -> bool:
        return DisciplinaRepository.exist_disciplina(codigo=codigo)
    
    @staticmethod
    def exist_DisciplinaValida(codigo) -> bool:
        return DisciplinaRepository.exist_disciplinaValida(codigo=codigo)
    
    @staticmethod
    def get_Disciplina(codigo):
        if not DisciplinaService.exist_Disciplina(codigo=codigo): raise CodigoDisciplinaInvalidoException()
        return DisciplinaRepository.get_disciplina(codigo=codigo)

    @staticmethod
    def get_disciplinaValida(codigo):
        if not DisciplinaService.exist_DisciplinaValida(codigo=codigo): raise CodigoDisciplinaInvalidoException()
        return DisciplinaRepository.get_disciplinaValida(codigo=codigo)
    
    @staticmethod
    def get_alunosInteressados(codigo):
        disciplina = DisciplinaService.get_Disciplina(codigo=codigo)
        return disciplina.alunos_interessados.all()
    
    @staticmethod
    def get_monitores(codigo):
        from core.services.aluno_service import AlunoService
        disciplina = DisciplinaService.get_Disciplina(codigo=codigo)
        return AlunoService.getMonitoresDisciplina(disciplina)
        
    @staticmethod
    def get_todas_disciplinas():
        return DisciplinaRepository.get_todas_disciplinas()