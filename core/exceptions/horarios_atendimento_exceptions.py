class HorarioInvalidoException(Exception):
    def __init__(self, mensagem="Horário Inválido"):
        super().__init__(mensagem)
        
class HorariosSobrepostosException(Exception):
    def __init__(self, mensagem="Horários Sobrepostos"):
        super().__init__(mensagem)
        
        
class DiaSemanaInvalidoException(Exception):
    def __init__(self, mensagem="Dia da Semana escolhido Inválido"):
        super().__init__(mensagem)

class HorarioNaoExisteException(Exception):
    def __init__(self, mensagem = "Horário não existe"):
        super().__init__(mensagem)

class HorarioNaoPertenceAoMonitorException(Exception):
    def __init__(self, mensagem = "Horário não pertence a esse monitor"):
        super().__init__(mensagem)
        
class DadosHorarioInvalidoException(Exception):
    def __init__(self, mensagem = "Dados do Horário novo inválidos"):
        super().__init__(mensagem)