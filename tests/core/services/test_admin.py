import pytest
from core.services.admin_service import AdminService
from core.exceptions.usuario_exceptions import AlunoNaoCadastradoException, SenhaIncorretaException, SenhaFracaException, DadosInvalidoException, AdminJaCadastradoException, UserNameInvalidoException, AdminInvalidoException, UsernameAdminNaoExisteException, AlunoJaDesativadoException, MonitorJaCadastradoException, MonitorNaoCadastradoException, AlunoJaAtivadoException

def test_cadastrar_admin_ja_existente(mocker):
    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.exist_admin",
        return_value=True
    )

    with pytest.raises(AdminJaCadastradoException):
        AdminService.cadastrarAdmin(
            username="admin1",
            senha="Senha@123",
            nome_completo="Admin Teste",
            email="admin@email.com"
        )
        

def test_cadastrar_admin_username_invalido(mocker):
    
    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.exist_admin",
        return_value=False
    )

    with pytest.raises(UserNameInvalidoException):
        AdminService.cadastrarAdmin(
            username="A B",
            senha="Senha@123",
            nome_completo="Admin Teste",
            email="admin@email.com"
        )
        
def test_cadastrar_admin_senha_fraca(mocker):

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.exist_admin",
        return_value=False
    )

    with pytest.raises(SenhaFracaException):
        AdminService.cadastrarAdmin(
            username="admin1",
            senha="senhafraca",
            nome_completo="Admin Teste",
            email="admin@email.com"
        )

def test_cadastrar_admin_email_vazio(mocker):

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.exist_admin",
        return_value=False
    )
    
    with pytest.raises(DadosInvalidoException):
        AdminService.cadastrarAdmin(
            username="Admin1",
            senha="Senha@123",
            nome_completo="Admin Teste",
            email=""
        )
        
def test_cadastrar_admin_valido(mocker):

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.exist_admin",
        return_value=False
    )
    
    payload = {
        "username": "admin123",
        "senha": "SenhaForte@123",
        "nome_completo": "Admin Sistema",
        "email": "admin@sistema.com"
    }
    
    usuario_mock = mocker.Mock()

    criar_usuario_mock = mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.criar_usuario",
        return_value=usuario_mock
    )

    result = AdminService.cadastrarAdmin(**payload)

    criar_usuario_mock.assert_called_once_with(
        username="admin123",
        password="SenhaForte@123",
        first_name="Admin",
        last_name="Sistema",
        email="admin@sistema.com",
        matricula="admin123",
        tipo="ADMIN",
        is_superuser=True,
        is_staff=False,
        is_active=True
    )

    assert result == usuario_mock
    
def test_alterar_admin_admin_nao_existe(mocker):
    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_admin",
        return_value=None
    )

    with pytest.raises(AdminInvalidoException):
        AdminService.alterarAdmin("admin", "Senha@123")
        
def test_alterar_admin_senha_atual_incorreta(mocker):
    admin_mock = mocker.Mock()

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_admin",
        return_value=admin_mock
    )
    
    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=False
    )

    with pytest.raises(SenhaIncorretaException):
        AdminService.alterarAdmin("admin", "errada")
        
from core.exceptions.usuario_exceptions import SenhaFracaException

def test_alterar_admin_nova_senha_fraca(mocker):
    admin_mock = mocker.Mock()

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_admin",
        return_value=admin_mock
    )

    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=True
    )

    with pytest.raises(SenhaFracaException):
        AdminService.alterarAdmin(
            "admin",
            "Senha@123",
            nova_senha="fraca"
        )
        
def test_alterar_admin_email_vazio(mocker):
    admin_mock = mocker.Mock()
    admin_mock.check_password.return_value = True

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_admin",
        return_value=admin_mock
    )

    with pytest.raises(DadosInvalidoException):
        AdminService.alterarAdmin(
            username="admin",
            senha_atual="Senha@123",
            email=""
        )

        
