from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Fornecedor, ContatoFornecedor, CategoriaFornecedor
from .serializers import (
    FornecedorSerializer, 
    FornecedorListSerializer, 
    FornecedorDetailSerializer,
    ContatoFornecedorSerializer,
    CategoriaFornecedorSerializer
)

# Views para páginas web
@login_required
def fornecedores_view(request):
    """Página principal de fornecedores"""
    return render(request, 'fornecedores.html')

@login_required
def novo_fornecedor_view(request):
    """Página para adicionar novo fornecedor"""
    return render(request, 'novo_fornecedor.html')

@login_required
def detalhe_fornecedor_view(request, pk):
    """Página de detalhes do fornecedor"""
    return render(request, 'detalhe_fornecedor.html')

@login_required
def editar_fornecedor_view(request, pk):
    """Página para editar fornecedor"""
    return render(request, 'editar_fornecedor.html')

# Views para API
class FornecedorViewSet(viewsets.ModelViewSet):
    permission_classes = []  # Permitir acesso público para listagem
    
    def get_queryset(self):
        # Se o usuário está autenticado, filtrar por usuário
        if self.request.user.is_authenticated:
            return Fornecedor.objects.filter(usuario=self.request.user)
        # Se não está autenticado, retornar todos os fornecedores ativos
        return Fornecedor.objects.filter(status='ativo')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FornecedorListSerializer
        elif self.action == 'retrieve':
            return FornecedorDetailSerializer
        return FornecedorSerializer
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def favoritos(self, request):
        """Retorna fornecedores marcados como favoritos"""
        fornecedores = self.get_queryset().filter(favorito=True)
        serializer = self.get_serializer(fornecedores, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Busca fornecedores por nome, CNPJ/CPF ou cidade"""
        query = request.query_params.get('q', '')
        if query:
            fornecedores = self.get_queryset().filter(
                Q(nome__icontains=query) |
                Q(cnpj_cpf__icontains=query) |
                Q(cidade__icontains=query) |
                Q(ramo_atividade__icontains=query)
            )
        else:
            fornecedores = self.get_queryset()
        
        serializer = self.get_serializer(fornecedores, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_favorito(self, request, pk=None):
        """Alterna o status de favorito"""
        fornecedor = self.get_object()
        fornecedor.favorito = not fornecedor.favorito
        fornecedor.save()
        serializer = self.get_serializer(fornecedor)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_cidade(self, request):
        """Agrupa fornecedores por cidade"""
        fornecedores = self.get_queryset().filter(status='ativo')
        
        cidades = {}
        for fornecedor in fornecedores:
            cidade = fornecedor.cidade or 'Sem cidade'
            if cidade not in cidades:
                cidades[cidade] = {
                    'cidade': cidade,
                    'estado': fornecedor.estado,
                    'quantidade': 0,
                    'total_contas': 0,
                    'fornecedores': []
                }
            
            cidades[cidade]['quantidade'] += 1
            
            # Calcular total de contas pendentes
            from contas.models import ContaPagar
            total_contas = ContaPagar.objects.filter(
                fornecedor=fornecedor,
                status='pendente'
            ).aggregate(total=Sum('valor'))['total'] or 0
            cidades[cidade]['total_contas'] += float(total_contas)
            
            cidades[cidade]['fornecedores'].append({
                'id': fornecedor.id,
                'nome': fornecedor.nome,
                'tipo': fornecedor.tipo,
                'telefone': fornecedor.telefone,
                'email': fornecedor.email
            })
        
        # Ordenar por quantidade de fornecedores
        resultado = list(cidades.values())
        resultado.sort(key=lambda x: x['quantidade'], reverse=True)
        
        return Response(resultado)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Estatísticas gerais dos fornecedores"""
        fornecedores = self.get_queryset()
        
        # Estatísticas básicas
        total_fornecedores = fornecedores.count()
        fornecedores_ativos = fornecedores.filter(status='ativo').count()
        fornecedores_favoritos = fornecedores.filter(favorito=True).count()
        
        # Por tipo
        pf_count = fornecedores.filter(tipo='pf').count()
        pj_count = fornecedores.filter(tipo='pj').count()
        
        # Por status
        inativos_count = fornecedores.filter(status='inativo').count()
        suspensos_count = fornecedores.filter(status='suspenso').count()
        
        # Top fornecedores por valor de contas
        from contas.models import ContaPagar
        from django.db.models import Sum
        
        top_fornecedores = []
        for fornecedor in fornecedores:
            total_contas = ContaPagar.objects.filter(
                fornecedor=fornecedor,
                status='pendente'
            ).aggregate(total=Sum('valor'))['total'] or 0
            
            if total_contas > 0:
                top_fornecedores.append({
                    'id': fornecedor.id,
                    'nome': fornecedor.nome,
                    'total_contas': float(total_contas),
                    'quantidade_contas': ContaPagar.objects.filter(
                        fornecedor=fornecedor,
                        status='pendente'
                    ).count()
                })
        
        # Ordenar por total de contas
        top_fornecedores.sort(key=lambda x: x['total_contas'], reverse=True)
        top_fornecedores = top_fornecedores[:10]  # Top 10
        
        return Response({
            'resumo': {
                'total_fornecedores': total_fornecedores,
                'fornecedores_ativos': fornecedores_ativos,
                'fornecedores_favoritos': fornecedores_favoritos,
                'pessoa_fisica': pf_count,
                'pessoa_juridica': pj_count,
                'inativos': inativos_count,
                'suspensos': suspensos_count
            },
            'top_fornecedores': top_fornecedores,
            'distribuicao_tipo': {
                'pessoa_fisica': pf_count,
                'pessoa_juridica': pj_count
            },
            'distribuicao_status': {
                'ativo': fornecedores_ativos,
                'inativo': inativos_count,
                'suspenso': suspensos_count
            }
        })

class ContatoFornecedorViewSet(viewsets.ModelViewSet):
    serializer_class = ContatoFornecedorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ContatoFornecedor.objects.filter(fornecedor__usuario=self.request.user)
    
    def perform_create(self, serializer):
        fornecedor_id = self.request.data.get('fornecedor')
        fornecedor = Fornecedor.objects.get(id=fornecedor_id, usuario=self.request.user)
        serializer.save(fornecedor=fornecedor)

class CategoriaFornecedorViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaFornecedorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CategoriaFornecedor.objects.filter(ativo=True)
    
    @action(detail=False, methods=['get'])
    def com_fornecedores(self, request):
        """Retorna categorias com contagem de fornecedores"""
        categorias = self.get_queryset()
        
        resultado = []
        for categoria in categorias:
            fornecedores_count = Fornecedor.objects.filter(
                usuario=request.user,
                status='ativo'
            ).count()  # Aqui você pode adicionar um campo categoria ao modelo Fornecedor se necessário
            
            resultado.append({
                'id': categoria.id,
                'nome': categoria.nome,
                'cor': categoria.cor,
                'descricao': categoria.descricao,
                'fornecedores_count': fornecedores_count
            })
        
        return Response(resultado) 