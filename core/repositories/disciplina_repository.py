from core.models import Disciplina, DisciplinaValida

class DisciplinaRepository:
    
    @staticmethod
    def criar_disciplina(**data):
        return Disciplina.objects.create(**data)
        
    @staticmethod
    def salvar(disciplina):
        disciplina.save()
    
    @staticmethod
    def exist_disciplina(codigo):
        return Disciplina.objects.filter(codigo = codigo).exists()
    
    @staticmethod
    def exist_disciplinaValida(codigo):
        return DisciplinaValida.objects.filter(codigo=codigo).exists
    
    @staticmethod
    def get_disciplina(codigo):
        return Disciplina.objects.filter(codigo=codigo).first()
    
    @staticmethod
    def get_disciplinaValida(codigo):
        return DisciplinaValida.objects.filter(codigo=codigo).first()

    @staticmethod
    def get_todas_disciplinas():
        return Disciplina.objects.all().order_by('nome')