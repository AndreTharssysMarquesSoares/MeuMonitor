class SuspensaoNaoExisteException(Exception):
    def __init__(self, mensagem="Suspensao Não Existe"):
        super().__init__(mensagem)
        
class SuspensaoComDadosInvalidosException(Exception):
    def __init__(self, mensagem = "Dados Invalidos na Suspensao"):
        super().__init__(mensagem)
    
class AlunoComSuspensaoJaAtivadaNessaDisciplinaException(Exception):
    def __init__(self, mensagem = "Aluno ja possui suspensao ativa nessa disciplina"):
        super().__init__(mensagem)