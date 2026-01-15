from core.repositories.mensagem_repository import MensagemForumRepository
from core.services.admin_service import AdminService
from core.services.aluno_service import AlunoService
from core.services.usuario_service import UsuarioService
from core.services.disciplina_service import DisciplinaService
from core.services.suspensao_service import SuspensaoService
from core.exceptions.usuario_exceptions import SenhaIncorretaException 
from core.exceptions.mensagem_exceptions import DadosInválidosException, MensagemNaoEncontradaException, TopicosAindaNaoCadastradosException, NenhumaRespostaEncontradaException, AlunoSuspensoNesseForumException
from django.utils import timezone
from core.services.notificacao_service import NotificacaoService, TipoNotificacao
class MensagemForumService:
    
    @staticmethod
    def criarTopicoAdmin(username, senha, titulo, texto, codigoDisciplina):
        
        admin = AdminService.getAdmin(username)
        disciplina = DisciplinaService.get_Disciplina(codigoDisciplina)
        
        if not UsuarioService.validarSenha(admin, senha): raise SenhaIncorretaException()
        
        if titulo is None or texto is None or codigoDisciplina is None or titulo == "" or texto == "" or codigoDisciplina == "": raise DadosInválidosException()
        
        topico = MensagemForumRepository.criarMensagem(
            titulo = titulo,
            texto = texto,
            autor = admin.username,
            disciplina = disciplina.codigo,
            resposta_para = None
        )
        
        for a in disciplina.alunos_interessados.all():
            NotificacaoService.gerarNotificacao(TipoNotificacao.FORUM, titulo, texto, a.matricula, topico.id)
            
        monitores = AlunoService.getMonitoresDisciplina(codigoDisciplina)
        
        for m in monitores:
            NotificacaoService.gerarNotificacao(TipoNotificacao.FORUM, titulo, texto, m.matricula, topico.id)
            
        return topico
        
    @staticmethod
    def criarMensagemAdmin(username, senha, texto, codigoDisciplina, idMensagemRespondida):
        
        admin = AdminService.getAdmin(username)
        disciplina = DisciplinaService.get_Disciplina(codigoDisciplina)
        
        if not UsuarioService.validarSenha(admin, senha): raise SenhaIncorretaException()
        
        if idMensagemRespondida is None or texto is None or codigoDisciplina is None or idMensagemRespondida == "" or texto == "" or codigoDisciplina == "": raise DadosInválidosException()
        
        mensagemPai = MensagemForumRepository.getMensagem(idMensagemRespondida)
        
        if not mensagemPai: raise MensagemNaoEncontradaException()
        
        mensagem = MensagemForumRepository.criarMensagem(
            titulo = None,
            texto = texto,
            autor = admin.username,
            disciplina = disciplina.codigo,
            resposta_para = idMensagemRespondida
        )
        
        for a in disciplina.alunos_interessados.all():
            NotificacaoService.gerarNotificacao(TipoNotificacao.FORUM, None, texto, a.matricula, mensagem.id)
            
        monitores = AlunoService.getMonitoresDisciplina(codigoDisciplina)
        
        for m in monitores:
            NotificacaoService.gerarNotificacao(TipoNotificacao.FORUM, None, texto, m.matricula, mensagem.id)
        
        return mensagem
        
    @staticmethod
    def criarTopicoAluno(matricula, senha, titulo, texto, codigoDisciplina):
        
        aluno = AlunoService.getAluno(matricula)
        disciplina = DisciplinaService.get_Disciplina(codigoDisciplina)
        
        if not UsuarioService.validarSenha(aluno, senha): raise SenhaIncorretaException()
        
        hoje = timezone.now().date()
        suspensoes = SuspensaoService.getSuspensoesAlunoDisciplina(matricula, codigoDisciplina)
        
        for s in suspensoes:
            if s.data_fim >= hoje: raise AlunoSuspensoNesseForumException()
        
        if titulo is None or texto is None or codigoDisciplina is None or titulo == "" or texto == "" or codigoDisciplina == "": raise DadosInválidosException()
        
        topico = MensagemForumRepository.criarMensagem(
            titulo = titulo,
            texto = texto,
            autor = aluno.matricula,
            disciplina = disciplina.codigo,
            resposta_para = None
        )
        
        for a in disciplina.alunos_interessados.all():
            NotificacaoService.gerarNotificacao(TipoNotificacao.FORUM, titulo, texto, a.matricula, topico.id)
            
        monitores = AlunoService.getMonitoresDisciplina(codigoDisciplina)
        
        for m in monitores:
            NotificacaoService.gerarNotificacao(TipoNotificacao.FORUM, titulo, texto, m.matricula, topico.id)
        
        return topico
        
    @staticmethod
    def criarMensagemAluno(matricula, senha, texto, codigoDisciplina, idMensagemRespondida):
        
        aluno = AlunoService.getAluno(matricula)
        disciplina = DisciplinaService.get_Disciplina(codigoDisciplina)
        
        if not UsuarioService.validarSenha(aluno, senha): raise SenhaIncorretaException()
        
        if idMensagemRespondida is None or texto is None or codigoDisciplina is None or idMensagemRespondida == "" or texto == "" or codigoDisciplina == "": raise DadosInválidosException()
        
        hoje = timezone.now().date()
        suspensoes = SuspensaoService.getSuspensoesAlunoDisciplina(matricula, codigoDisciplina)
        
        for s in suspensoes:
            if s.data_fim >= hoje: raise AlunoSuspensoNesseForumException()
        
        mensagemPai = MensagemForumRepository.getMensagem(idMensagemRespondida)
        
        if not mensagemPai: raise MensagemNaoEncontradaException()
        
        mensagem = MensagemForumRepository.criarMensagem(
            titulo = None,
            texto = texto,
            autor = aluno.matricula,
            disciplina = disciplina.codigo,
            resposta_para = idMensagemRespondida
        )
        
        for a in disciplina.alunos_interessados.all():
            NotificacaoService.gerarNotificacao(TipoNotificacao.FORUM, None, texto, a.matricula, mensagem.id)
            
        monitores = AlunoService.getMonitoresDisciplina(codigoDisciplina)
        
        for m in monitores:
            NotificacaoService.gerarNotificacao(TipoNotificacao.FORUM, None, texto, m.matricula, mensagem.id)
            
        return mensagem
        
    @staticmethod
    def removerMensagemAdmin(username, senha, id):
        
        admin = AdminService.getAdmin(username)
        
        if not UsuarioService.validarSenha(admin, senha): raise SenhaIncorretaException()
        
        mensagem = MensagemForumService.getMensagem(id)
        
        mensagem.delete()
        
        return True
        
    @staticmethod
    def removerMensagemAluno(matricula, senha, id):
        
        aluno =  AlunoService.getAluno(matricula)
        
        if not UsuarioService.validarSenha(aluno, senha): raise SenhaIncorretaException()
        
        mensagem = MensagemForumService.getMensagem(id)
        
        mensagem.delete()
        
        return True
        
    @staticmethod
    def getMensagem(id):
        mensagem = MensagemForumRepository.getMensagem(id)
        if not mensagem: raise MensagemNaoEncontradaException()
        return mensagem
        
    @staticmethod
    def getTopicosDaDisciplina(codigoDisciplina):
        disciplina = DisciplinaService.get_Disciplina(codigoDisciplina)
        mensagens = MensagemForumRepository.getTopicosDaDisciplina(disciplina.codigo)
        if not mensagens: raise TopicosAindaNaoCadastradosException()
        return mensagens
        
    @staticmethod
    def getRespostas(idMensagem):
        mensagens = MensagemForumRepository.getRespostas(idMensagem)
        if not mensagens: raise NenhumaRespostaEncontradaException()
        return mensagens
        
    @staticmethod
    def getAutor(idMensagem):
        mensagem = MensagemForumService.getMensagem(idMensagem)
        return mensagem.autor
    
    @staticmethod
    def criarTopicoWeb(matricula, codigoDisciplina, titulo, texto):
        """
        Cria um novo tópico no fórum (versão web - usuário já autenticado).
        """
        from core.models import Usuario, Disciplina

        try:
            autor = Usuario.objects.get(username=matricula)
        except Usuario.DoesNotExist:
            raise Exception("Aluno não encontrado.")

        try:
            disciplina = Disciplina.objects.get(codigo=codigoDisciplina)
        except Disciplina.DoesNotExist:
            raise Exception("Disciplina não encontrada.")

        if not titulo or not titulo.strip():
            raise Exception("O título não pode estar vazio.")
        
        if not texto or not texto.strip():
            raise Exception("O texto não pode estar vazio.")
 
        topico = MensagemForumRepository.criarMensagem(
            autor=autor,
            disciplina=disciplina,
            titulo=titulo.strip(),
            texto=texto.strip(),
            resposta_para=None
        )

        interessados = Usuario.objects.filter(interesses=disciplina).exclude(username=matricula)

        for destinatario in interessados:
            try:
                NotificacaoService.gerarNotificacao(
                    tipo=TipoNotificacao.FORUM,
                    titulo=f"Novo tópico em {disciplina.nome}",
                    texto=f"{autor.first_name} criou: {titulo}",
                    destinatario=destinatario,
                    mensagem_forum=topico
                )
            except Exception as e:
                print(f"Erro ao notificar {destinatario.username}: {e}")
        
        return topico
    
    @staticmethod
    def responderTopicoWeb(matricula, idMensagem, texto):
        """
        Responde a um tópico existente (versão web - usuário já autenticado).
        """
        from core.models import Usuario, MensagemForum

        try:
            autor = Usuario.objects.get(username=matricula)
        except Usuario.DoesNotExist:
            raise Exception("Aluno não encontrado.")

        try:
            mensagem_pai = MensagemForum.objects.get(id=idMensagem)
        except MensagemForum.DoesNotExist:
            raise Exception("Tópico não encontrado.")

        if not texto or not texto.strip():
            raise Exception("A resposta não pode estar vazia.")

        resposta = MensagemForumRepository.criarMensagem(
            autor=autor,
            disciplina=mensagem_pai.disciplina,
            titulo=None,
            texto=texto.strip(),
            resposta_para=mensagem_pai
        )

        topico_raiz = mensagem_pai
        while topico_raiz.resposta_para is not None:
            topico_raiz = topico_raiz.resposta_para
        
        disciplina = topico_raiz.disciplina
        interessados = Usuario.objects.filter(interesses=disciplina).exclude(username=matricula)
        
        for destinatario in interessados:
            try:
                NotificacaoService.gerarNotificacao(
                    tipo=TipoNotificacao.FORUM,
                    titulo=f"Nova resposta em '{topico_raiz.titulo}'",
                    texto=f"{autor.first_name} respondeu no fórum",
                    destinatario=destinatario,
                    mensagem_forum=resposta
                )
            except Exception as e:
                print(f"Erro ao notificar {destinatario.username}: {e}")
        
        return resposta
    
    @staticmethod
    def getRespostasComAninhamento(id_mensagem):
        from core.models import MensagemForum
        
        respostas_diretas = MensagemForum.objects.filter(resposta_para_id=id_mensagem).order_by('data_envio')
        
        resultado = []
        for r in respostas_diretas:
            sub_respostas = MensagemForumService.getRespostasComAninhamento(r.id)
            resultado.append({
                'objeto': r,
                'respostas': sub_respostas
            })
        
        return resultado

    @staticmethod
    def contarRespostasTotal(respostas):
        """
        Conta recursivamente todas as respostas (incluindo sub-respostas).
        Recebe uma lista de dicionários com 'objeto' e 'respostas'.
        """
        if not respostas:
            return 0
        total = 0
        for resp in respostas:
            total += 1
            if 'respostas' in resp and resp['respostas']:
                total += MensagemForumService.contarRespostasTotal(resp['respostas'])
        return total

    @staticmethod
    def excluirMensagem(id_mensagem):
        from core.models import MensagemForum
        
        mensagem = MensagemForum.objects.filter(id=id_mensagem).first()
        if not mensagem:
            raise Exception("Mensagem não encontrada.")

        mensagem.delete()
        return True