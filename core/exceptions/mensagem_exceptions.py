class DadosInválidosException(Exception):
    def __init__(self, mensagem="Dados Inválidos"):
        super().__init__(mensagem)
        
class MensagemNaoEncontradaException(Exception):
    def __init__(self, mensagem="Mensagem Não Encontrada"):
        super().__init__(mensagem)
        
class TopicosAindaNaoCadastradosException(Exception):
    def __init__(self, mensagem="Topicos ainda não cadastrados"):
        super().__init__(mensagem)
        
class NenhumaRespostaEncontradaException(Exception):
    def __init__(self, mensagem="Nenhuma Resposta cadastrada"):
        super().__init__(mensagem)
        
class AlunoSuspensoNesseForumException(Exception):
    def __init__(self, mensagem="Aluno esta suspenso nesse Forum"):
        super().__init__(mensagem)