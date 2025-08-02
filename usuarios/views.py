from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth.models import User
from .models import PerfilUsuario, Permissao, GrupoPermissao, UsuarioPermissao, LogAcesso
from .serializers import (
    PerfilUsuarioSerializer,
    PerfilUsuarioListSerializer,
    PermissaoSerializer,
    GrupoPermissaoSerializer
)

# Views para páginas web
@login_required
def usuarios_view(request):
    """Página principal de usuários"""
    return render(request, 'usuarios.html')

@login_required
def novo_usuario_view(request):
    """Página para adicionar novo usuário"""
    return render(request, 'novo_usuario.html')

@login_required
def detalhe_usuario_view(request, pk):
    """Página de detalhes do usuário"""
    return render(request, 'detalhe_usuario.html')

@login_required
def editar_usuario_view(request, pk):
    """Página para editar usuário"""
    return render(request, 'editar_usuario.html')

# Views para API
class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Apenas administradores podem ver todos os usuários
        if self.request.user.is_superuser:
            return PerfilUsuario.objects.all()
        else:
            # Usuários normais só veem seu próprio perfil
            return PerfilUsuario.objects.filter(usuario=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PerfilUsuarioListSerializer
        return PerfilUsuarioSerializer
    
    def perform_create(self, serializer):
        # Apenas administradores podem criar usuários
        if not self.request.user.is_superuser:
            raise PermissionError("Apenas administradores podem criar usuários")
        
        # Salvar o serializer normalmente
        serializer.save()
    
    def perform_update(self, serializer):
        # Apenas administradores podem atualizar usuários
        if not self.request.user.is_superuser:
            raise PermissionError("Apenas administradores podem atualizar usuários")
        
        # Salvar o serializer normalmente
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def meu_perfil(self, request):
        """Retorna o perfil do usuário logado"""
        perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
        serializer = self.get_serializer(perfil)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        """Altera o status do usuário"""
        if not request.user.is_superuser:
            return Response({'error': 'Permissão negada'}, status=403)
        
        perfil = self.get_object()
        novo_status = request.data.get('status')
        
        if novo_status in ['ativo', 'inativo', 'suspenso']:
            perfil.status = novo_status
            perfil.save()
            serializer = self.get_serializer(perfil)
            return Response(serializer.data)
        
        return Response({'error': 'Status inválido'}, status=400)
    
    @action(detail=True, methods=['post'])
    def alterar_nivel(self, request, pk=None):
        """Altera o nível de acesso do usuário"""
        if not request.user.is_superuser:
            return Response({'error': 'Permissão negada'}, status=403)
        
        perfil = self.get_object()
        novo_nivel = request.data.get('nivel_acesso')
        
        if novo_nivel in ['visualizador', 'usuario', 'gerente', 'admin']:
            perfil.nivel_acesso = novo_nivel
            perfil.save()
            serializer = self.get_serializer(perfil)
            return Response(serializer.data)
        
        return Response({'error': 'Nível de acesso inválido'}, status=400)
    
    @action(detail=True, methods=['get'])
    def mostrar_senha(self, request, pk=None):
        """Mostra a senha do usuário (apenas para administradores)"""
        if not request.user.is_superuser:
            return Response({'error': 'Permissão negada'}, status=403)
        
        perfil = self.get_object()
        user = perfil.usuario
        
        # Por segurança, não retornamos a senha real
        # Em vez disso, retornamos uma mensagem informativa
        return Response({
            'usuario': user.username,
            'senha': '********',
            'mensagem': 'Por segurança, as senhas não podem ser visualizadas diretamente. Use a opção de redefinir senha.'
        })
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos usuários"""
        if not request.user.is_superuser:
            return Response({'error': 'Permissão negada'}, status=403)
        
        total = PerfilUsuario.objects.count()
        ativos = PerfilUsuario.objects.filter(status='ativo').count()
        administradores = PerfilUsuario.objects.filter(nivel_acesso='admin').count()
        
        # Último acesso
        ultimo_acesso = PerfilUsuario.objects.filter(
            ultimo_acesso__isnull=False
        ).order_by('-ultimo_acesso').values_list('ultimo_acesso', flat=True).first()
        
        return Response({
            'total': total,
            'ativos': ativos,
            'administradores': administradores,
            'ultimo_acesso': ultimo_acesso.strftime('%d/%m/%Y %H:%M') if ultimo_acesso else None
        })

class PermissaoViewSet(viewsets.ModelViewSet):
    serializer_class = PermissaoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Permissao.objects.none()
        return Permissao.objects.filter(ativo=True)

class GrupoPermissaoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoPermissaoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return GrupoPermissao.objects.none()
        return GrupoPermissao.objects.filter(ativo=True) 