def test_alterar_admin_email_e_senha_sucesso(mocker):
    admin_mock = mocker.Mock()
    admin_mock.email = "antigo@email.com"

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_admin",
        return_value=admin_mock
    )

    mocker.patch(
        "core.services.usuario_service.UsuarioService.validarSenha",
        return_value=True
    )

    salvar_mock = mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.salvar"
    )

    result = AdminService.alterarAdmin(
        "admin",
        "Senha@123",
        email="novo@email.com",
        nova_senha="NovaSenha@123"
    )

    assert admin_mock.email == "novo@email.com"
    admin_mock.set_password.assert_called_once_with("NovaSenha@123")
    salvar_mock.assert_called_once_with(admin_mock)
    assert result == admin_mock

def test_validar_acesso_admin_nao_existe(mocker):
    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_admin",
        return_value=None
    )

    with pytest.raises(UsernameAdminNaoExisteException):
        AdminService.validarAcessoAdmin("admin", "Senha@123")
        

def test_validar_acesso_admin_senha_incorreta(mocker):
    admin_mock = mocker.Mock()
    admin_mock.check_password.return_value = False

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_admin",
        return_value=admin_mock
    )

    with pytest.raises(SenhaIncorretaException):
        AdminService.validarAcessoAdmin("admin", "senha_errada")

from core.services.admin_service import AdminService

def test_validar_acesso_admin_valido(mocker):
    admin_mock = mocker.Mock()
    admin_mock.check_password.return_value = True

    mocker.patch(
        "core.repositories.usuario_repository.UsuarioRepository.get_admin",
        return_value=admin_mock
    )

    resultado = AdminService.validarAcessoAdmin("admin", "Senha@123")

    assert resultado is True

def test_desativar_aluno_admin_invalido(mocker):
    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=False
    )

    with pytest.raises(AdminInvalidoException):
        AdminService.desativarAluno("admin", "senha", "2023001")
        
