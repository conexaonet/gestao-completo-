from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
from core.middleware import require_admin_or_senhas_permission
from .models import GerenciadorSenhas
from .serializers import GerenciadorSenhasSerializer, GerenciadorSenhasListSerializer
import logging

logger = logging.getLogger(__name__)

class GerenciadorSenhasViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Verificar permissões
        if not self.request.user.is_authenticated:
            logger.warning(f'Tentativa de acesso não autenticado: {self.request.META.get("REMOTE_ADDR")}')
            return GerenciadorSenhas.objects.none()
        
        # Registrar acesso
        if hasattr(self.request.user, 'perfil'):
            self.request.user.perfil.registrar_acesso(
                self.request, 
                f'/api/senhas/senhas/{self.action}/',
                'listar_senhas'
            )
        
        # Verificar permissão específica
        if not self.request.user.is_superuser:
            if not hasattr(self.request.user, 'perfil') or not self.request.user.perfil.pode_acessar_senhas:
                logger.warning(f'Tentativa de acesso sem permissão: {self.request.user.username} - {self.request.META.get("REMOTE_ADDR")}')
                return GerenciadorSenhas.objects.none()
        
        queryset = GerenciadorSenhas.objects.filter(usuario=self.request.user)
        print(f"QuerySet para usuário {self.request.user.username}: {queryset.count()} senhas")
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GerenciadorSenhasListSerializer
        return GerenciadorSenhasSerializer
    
    def perform_create(self, serializer):
        try:
            # Verificar permissões
            if not self.request.user.is_superuser:
                if not hasattr(self.request.user, 'perfil') or not self.request.user.perfil.pode_acessar_senhas:
                    logger.warning(f'Tentativa de criar senha sem permissão: {self.request.user.username}')
                    raise PermissionError("Sem permissão para criar senhas")
            
            print(f"Criando senha para usuário: {self.request.user.username}")
            print(f"Dados recebidos: {self.request.data}")
            print(f"Files recebidos: {self.request.FILES}")
            
            instance = serializer.save(usuario=self.request.user)
            print(f"Senha criada com sucesso: {instance.id}")
            
            # Registrar acesso
            if hasattr(self.request.user, 'perfil'):
                self.request.user.perfil.registrar_acesso(
                    self.request, 
                    f'/api/senhas/senhas/{instance.id}/',
                    'criar_senha',
                    True
                )
            
            return instance
        except Exception as e:
            print(f"Erro ao criar senha: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
            # Registrar erro
            if hasattr(self.request.user, 'perfil'):
                self.request.user.perfil.registrar_acesso(
                    self.request, 
                    '/api/senhas/senhas/',
                    'criar_senha',
                    False
                )
            
            raise e
    
    def perform_update(self, serializer):
        try:
            # Verificar permissões
            if not self.request.user.is_superuser:
                if not hasattr(self.request.user, 'perfil') or not self.request.user.perfil.pode_acessar_senhas:
                    logger.warning(f'Tentativa de atualizar senha sem permissão: {self.request.user.username}')
                    raise PermissionError("Sem permissão para atualizar senhas")
            
            instance = serializer.save()
            
            # Registrar acesso
            if hasattr(self.request.user, 'perfil'):
                self.request.user.perfil.registrar_acesso(
                    self.request, 
                    f'/api/senhas/senhas/{instance.id}/',
                    'atualizar_senha',
                    True
                )
            
            return instance
        except Exception as e:
            # Registrar erro
            if hasattr(self.request.user, 'perfil'):
                self.request.user.perfil.registrar_acesso(
                    self.request, 
                    f'/api/senhas/senhas/{serializer.instance.id if serializer.instance else "unknown"}/',
                    'atualizar_senha',
                    False
                )
            raise e
    
    def perform_destroy(self, instance):
        try:
            # Verificar permissões
            if not self.request.user.is_superuser:
                if not hasattr(self.request.user, 'perfil') or not self.request.user.perfil.pode_acessar_senhas:
                    logger.warning(f'Tentativa de excluir senha sem permissão: {self.request.user.username}')
                    raise PermissionError("Sem permissão para excluir senhas")
            
            # Registrar acesso antes de excluir
            if hasattr(self.request.user, 'perfil'):
                self.request.user.perfil.registrar_acesso(
                    self.request, 
                    f'/api/senhas/senhas/{instance.id}/',
                    'excluir_senha',
                    True
                )
            
            instance.delete()
        except Exception as e:
            # Registrar erro
            if hasattr(self.request.user, 'perfil'):
                self.request.user.perfil.registrar_acesso(
                    self.request, 
                    f'/api/senhas/senhas/{instance.id}/',
                    'excluir_senha',
                    False
                )
            raise e
    
    @action(detail=False, methods=['get'])
    def favoritos(self, request):
        """Retorna senhas marcadas como favoritas"""
        # Verificar permissões
        if not request.user.is_superuser:
            if not hasattr(request.user, 'perfil') or not request.user.perfil.pode_acessar_senhas:
                return Response({'error': 'Sem permissão'}, status=403)
        
        senhas = self.get_queryset().filter(favorito=True)
        print(f"Favoritos para usuário {request.user.username}: {senhas.count()} senhas")
        serializer = self.get_serializer(senhas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Busca senhas por título, URL ou usuário"""
        # Verificar permissões
        if not request.user.is_superuser:
            if not hasattr(request.user, 'perfil') or not request.user.perfil.pode_acessar_senhas:
                return Response({'error': 'Sem permissão'}, status=403)
        
        query = request.query_params.get('q', '')
        if query:
            senhas = self.get_queryset().filter(
                Q(titulo__icontains=query) |
                Q(url__icontains=query) |
                Q(usuario_login__icontains=query) |
                Q(observacoes__icontains=query)
            )
        else:
            senhas = self.get_queryset()
        
        serializer = self.get_serializer(senhas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_favorito(self, request, pk=None):
        """Alterna o status de favorito"""
        # Verificar permissões
        if not request.user.is_superuser:
            if not hasattr(request.user, 'perfil') or not request.user.perfil.pode_acessar_senhas:
                return Response({'error': 'Sem permissão'}, status=403)
        
        senha = self.get_object()
        senha.favorito = not senha.favorito
        senha.save()
        serializer = self.get_serializer(senha)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def revelar_senha(self, request, pk=None):
        """Revela a senha descriptografada"""
        # Verificar permissões
        if not request.user.is_superuser:
            if not hasattr(request.user, 'perfil') or not request.user.perfil.pode_acessar_senhas:
                return Response({'error': 'Sem permissão'}, status=403)
        
        senha = self.get_object()
        
        # Registrar acesso sensível
        if hasattr(request.user, 'perfil'):
            request.user.perfil.registrar_acesso(
                request, 
                f'/api/senhas/senhas/{senha.id}/revelar_senha/',
                'revelar_senha',
                True
            )
        
        return Response({
            'id': senha.id,
            'titulo': senha.titulo,
            'senha': senha.get_senha()
        })
    
    @action(detail=True, methods=['get'])
    def download_arquivo(self, request, pk=None):
        """Download do arquivo anexado"""
        # Verificar permissões
        if not request.user.is_superuser:
            if not hasattr(request.user, 'perfil') or not request.user.perfil.pode_acessar_senhas:
                return Response({'error': 'Sem permissão'}, status=403)
        
        senha = self.get_object()
        if not senha.arquivo:
            raise Http404("Arquivo não encontrado")
        
        try:
            response = FileResponse(senha.arquivo.open('rb'))
            response['Content-Disposition'] = f'attachment; filename="{senha.arquivo.name.split("/")[-1]}"'
            
            # Registrar download
            if hasattr(request.user, 'perfil'):
                request.user.perfil.registrar_acesso(
                    request, 
                    f'/api/senhas/senhas/{senha.id}/download_arquivo/',
                    'download_arquivo',
                    True
                )
            
            return response
        except Exception as e:
            print(f"Erro ao fazer download do arquivo: {e}")
            raise Http404("Erro ao processar arquivo")
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas das senhas do usuário"""
        # Verificar permissões
        if not request.user.is_superuser:
            if not hasattr(request.user, 'perfil') or not request.user.perfil.pode_acessar_senhas:
                return Response({'error': 'Sem permissão'}, status=403)
        
        queryset = self.get_queryset()
        total_senhas = queryset.count()
        favoritos = queryset.filter(favorito=True).count()
        com_arquivos = queryset.exclude(arquivo='').count()
        
        return Response({
            'total_senhas': total_senhas,
            'favoritos': favoritos,
            'com_arquivos': com_arquivos,
            'sem_arquivos': total_senhas - com_arquivos
        })
    
    @action(detail=False, methods=['get'])
    def categorias(self, request):
        """Retorna categorias baseadas nos títulos das senhas"""
        # Verificar permissões
        if not request.user.is_superuser:
            if not hasattr(request.user, 'perfil') or not request.user.perfil.pode_acessar_senhas:
                return Response({'error': 'Sem permissão'}, status=403)
        
        queryset = self.get_queryset()
        categorias = {}
        
        for senha in queryset:
            # Extrai categoria do título (ex: "Banco - Nubank" -> "Banco")
            if ' - ' in senha.titulo:
                categoria = senha.titulo.split(' - ')[0]
            else:
                categoria = 'Geral'
            
            if categoria not in categorias:
                categorias[categoria] = 0
            categorias[categoria] += 1
        
        return Response(categorias)

