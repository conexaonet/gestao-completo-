from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.middleware import require_senhas_permission
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Página inicial do sistema"""
    if not request.user.is_authenticated:
        return redirect('/admin/login/')
    return render(request, 'dev_dashboard.html')

@login_required
def dashboard(request):
    """Dashboard principal do sistema"""
    context = {
        'titulo': 'Dashboard - Gestão Empresarial',
        'usuario': request.user,
    }
    return render(request, 'dev_dashboard.html', context)

def contas_pagar_view(request):
    """Página de contas a pagar"""
    return render(request, 'contas_pagar.html')

def despesas_view(request):
    """Página de despesas"""
    return render(request, 'despesas.html')

@login_required
@require_senhas_permission
def senhas_view(request):
    """View protegida para o gerenciador de senhas"""
    try:
        # Marcar sessão como autorizada
        request.session['senhas_authorized'] = True
        
        # Registrar acesso
        if hasattr(request.user, 'perfil'):
            request.user.perfil.registrar_acesso(
                request, 
                '/senhas/',
                'acesso_pagina_senhas',
                True
            )
            request.user.perfil.atualizar_ultimo_acesso()
        
        return render(request, 'senhas.html')
    except Exception as e:
        logger.error(f"Erro ao acessar página de senhas: {e}")
        messages.error(request, 'Erro ao carregar página de senhas')
        return redirect('admin:index')

def senhas_login_view(request):
    """Página de login específica para o gerenciador de senhas"""
    if request.user.is_authenticated:
        # Se já está logado, verificar permissões
        if hasattr(request.user, 'perfil') and request.user.perfil.pode_acessar_senhas:
            # Marcar sessão como autorizada
            request.session['senhas_authorized'] = True
            return redirect('core:senhas')
        else:
            messages.error(request, 'Você não tem permissão para acessar o gerenciador de senhas.')
            return redirect('admin:index')
    
    return render(request, 'senhas_login.html')

def notas_fiscais_view(request):
    """Página de notas fiscais"""
    return render(request, 'notas_fiscais.html')

def relatorio_mensal_view(request):
    """Página de relatório mensal"""
    return render(request, 'relatorio_mensal.html')

def relatorio_categoria_view(request):
    """Página de análise por categoria"""
    return render(request, 'relatorio_categoria.html')

def relatorio_evolucao_view(request):
    """Página de evolução de gastos"""
    return render(request, 'relatorio_evolucao.html')

