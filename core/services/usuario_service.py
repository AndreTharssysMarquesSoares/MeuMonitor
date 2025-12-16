from core.repositories.usuario_repository import UsuarioRepository
from core.exceptions.usuario_exceptions import SenhaIncorretaException, UsuarioNaoExisteException, SenhaFracaException
import re

class UsuarioService:
        
    @staticmethod
    def alterarSenha(id, senhaAtual, novaSenha):
        user = UsuarioRepository.get_usuario(id = id)
        if not user: raise UsuarioNaoExisteException()
        if not UsuarioService.validarSenha(user, senhaAtual): raise SenhaIncorretaException()
        if not UsuarioService.auth_password_validators(novaSenha): raise SenhaFracaException()
        
        user.set_password(novaSenha)
        
        UsuarioRepository.salvar(usuario=user)
        
        return user

    @staticmethod
    def auth_password_validators(senha) -> bool:
        if len(senha) < 8:
            return False

        if not re.search(r"[A-Z]", senha):
            return False

        if not re.search(r"[a-z]", senha):
            return False

        if not re.search(r"[0-9]", senha):
            return False

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
            return False

        return True
        
    @staticmethod
    def validarSenha(user, senha) -> bool:
        return user.check_password(senha) 
    
    @staticmethod
    def username_valido(username) -> bool:
        return username is not None and " " not in username and username != ""