def test_desativar_aluno_ja_desativado(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.is_active = False

    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    mocker.patch(
        "core.services.admin_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    with pytest.raises(AlunoJaDesativadoException):
        AdminService.desativarAluno("admin", "senha", "2023001")
        
def test_desativar_aluno_com_sucesso(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.is_active = True

    validar_mock = mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    salvar_mock = mocker.patch(
        "core.services.admin_service.UsuarioRepository.salvar"
    )

    mocker.patch(
        "core.services.admin_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    aluno = AdminService.desativarAluno("admin", "senha", "2023001")

    assert aluno.is_active is False
    salvar_mock.assert_called_once_with(aluno)
    validar_mock.assert_called_once()

def test_ativar_aluno_admin_invalido(mocker):
    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=False
    )

    with pytest.raises(AdminInvalidoException):
        AdminService.ativarAluno("admin", "senha", "2023001")
        
def test_ativar_aluno_ja_ativado(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.is_active = True

    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    mocker.patch(
        "core.services.admin_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    with pytest.raises(AlunoJaAtivadoException):
        AdminService.ativarAluno("admin", "senha", "2023001")
        
def test_ativar_aluno_com_sucesso(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.is_active = False

    validar_mock = mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    salvar_mock = mocker.patch(
        "core.services.admin_service.UsuarioRepository.salvar"
    )

    mocker.patch(
        "core.services.admin_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    aluno = AdminService.ativarAluno("admin", "senha", "2023001")

    assert aluno.is_active is True
    salvar_mock.assert_called_once_with(aluno)
    validar_mock.assert_called_once()

def test_criar_monitor_admin_invalido(mocker):
    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=False
    )

    with pytest.raises(AdminInvalidoException):
        AdminService.criarMonitor("admin", "senha", "2023001", "MAT001")
        
def test_criar_monitor_aluno_nao_existe(mocker):
    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    mocker.patch(
        "core.services.admin_service.AlunoService.getAluno",
        return_value=None
    )

    with pytest.raises(AlunoNaoCadastradoException):
        AdminService.criarMonitor("admin", "senha", "2023001", "MAT001")
        
def test_criar_monitor_aluno_ja_monitor(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.monitor_de = "MAT001"

    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    mocker.patch(
        "core.services.admin_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.admin_service.DisciplinaService.get_Disciplina"
    )

    with pytest.raises(MonitorJaCadastradoException):
        AdminService.criarMonitor("admin", "senha", "2023001", "MAT001")
        
def test_criar_monitor_com_sucesso(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.monitor_de = None

    disciplina_mock = mocker.Mock()
    disciplina_mock.codigo = "MAT001"

    validar_mock = mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    salvar_mock = mocker.patch(
        "core.services.admin_service.UsuarioRepository.salvar"
    )

    mocker.patch(
        "core.services.admin_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    mocker.patch(
        "core.services.admin_service.DisciplinaService.get_Disciplina",
        return_value=disciplina_mock
    )

    aluno = AdminService.criarMonitor("admin", "senha", "2023001", "MAT001")

    assert aluno.monitor_de == "MAT001"
    salvar_mock.assert_called_once_with(aluno)
    validar_mock.assert_called_once()
    
def test_remover_monitor_admin_invalido(mocker):
    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=False
    )

    with pytest.raises(AdminInvalidoException):
        AdminService.removerMonitor("admin", "senha", "2023001")

def test_remover_monitor_aluno_nao_existe(mocker):
    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    mocker.patch(
        "core.services.admin_service.AlunoService.getAluno",
        return_value=None
    )

    with pytest.raises(AlunoNaoCadastradoException):
        AdminService.removerMonitor("admin", "senha", "2023001")

def test_remover_monitor_aluno_nao_e_monitor(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.monitor_de = None

    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    mocker.patch(
        "core.services.admin_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    with pytest.raises(MonitorNaoCadastradoException):
        AdminService.removerMonitor("admin", "senha", "2023001")
        
def test_remover_monitor_com_sucesso(mocker):
    aluno_mock = mocker.Mock()
    aluno_mock.monitor_de = "MAT001"

    validar_mock = mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    salvar_mock = mocker.patch(
        "core.services.admin_service.UsuarioRepository.salvar"
    )

    mocker.patch(
        "core.services.admin_service.AlunoService.getAluno",
        return_value=aluno_mock
    )

    aluno = AdminService.removerMonitor("admin", "senha", "2023001")

    assert aluno.monitor_de is None
    salvar_mock.assert_called_once_with(aluno)
    validar_mock.assert_called_once()

def test_criar_disciplina_admin_invalido(mocker):
    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=False
    )

    with pytest.raises(AdminInvalidoException):
        AdminService.criarDisciplina("admin", "senha", "MAT001")
        
def test_criar_disciplina_com_sucesso(mocker):
    disciplina_mock = mocker.Mock()

    validar_mock = mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    cadastrar_mock = mocker.patch(
        "core.services.admin_service.DisciplinaService.cadastrarDisciplina",
        return_value=disciplina_mock
    )

    disciplina = AdminService.criarDisciplina("admin", "senha", "MAT001")

    assert disciplina == disciplina_mock
    cadastrar_mock.assert_called_once_with(codigo="MAT001")
    validar_mock.assert_called_once()

def test_get_monitores_admin_invalido(mocker):
    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=False
    )

    with pytest.raises(AdminInvalidoException):
        AdminService.getMonitores("admin", "senha")
    
def test_get_monitores_com_sucesso(mocker):
    monitores_mock = [mocker.Mock(), mocker.Mock()]

    validar_mock = mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    repo_mock = mocker.patch(
        "core.services.admin_service.UsuarioRepository.get_monitores",
        return_value=monitores_mock
    )

    resultado = AdminService.getMonitores("admin", "senha")

    assert resultado == monitores_mock
    repo_mock.assert_called_once()
    validar_mock.assert_called_once()
    
def test_get_nao_monitores_admin_invalido(mocker):
    mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=False
    )

    with pytest.raises(AdminInvalidoException):
        AdminService.getNaoMonitores("admin", "senha")
        
def test_get_nao_monitores_com_sucesso(mocker):
    nao_monitores_mock = [mocker.Mock()]

    validar_mock = mocker.patch(
        "core.services.admin_service.AdminService.validarAcessoAdmin",
        return_value=True
    )

    repo_mock = mocker.patch(
        "core.services.admin_service.UsuarioRepository.get_nao_monitores",
        return_value=nao_monitores_mock
    )

    resultado = AdminService.getNaoMonitores("admin", "senha")

    assert resultado == nao_monitores_mock
    repo_mock.assert_called_once()
    validar_mock.assert_called_once()
