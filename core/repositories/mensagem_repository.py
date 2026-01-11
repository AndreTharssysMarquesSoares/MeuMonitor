from core.models import MensagemForum

class MensagemForumRepository:
    
    @staticmethod
    def criarMensagem(**data):
        """
        Cria uma mensagem. Aceita tanto o formato antigo quanto o novo.
        Formato antigo: autor (string), disciplina (codigo), resposta_para
        Formato novo: autor (objeto), disciplina (objeto), mensagem_pai
        """
        if 'mensagem_pai' in data:
            data['resposta_para'] = data.pop('mensagem_pai')
        
        return MensagemForum.objects.create(**data)
        
    @staticmethod
    def removerMensagem(id):
        MensagemForum.objects.filter(id=id).delete()
        
    @staticmethod
    def salvar(mensagem):
        mensagem.save()
        return mensagem
    
    @staticmethod
    def getMensagem(id):
        return MensagemForum.objects.filter(id=id).first()
        
    @staticmethod
    def getMensagensDeAutor(autor):
        return MensagemForum.objects.filter(autor=autor)
    
    @staticmethod
    def getTopicosDaDisciplina(disciplina):
        """
        Retorna tópicos (mensagens sem resposta_para) de uma disciplina.
        Aceita tanto código (string/int) quanto objeto Disciplina.
        """
        if hasattr(disciplina, 'codigo'):
            codigo = disciplina.codigo
        else:
            codigo = disciplina
            
        return MensagemForum.objects.filter(
            disciplina__codigo=codigo, 
            resposta_para__isnull=True
        ).order_by('-data_envio')
    
    @staticmethod
    def getRespostas(id):
        """Retorna todas as respostas de uma mensagem"""
        return MensagemForum.objects.filter(resposta_para_id=id).order_by('data_envio')

    @staticmethod
    def getAutor(id):
        mensagem = MensagemForum.objects.filter(id=id).first()
        return mensagem.autor if mensagem else None
    
    @staticmethod
    def getTitulo(id):
        mensagem = MensagemForum.objects.filter(id=id).first()
        return mensagem.titulo if mensagem else None
    
    @staticmethod
    def getTexto(id):
        mensagem = MensagemForum.objects.filter(id=id).first()
        return mensagem.texto if mensagem else None