from core.models import Usuario, AlunoValido

class UsuarioRepository:
    
    @staticmethod
    def matricula_valida(matricula):
        return AlunoValido.objects.filter(matricula = matricula).exists()
    
    @staticmethod
    def criar_usuario(**data):
        return Usuario.objects.create_user(**data) 
    
    @staticmethod
    def exist_aluno(matricula):
        return Usuario.objects.filter(tipo='ALUNO', matricula= matricula).exists()
    
    @staticmethod
    def salvar(usuario):
        usuario.save()
        
    @staticmethod
    def exist_admin(username):
        return Usuario.objects.filter(tipo = 'ADMIN', username=username).exists()
        
    @staticmethod
    def get_admin(username):
        return Usuario.objects.filter(tipo= 'ADMIN', is_superuser = True, username = username).first()
    
    @staticmethod
    def get_admins():
        return Usuario.objects.filter(tipo= 'ADMIN', is_superuser = True)
    
    @staticmethod
    def get_aluno_valido(matricula):
        return AlunoValido.objects.filter(matricula=matricula).first()         
    
    @staticmethod
    def get_usuario(id):
        return Usuario.objects.filter(id=id).first()
    
    @staticmethod
    def get_alunos():
        return Usuario.objects.filter(tipo = 'ALUNO')
    
    @staticmethod
    def get_aluno(matricula):
        return Usuario.objects.filter(tipo = 'ALUNO', matricula=matricula).first()
    
    @staticmethod
    def get_monitores():
        return Usuario.objects.filter(tipo = 'ALUNO', monitor_de__isnull=False)
    
    @staticmethod
    def get_nao_monitores():
        return Usuario.objects.filter(tipo = 'ALUNO', monitor_de__isnull=True)
    
    @staticmethod
    def get_monitores_disciplina(disciplina):
        return Usuario.objects.filter(tipo = 'ALUNO', monitor_de=disciplina)
    