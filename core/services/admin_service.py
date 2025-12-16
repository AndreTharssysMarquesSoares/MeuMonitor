from core.repositories.usuario_repository import UsuarioRepository
from core.services.usuario_service import UsuarioService
from core.services.aluno_service import AlunoService 
from core.services.disciplina_service import DisciplinaService
from core.exceptions.usuario_exceptions import AlunoNaoCadastradoException, SenhaIncorretaException, SenhaFracaException, DadosInvalidoException, AdminJaCadastradoException, UserNameInvalidoException, AdminInvalidoException, UsernameAdminNaoExisteException, AlunoJaDesativadoException, MonitorJaCadastradoException, MonitorNaoCadastradoException, AlunoJaAtivadoException

class AdminService:
    
    @staticmethod
    def cadastrarAdmin(**payload):
        
        """
        Payload esperando:
        - nome completo
        - username
        - email
        - password
        """
        senha = payload.get('senha')
        username = payload.get('username')
        nome = payload.get('nome_completo')
        
        if UsuarioRepository.exist_admin(username=username): raise AdminJaCadastradoException()
        if not UsuarioService.username_valido(username): raise UserNameInvalidoException()
        if not UsuarioService.auth_password_validators(senha): raise SenhaFracaException()
        if payload.get('email') == "" or nome == "": raise DadosInvalidoException()
        
        nome = nome.split(" ")
        
        usuario = UsuarioRepository.criar_usuario(
            username=username,
            password=senha,
            first_name= nome[0],
            last_name=nome[-1],
            email=payload.get("email"),
            matricula=username,
            tipo="ADMIN",
            is_superuser=True,
            is_staff=False,
            is_active=True
        )
        
        return usuario
    
    @staticmethod
    def alterarAdmin(username, senha_atual, **payload):
        """
        payload opcional:
        - email
        - nova_senha
        """
        admin = UsuarioRepository.get_admin(username=username)
        if not admin: raise AdminInvalidoException()
        if not UsuarioService.validarSenha(admin, senha_atual): raise SenhaIncorretaException()

        email = payload.get("email")
        if email:
            admin.email = email

        nova_senha = payload.get("nova_senha")
        if nova_senha:
            if not UsuarioService.auth_password_validators(nova_senha): raise SenhaFracaException()
            admin.set_password(nova_senha)

        UsuarioRepository.salvar(admin)

        return admin

    @staticmethod
    def validarAcessoAdmin(username, senha) -> bool: 
        admin = UsuarioRepository.get_admin(username=username)
        if not admin: raise UsernameAdminNaoExisteException()
        if not admin.check_password(senha): raise SenhaIncorretaException()
        return True
    
    @staticmethod
    def desativarAluno(username, senha, matricula):
        if not AdminService.validarAcessoAdmin(username, senha): raise AdminInvalidoException()
        aluno = AlunoService.getAluno(matricula=matricula)
        if not aluno.is_active: raise AlunoJaDesativadoException()
        aluno.is_active = False
        UsuarioRepository.salvar(aluno)
        return aluno
    
    @staticmethod
    def ativarAluno(username, senha, matricula):
        if not AdminService.validarAcessoAdmin(username, senha): raise AdminInvalidoException()
        aluno = AlunoService.getAluno(matricula=matricula)
        if aluno.is_active: raise AlunoJaAtivadoException()
        aluno.is_active = True
        UsuarioRepository.salvar(aluno)
        return aluno
    
    @staticmethod
    def criarMonitor(username, senha, matricula, codigoDisciplina):
        if not AdminService.validarAcessoAdmin(username=username, senha=senha): raise AdminInvalidoException()
        aluno = AlunoService.getAluno(matricula=matricula)
        if not aluno: raise AlunoNaoCadastradoException()
        disciplina = DisciplinaService.get_Disciplina(codigo=codigoDisciplina)
        if aluno.monitor_de is not None: raise MonitorJaCadastradoException()
        aluno.monitor_de = disciplina.codigo
        UsuarioRepository.salvar(aluno)
        return aluno
    
    @staticmethod
    def removerMonitor(username, senha, matricula):
        if not AdminService.validarAcessoAdmin(username=username, senha=senha): raise AdminInvalidoException()
        aluno = AlunoService.getAluno(matricula=matricula)
        if not aluno: raise AlunoNaoCadastradoException()
        if aluno.monitor_de is None: raise MonitorNaoCadastradoException()
        aluno.monitor_de = None
        UsuarioRepository.salvar(aluno)
        return aluno
    
    @staticmethod
    def criarDisciplina(username, senha, codigo):
        if not AdminService.validarAcessoAdmin(username=username, senha=senha): raise AdminInvalidoException()
        disciplina = DisciplinaService.cadastrarDisciplina(codigo=codigo)
        return disciplina
    
    @staticmethod
    def getMonitores(username, senha):
        if not AdminService.validarAcessoAdmin(username=username, senha = senha): raise AdminInvalidoException()
        return UsuarioRepository.get_monitores()
    
    @staticmethod
    def getNaoMonitores(username, senha):
        if not AdminService.validarAcessoAdmin(username=username, senha = senha): raise AdminInvalidoException()
        return UsuarioRepository.get_nao_monitores()