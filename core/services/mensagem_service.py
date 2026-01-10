from core.repositories.mensagem_repository import MensagemForumRepository
from core.services.admin_service import AdminService
from core.services.aluno_service import AlunoService
from core.services.usuario_service import UsuarioService
from core.services.disciplina_service import DisciplinaService
from core.exceptions.usuario_exceptions import SenhaIncorretaException 
from core.exceptions.mensagem_exceptions import DadosInválidosException, MensagemNaoEncontradaException, TopicosAindaNaoCadastradosException, NenhumaRespostaEncontradaException

class MensagemForumService:
    
    @staticmethod
    def criarTopicoAdmin(username, senha, titulo, texto, codigoDisciplina):
        
        admin = AdminService.getAdmin(username)
        disciplina = DisciplinaService.get_Disciplina(codigoDisciplina)
        
        if not UsuarioService.validarSenha(admin, senha): raise SenhaIncorretaException()
        
        if titulo is None or texto is None or codigoDisciplina is None or titulo == "" or texto == "" or codigoDisciplina == "": raise DadosInválidosException()
        
        topico = MensagemForumRepository.criarMensagem(
            titulo = titulo,
            texto = texto,
            autor = admin.username,
            disciplina = disciplina.codigo,
            resposta_para = None
        )
        
        return topico
        
    @staticmethod
    def criarMensagemAdmin(username, senha, texto, codigoDisciplina, idMensagemRespondida):
        
        admin = AdminService.getAdmin(username)
        disciplina = DisciplinaService.get_Disciplina(codigoDisciplina)
        
        if not UsuarioService.validarSenha(admin, senha): raise SenhaIncorretaException()
        
        if idMensagemRespondida is None or texto is None or codigoDisciplina is None or idMensagemRespondida == "" or texto == "" or codigoDisciplina == "": raise DadosInválidosException()
        
        mensagemPai = MensagemForumRepository.getMensagem(idMensagemRespondida)
        
        if not mensagemPai: raise MensagemNaoEncontradaException()
        
        mensagem = MensagemForumRepository.criarMensagem(
            titulo = None,
            texto = texto,
            autor = admin.username,
            disciplina = disciplina.codigo,
            resposta_para = idMensagemRespondida
        )
        
        return mensagem
        
    @staticmethod
    def criarTopicoAluno(matricula, senha, titulo, texto, codigoDisciplina):
        
        aluno = AlunoService.getAluno(matricula)
        disciplina = DisciplinaService.get_Disciplina(codigoDisciplina)
        
        if not UsuarioService.validarSenha(aluno, senha): raise SenhaIncorretaException()
        
        if titulo is None or texto is None or codigoDisciplina is None or titulo == "" or texto == "" or codigoDisciplina == "": raise DadosInválidosException()
        
        topico = MensagemForumRepository.criarMensagem(
            titulo = titulo,
            texto = texto,
            autor = aluno.matricula,
            disciplina = disciplina.codigo,
            resposta_para = None
        )
        
        return topico
        
    @staticmethod
    def criarMensagemAluno(matricula, senha, texto, codigoDisciplina, idMensagemRespondida):
        
        aluno = AlunoService.getAluno(matricula)
        disciplina = DisciplinaService.get_Disciplina(codigoDisciplina)
        
        if not UsuarioService.validarSenha(aluno, senha): raise SenhaIncorretaException()
        
        if idMensagemRespondida is None or texto is None or codigoDisciplina is None or idMensagemRespondida == "" or texto == "" or codigoDisciplina == "": raise DadosInválidosException()
        
        mensagemPai = MensagemForumRepository.getMensagem(idMensagemRespondida)
        
        if not mensagemPai: raise MensagemNaoEncontradaException()
        
        mensagem = MensagemForumRepository.criarMensagem(
            titulo = None,
            texto = texto,
            autor = aluno.matricula,
            disciplina = disciplina.codigo,
            resposta_para = idMensagemRespondida
        )
        
        return mensagem
        
    @staticmethod
    def removerMensagemAdmin(username, senha, id):
        
        admin = AdminService.getAdmin(username)
        
        if not UsuarioService.validarSenha(admin, senha): raise SenhaIncorretaException()
        
        mensagem = MensagemForumService.getMensagem(id)
        
        mensagem.delete()
        
        return True
        
    @staticmethod
    def removerMensagemAluno(matricula, senha, id):
        
        aluno =  AlunoService.getAluno(matricula)
        
        if not UsuarioService.validarSenha(aluno, senha): raise SenhaIncorretaException()
        
        mensagem = MensagemForumService.getMensagem(id)
        
        mensagem.delete()
        
        return True
        
    @staticmethod
    def getMensagem(id):
        mensagem = MensagemForumRepository.getMensagem(id)
        if not mensagem: raise MensagemNaoEncontradaException()
        return mensagem
        
    @staticmethod
    def getTopicosDaDisciplina(codigoDisciplina):
        disciplina = DisciplinaService.get_Disciplina(codigoDisciplina)
        mensagens = MensagemForumRepository.getTopicosDaDisciplina(disciplina.codigo)
        if not mensagens: raise TopicosAindaNaoCadastradosException()
        return mensagens
        
    @staticmethod
    def getRespostas(idMensagem):
        mensagens = MensagemForumRepository.getRespostas(idMensagem)
        if not mensagens: raise NenhumaRespostaEncontradaException()
        return mensagens
        
    @staticmethod
    def getAutor(idMensagem):
        mensagem = MensagemForumService.getMensagem(idMensagem)
        return mensagem.autor
