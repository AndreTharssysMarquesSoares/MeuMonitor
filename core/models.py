from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# BLOCO A: TABELAS DE VALIDAÇÃO (MOCK SIGAA)
class AlunoValido(models.Model):
    matricula = models.CharField(max_length=20, unique=True)
    nome_completo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.matricula} - {self.nome_completo}"

class DisciplinaValida(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

# BLOCO B: ATORES E OBJETOS DO SISTEMA

class Disciplina(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    
    alunos_interessados = models.ManyToManyField('Usuario', related_name='interesses', blank=True)

    def clean(self):
        if not DisciplinaValida.objects.filter(codigo=self.codigo).exists():
            raise ValidationError("Este código de disciplina não existe na Instituição.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    TIPO_CHOICES = (
        ('ALUNO', 'Aluno'),
        ('ADMIN', 'Administrador'),
    )

    matricula = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True, 
        verbose_name="Matrícula (Apenas Alunos)"
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='ALUNO')

    monitor_de = models.ForeignKey(
        Disciplina, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='monitores', 
        verbose_name="É Monitor da Disciplina"
    )

    def clean(self):
        if self.is_superuser:
            return

        if self.monitor_de and self.tipo != 'ALUNO':
            raise ValidationError("Apenas usuários do tipo 'Aluno' podem ser monitores.")

        if self.tipo == 'ALUNO':
            if not self.matricula:
                raise ValidationError("Usuários do tipo Aluno devem possuir uma matrícula.")
            
            if not AlunoValido.objects.filter(matricula=self.matricula).exists():
                raise ValidationError("Matrícula não encontrada na base de dados da Instituição.")

    def save(self, *args, **kwargs):
        if self.tipo == 'ALUNO' and self.matricula:
            self.username = self.matricula
        self.clean()
        super().save(*args, **kwargs)

    @property
    def eh_monitor(self):
        return self.monitor_de is not None

    def __str__(self):
        identificacao = self.matricula if self.matricula else self.username
        role = "Monitor" if self.eh_monitor else self.get_tipo_display()
        return f"{self.first_name} ({identificacao}) - {role}"


# BLOCO C: FUNCIONALIDADES

class HorarioAtendimento(models.Model):
    monitor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='meus_horarios')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    
    DIAS_SEMANA = (
        ('SEG', 'Segunda-feira'), ('TER', 'Terça-feira'), ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'), ('SEX', 'Sexta-feira'), ('SAB', 'Sábado'),
    )
    dia_semana = models.CharField(max_length=3, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    class Meta:
        verbose_name = "Horário de Atendimento"
        verbose_name_plural = "Horários de Atendimento"

    def clean(self):
        if self.hora_fim <= self.hora_inicio:
            raise ValidationError("A hora final deve ser posterior à inicial.")
        
        monitor_disciplina = getattr(self.monitor, 'monitor_de', None)
        if monitor_disciplina != self.disciplina:
             raise ValidationError(f"O usuário {self.monitor} não é monitor da disciplina {self.disciplina}.")

class MensagemForum(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    titulo = models.CharField(max_length=200, blank=True, null=True)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    
    resposta_para = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respostas')

    def __str__(self):
        tipo = "Tópico" if self.resposta_para is None else "Resposta"
        return f"[{tipo}] {self.autor.first_name}: {self.texto[:20]}..."