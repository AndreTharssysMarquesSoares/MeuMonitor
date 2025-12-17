from core.repositories.usuario_repository import UsuarioRepository
from core.services.usuario_service import UsuarioService
from core.services.disciplina_service import DisciplinaService
from core.exceptions.usuario_exceptions import MatriculaInvalidaException, AlunoNaoCadastradoException, SenhaFracaException, AlunoJaCadastradoException, DadosInvalidoException, SenhaIncorretaException, AlunoInvalidoException, AlunoJaInteressadoException, AlunoNaoInteressadoException

class AlunoService:
    
    @staticmethod
    def cadastrarAluno(**payload):
        
        """
        Payload esperando:
        - email
        - matricula
        - password
        """
        
        matricula = payload.get('matricula')
        senha = payload.get('senha')
        
        aluno = AlunoService.getAlunoValido(matricula=matricula)
        
        if not aluno: raise MatriculaInvalidaException()
        if UsuarioRepository.exist_aluno(matricula=matricula): raise AlunoJaCadastradoException()
        if not UsuarioService.auth_password_validators(senha): raise SenhaFracaException()
        if payload.get('email') == "": raise DadosInvalidoException()
        
        nome_aluno = aluno.nome_completo.split(' ')
    
        user = UsuarioRepository.criar_usuario(
            username=matricula,
            password=senha,
            first_name= nome_aluno[0],
            last_name=nome_aluno[-1],
            email=payload.get("email"),
            matricula=matricula,
            tipo="ALUNO",
            is_superuser=False,
            is_staff=False,
            is_active=True
        )
        
        return user
    
    @staticmethod
    def alterarAluno(matricula, senha_atual, **payload):
        """
        payload opcional:
        - email
        - nova_senha
        """
        aluno = UsuarioRepository.get_aluno(matricula=matricula)
        if not aluno: raise AlunoNaoCadastradoException()

        if not UsuarioService.validarSenha(aluno, senha_atual): raise SenhaIncorretaException()

        email = payload.get("email")
        if email is not None:
            if email == "":
                raise DadosInvalidoException()
            aluno.email = email

        nova_senha = payload.get("nova_senha")
        if nova_senha:
            if not UsuarioService.auth_password_validators(nova_senha): raise SenhaFracaException()
            aluno.set_password(nova_senha)

        UsuarioRepository.salvar(aluno)

        return aluno

    @staticmethod
    def addInteresseDisciplina(matricula, senha, codigo):
        if not AlunoService.validarAcessoAluno(matricula=matricula, senha= senha): raise AlunoInvalidoException()
        
        aluno = AlunoService.getAluno(matricula=matricula)
        disciplina = DisciplinaService.get_Disciplina(codigo=codigo)
        
        if aluno.interesses.filter(id = disciplina.codigo).exist(): raise AlunoJaInteressadoException()
        
        aluno.interesses.add(disciplina)
        
    @staticmethod
    def removeInteresseDisciplina(matricula, senha, codigo):
        if not AlunoService.validarAcessoAluno(matricula=matricula, senha= senha): raise AlunoInvalidoException()
        
        aluno = AlunoService.getAluno(matricula=matricula)
        disciplina = DisciplinaService.get_Disciplina(codigo=codigo)
        
        if not aluno.interesses.filter(id = disciplina.codigo).exist(): raise AlunoNaoInteressadoException()
        
        aluno.interesses.remove(disciplina)
    
    @staticmethod
    def getInteresseAluno(matricula, senha):
        if not AlunoService.validarAcessoAluno(matricula=matricula, senha= senha): raise AlunoInvalidoException()
        aluno = AlunoService.getAluno(matricula=matricula)
        return aluno.interesses.all()
    
    @staticmethod
    def getMonitoresDisciplina(disciplina):
        return UsuarioRepository.get_monitores_disciplina(disciplina=disciplina)
    
    @staticmethod
    def getAlunoValido(matricula):
        aluno_valido = UsuarioRepository.get_aluno_valido(matricula=matricula)
        
        if not aluno_valido: raise MatriculaInvalidaException()
        
        return aluno_valido
        
    @staticmethod
    def getAluno(matricula):
        
        aluno = UsuarioRepository.get_aluno(matricula=matricula)
        
        if not aluno: raise AlunoNaoCadastradoException()
        
        return aluno
    
    @staticmethod
    def validarAcessoAluno(matricula, senha) -> bool: 
        aluno = UsuarioRepository.get_aluno(matricula=matricula)
        if not aluno: raise AlunoNaoCadastradoException()
        if not aluno.check_password(senha): raise SenhaIncorretaException()
        return True