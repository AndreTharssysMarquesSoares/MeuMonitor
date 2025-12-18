from core.repositories.usuario_repository import UsuarioRepository
from core.services.usuario_service import UsuarioService
from core.services.aluno_service import AlunoService 
from core.services.disciplina_service import DisciplinaService
from core.exceptions.usuario_exceptions import AlunoNaoCadastradoException, SenhaIncorretaException, SenhaFracaException, DadosInvalidoException, AdminJaCadastradoException, UserNameInvalidoException, AdminInvalidoException, UsernameAdminNaoExisteException, AlunoJaDesativadoException, MonitorJaCadastradoException, MonitorNaoCadastradoException, AlunoJaAtivadoException
from core.exceptions.disciplina_exceptions import DisciplinaJaCadastradaException, CodigoDisciplinaInvalidoException
from core.repositories.disciplina_repository import DisciplinaRepository

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
    
    @staticmethod
    def buscarDisciplinaValida(codigo):
        if not DisciplinaService.exist_DisciplinaValida(codigo):
            raise CodigoDisciplinaInvalidoException("Disciplina não encontrada na base oficial da UFCG.")
        
        return DisciplinaService.get_disciplinaValida(codigo)

    @staticmethod
    def criarDisciplinaWeb(codigo):
        if DisciplinaService.exist_Disciplina(codigo): 
            raise DisciplinaJaCadastradaException()
            
        disciplina_valida = DisciplinaService.get_disciplinaValida(codigo)
        
        return DisciplinaRepository.criar_disciplina(
            codigo=codigo,
            nome=disciplina_valida.nome
        )

    @staticmethod
    def deletarDisciplinaWeb(codigo):
        from core.models import Disciplina
        Disciplina.objects.filter(codigo=codigo).delete()

    @staticmethod
    def criarMonitorWeb(matricula_aluno, codigo_disciplina):
        aluno = AlunoService.getAluno(matricula=matricula_aluno)
        disciplina = DisciplinaService.get_Disciplina(codigo=codigo_disciplina)
        
        if aluno.monitor_de is not None: 
            raise MonitorJaCadastradoException()
            
        aluno.monitor_de = disciplina
        UsuarioRepository.salvar(aluno)

        if not aluno.interesses.filter(codigo=disciplina.codigo).exists():
            aluno.interesses.add(disciplina)
            
        return aluno

    @staticmethod
    def removerMonitorWeb(matricula_aluno):
        aluno = AlunoService.getAluno(matricula=matricula_aluno)
        
        if aluno.monitor_de is None: 
            raise MonitorNaoCadastradoException()
        
        disciplina_alvo = aluno.monitor_de
        aluno.monitor_de = None

        if aluno.interesses.filter(id=disciplina_alvo.id).exists():
            aluno.interesses.remove(disciplina_alvo)

        UsuarioRepository.salvar(aluno)
        return aluno

    @staticmethod
    def getTodosMonitoresWeb():
        return UsuarioRepository.get_monitores()