class MatriculaInvalidaException(Exception):
    def __init__(self, mensagem="Matrícula inválida"):
        super().__init__(mensagem)
        
class AlunoNaoCadastradoException(Exception):
    def __init__(self, mensagem="Aluno não cadastrado"):
        super().__init__(mensagem)
        
class SenhaIncorretaException(Exception):
    def __init__(self, mensagem="Senha Incorreta"):
        super().__init__(mensagem)
        
class UsuarioNaoExisteException(Exception):
    def __init__(self, mensagem="Usuario não existe!"):
        super().__init__(mensagem)
        
class SenhaFracaException(Exception):
    def __init__(self, mensagem="Senha fraca"):
        super().__init__(mensagem)
        
class AlunoJaCadastradoException(Exception):
    def __init__(self, mensagem="Aluno já possui cadastro, entre com a senha"):
        super().__init__(mensagem)
        
class DadosInvalidoException(Exception):
    def __init__(self, mensagem="Dados invalidos"):
        super().__init__(mensagem)
        
class AdminJaCadastradoException(Exception):
    def __init__(self, mensagem="Administrador já possui cadastro, entre com a senha"):
        super().__init__(mensagem)
        
class UserNameInvalidoException(Exception):
    def __init__(self, mensagem="User name inváildo(com espaços em branco ou None)"):
        super().__init__(mensagem)
        
class AdminInvalidoException(Exception):
    def __init__(self, mensagem="Admin inválido"):
        super().__init__(mensagem)
        
class UsernameAdminNaoExisteException(Exception):
    def __init__(self, mensagem="Admin não existe"):
        super().__init__(mensagem)
    
class AlunoJaDesativadoException(Exception):
    def __init__(self, mensagem="Aluno já foi desativado"):
        super().__init__(mensagem)
        
class MonitorJaCadastradoException(Exception):
    def __init__(self, mensagem="Monitor Já Cadastrado"):
        super().__init__(mensagem)
        
class MonitorNaoCadastradoException(Exception):
    def __init__(self, mensagem="Monitor não cadastrado"):
        super().__init__(mensagem)
        
class AlunoInvalidoException(Exception):
    def __init__(self, mensagem="Aluno inválido"):
        super().__init__(mensagem)
        
class AlunoJaInteressadoException(Exception):
    def __init__(self, mensagem="Aluno com interesse ja cadastrado"):
        super().__init__(mensagem)
        
class AlunoNaoInteressadoException(Exception):
    def __init__(self, mensagem="Aluno com interesse nao cadastrado"):
        super().__init__(mensagem)

class AlunoJaAtivadoException(Exception):
    def __init__(self, mensagem="Aluno ja ativado"):
        super().__init__(mensagem)