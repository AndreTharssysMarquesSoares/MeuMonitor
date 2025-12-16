class DisciplinaJaCadastradaException(Exception):
    def __init__(self, mensagem="Disciplina Já Cadastrada"):
        super().__init__(mensagem)
        
class CodigoDisciplinaInvalidoException(Exception):
    def __init__(self, mensagem="Codigo Invalido"):
        super().__init__(mensagem)