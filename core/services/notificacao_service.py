from core.models import Usuario
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

        tipo_map = {
            'Fórum': 'FORUM',
            'Sistema': 'SISTEMA', 
            'Administração': 'ADMIN'
        }
        tipo_db = tipo_map.get(tipo.value, 'FORUM')

        notificacao = NotificacaoRepository.notificar(
            tipo = tipo_db,
            titulo = titulo,
            texto = texto,
            destinatario = destinatario,
            mensagem_forum = mensagem_forum,
        )

        return notificacao
    
    @staticmethod
    def marcarNotificacaoETopicoComoLidos(notificacao_id, usuario):
        """
        Marca como lida a notificação E todas as outras do mesmo tópico.
        """
        from core.models import Notificacao, MensagemForum
        
        try:
            notificacao = Notificacao.objects.get(id=notificacao_id, destinatario=usuario)
        except Notificacao.DoesNotExist:
            return None

        if notificacao.mensagem_forum:
            topico_raiz = notificacao.mensagem_forum
            while topico_raiz.resposta_para is not None:
                topico_raiz = topico_raiz.resposta_para

            def coletar_ids(mensagem):
                ids = [mensagem.id]
                for resp in MensagemForum.objects.filter(resposta_para=mensagem):
                    ids.extend(coletar_ids(resp))
                return ids
            
            ids_do_topico = coletar_ids(topico_raiz)
            Notificacao.objects.filter(
                destinatario=usuario,
                mensagem_forum_id__in=ids_do_topico,
                lida=False
            ).update(lida=True)
        else:
            notificacao.lida = True
            notificacao.save()
        
        return True
    
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
    
    @staticmethod
    def getContextoNotificacoesAgrupadas(user):

        try: 
            qs = NotificacaoService.getNotificacoesAluno(user)
            nao_lidas_total = qs.filter(lida=False).count()
            notificacoes_agrupadas = {}
            
            for notif in qs.order_by('-data_criacao'):
                if notif.mensagem_forum:
                    topico_raiz = notif.mensagem_forum
                    while topico_raiz.resposta_para is not None:
                        topico_raiz = topico_raiz.resposta_para
                    
                    topico_id = topico_raiz.id
                    
                    if topico_id not in notificacoes_agrupadas:
                        notificacoes_agrupadas[topico_id] = {
                            'topico': topico_raiz,
                            'disciplina': topico_raiz.disciplina,
                            'titulo': topico_raiz.titulo,
                            'ultima_notificacao': notif,
                            'nao_lidas': 0,
                            'total': 0
                        }
                    
                    notificacoes_agrupadas[topico_id]['total'] += 1
                    if not notif.lida:
                        notificacoes_agrupadas[topico_id]['nao_lidas'] += 1
                else:
                    notif_id = f"other_{notif.id}"
                    notificacoes_agrupadas[notif_id] = {
                        'topico': None,
                        'disciplina': None,
                        'titulo': notif.titulo,
                        'ultima_notificacao': notif,
                        'nao_lidas': 1 if not notif.lida else 0,
                        'total': 1
                    }
        
            notificacoes_lista = sorted(
                notificacoes_agrupadas.values(),
                key=lambda x: x['ultima_notificacao'].data_criacao,
                reverse=True
            )[:10]
            
        except Exception as e:
            print(f"[ERRO] get_notificacoes_context: {e}")
            notificacoes_lista = []
            nao_lidas_total = 0
        
        return {
            'notificacoes': notificacoes_lista,
            'notificacoes_nao_lidas': nao_lidas_total
        }
    
    @staticmethod
    def enviarComunicadoGeral(titulo, mensagem, remetente):
        """
        Envia uma notificação para TODOS os usuários do sistema.
        """
        from core.models import Notificacao
        
        todos_usuarios = Usuario.objects.filter(is_active=True)
        
        notificacoes_criadas = []
        for usuario in todos_usuarios:
            if usuario.id != remetente.id:
                notif = Notificacao.objects.create(
                    destinatario=usuario,
                    tipo='ADMIN',
                    titulo=titulo,
                    texto=mensagem
                )
                notificacoes_criadas.append(notif)
        
        return notificacoes_criadas