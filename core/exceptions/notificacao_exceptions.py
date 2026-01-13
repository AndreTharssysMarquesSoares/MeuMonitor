class TipoNotificaoInvalidaException(Exception):
    def __init__(self, mensagem="Tipo inválido"):
        super().__init__(mensagem)
        
class NotificacaoInvalidaException(Exception):
    def __init__(self, mensagem="Dados Invalidos na Notificacao"):
        super().__init__(mensagem)
        
class NotificaoNaoExisteException(Exception):
    def __init__(self, mensagem="Notificação não existe"):
        super().__init__(mensagem)