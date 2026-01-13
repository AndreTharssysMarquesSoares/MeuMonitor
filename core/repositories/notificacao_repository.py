from core.models import Notificacao
from django.db.models import QuerySet

class NotificacaoRepository:
    
    @staticmethod
    def notificar(**data):
        return Notificacao.objects.create(**data)
    
    @staticmethod
    def salvar(notificacao):
        Notificacao.save(notificacao)
    
    @staticmethod
    def getNotificacao(id):
        return Notificacao.objects.filter(id=id).first()
    
    @staticmethod
    def getNotificacoesAluno(matricula) -> QuerySet[Notificacao]:
        return Notificacao.objects.filter(destinatario=matricula)