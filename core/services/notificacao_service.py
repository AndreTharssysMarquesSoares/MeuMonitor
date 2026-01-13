from core.repositories.notificacao_repository import NotificacaoRepository
from enum import Enum
from core.exceptions.notificacao_exceptions import TipoNotificaoInvalidaException, NotificacaoInvalidaException, NotificaoNaoExisteException

class TipoNotificacao(Enum):
    FORUM = 'Fórum'
    SISTEMA = 'Sistema'
    ADMIN = 'Administração'
    
class NotificacaoService:
    
    @staticmethod
    def gerarNotificacao(tipo, titulo, texto, destinatario, mensagem_forum=None):

        if not isinstance(tipo, TipoNotificacao):
            raise TipoNotificaoInvalidaException()

        if tipo == TipoNotificacao.FORUM:
            if mensagem_forum is None:
                raise NotificacaoInvalidaException()
        else:
            if mensagem_forum is not None:
                raise NotificacaoInvalidaException()
            
        if texto is None or titulo == "" or texto == "": raise NotificacaoInvalidaException()
            
        notificacao = NotificacaoRepository.notificar(
            tipo = tipo,
            titulo = titulo,
            texto = texto,
            destinatario = destinatario,
            mensagem_forum = mensagem_forum,
        )
        
        return notificacao
    
    @staticmethod
    def getNotificacao(id):
        return NotificacaoRepository.getNotificacao(id)
    
    @staticmethod
    def getNotificacoesAluno(matricula):
        return NotificacaoRepository.getNotificacoesAluno(matricula)
    
    @staticmethod
    def marcarLida(id):
        notificacao = NotificacaoService.getNotificacao(id)
        if not notificacao: raise NotificaoNaoExisteException()
        notificacao.lida = True
        NotificacaoRepository.salvar(notificacao)
        return True