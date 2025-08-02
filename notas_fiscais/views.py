from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import NotaFiscal, ItemNotaFiscal
from .serializers import NotaFiscalSerializer, NotaFiscalListSerializer, ItemNotaFiscalSerializer

class NotaFiscalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return NotaFiscal.objects.filter(usuario=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NotaFiscalListSerializer
        return NotaFiscalSerializer
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def entradas(self, request):
        """Retorna notas fiscais de entrada"""
        notas = self.get_queryset().filter(tipo='entrada')
        serializer = self.get_serializer(notas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def saidas(self, request):
        """Retorna notas fiscais de saída"""
        notas = self.get_queryset().filter(tipo='saida')
        serializer = self.get_serializer(notas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Retorna notas fiscais pendentes"""
        notas = self.get_queryset().filter(status='pendente')
        serializer = self.get_serializer(notas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def resumo_mensal(self, request):
        """Retorna resumo de notas fiscais do mês atual"""
        hoje = timezone.now().date()
        inicio_mes = hoje.replace(day=1)
        
        notas = self.get_queryset().filter(
            data_emissao__gte=inicio_mes,
            data_emissao__lte=hoje
        )
        
        entradas = notas.filter(tipo='entrada').aggregate(
            total=Sum('valor_total')
        )['total'] or 0
        
        saidas = notas.filter(tipo='saida').aggregate(
            total=Sum('valor_total')
        )['total'] or 0
        
        return Response({
            'periodo': {
                'inicio': inicio_mes,
                'fim': hoje
            },
            'entradas': {
                'total': entradas,
                'quantidade': notas.filter(tipo='entrada').count()
            },
            'saidas': {
                'total': saidas,
                'quantidade': notas.filter(tipo='saida').count()
            },
            'saldo': entradas - saidas
        })
    
    @action(detail=True, methods=['post'])
    def processar(self, request, pk=None):
        """Marca uma nota fiscal como processada"""
        nota = self.get_object()
        nota.status = 'processada'
        nota.save()
        serializer = self.get_serializer(nota)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancela uma nota fiscal"""
        nota = self.get_object()
        nota.status = 'cancelada'
        nota.save()
        serializer = self.get_serializer(nota)
        return Response(serializer.data)

class ItemNotaFiscalViewSet(viewsets.ModelViewSet):
    serializer_class = ItemNotaFiscalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ItemNotaFiscal.objects.filter(nota_fiscal__usuario=self.request.user)

