from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Disciplina, AlunoValido, DisciplinaValida, HorarioAtendimento, MensagemForum

@admin.register(Usuario)
class CustomUsuarioAdmin(UserAdmin):

    list_display = ('username', 'matricula', 'first_name', 'tipo', 'monitor_de')
    list_filter = ('tipo', 'monitor_de')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Acadêmicas', {'fields': ('matricula', 'tipo', 'monitor_de')}),
    )

admin.site.register(Disciplina)
admin.site.register(AlunoValido)
admin.site.register(DisciplinaValida)
admin.site.register(HorarioAtendimento)
admin.site.register(MensagemForum)