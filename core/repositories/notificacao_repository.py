from core.models import Notificacao
from django.db.models import QuerySet

class NotificacaoRepository:
    
    @staticmethod
    def notificar(**data):
        return Notificacao.objects.create(**data)
    
    @staticmethod
    def salvar(notificacao):
        Notificacao.save()
    
    @staticmethod
    def getNotificacao(id):
        return Notificacao.objects.filter(id=id).first()
    
    @staticmethod
    def getNotificacoesAluno(matricula) -> QuerySet[Notificacao]:
        if isinstance(matricula, str):
            return Notificacao.objects.filter(destinatario__username=matricula)
        else:
            return Notificacao.objects.filter(destinatario=matricula)