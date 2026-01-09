from core.models import MensagemForum

class MensagemForumRepository:
    
    @staticmethod
    def criarMensagem(**data):
        return MensagemForum.objects.create(**data)
        
    @staticmethod
    def removerMensagem(id):
        MensagemForum.objects.filter(id=id).delete()
        
    @staticmethod
    def salvar(mensagem):
        MensagemForum.save(mensagem)
        return mensagem
    
    @staticmethod
    def getMensagem(id):
        return MensagemForum.objects.filter(id=id).first()
        
    @staticmethod
    def getMensagensDeAutor(autor):
        return MensagemForum.objects.filter(autor=autor)
    
    @staticmethod
    def getTopicosDaDisciplina(disciplina):
        return MensagemForum.objects.filter(disciplina=disciplina, resposta_para__isnull=True).order_by('data_envio')
    
    @staticmethod
    def getRespostas(id):
        return MensagemForum.objects.filter(resposta_para_id=id).order_by('data_envio')

    @staticmethod
    def getAutor(id):
        mensagem =  MensagemForum.objects.filter(id=id).first()
        return mensagem.autor  
    
    @staticmethod
    def getTitulo(id):
        mensagem =  MensagemForum.objects.filter(id=id).first()
        return mensagem.titulo
    
    @staticmethod
    def getTexto(id):
        mensagem =  MensagemForum.objects.filter(id=id).first()
        return mensagem.texto    
        