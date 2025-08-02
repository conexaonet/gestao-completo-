from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log de tentativas de acesso
        if request.path.startswith('/senhas/'):
            logger.info(f'Tentativa de acesso ao gerenciador de senhas: {request.user} - {request.path} - {request.META.get("REMOTE_ADDR")}')
        
        response = self.get_response(request)
        return response

def require_senhas_permission(view_func):
    """
    Decorator para verificar permissão específica para acessar o gerenciador de senhas
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('core:senhas_login')
        
        # Verificar se o usuário tem permissão específica
        if not hasattr(request.user, 'perfil') or not request.user.perfil.pode_acessar_senhas:
            messages.error(request, 'Você não tem permissão para acessar o gerenciador de senhas.')
            return redirect('admin:index')
        
        # Marcar sessão como autorizada
        request.session['senhas_authorized'] = True
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def require_admin_or_senhas_permission(view_func):
    """
    Decorator para verificar se é admin ou tem permissão específica
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('admin:login')
        
        # Admin sempre tem acesso
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        # Verificar permissão específica
        if not hasattr(request.user, 'perfil') or not request.user.perfil.pode_acessar_senhas:
            messages.error(request, 'Você não tem permissão para acessar esta funcionalidade.')
            return redirect('admin:index')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view 