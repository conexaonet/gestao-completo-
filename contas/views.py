from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Categoria, ContaPagar, DespesaDiaria
from .serializers import CategoriaSerializer, ContaPagarSerializer, DespesaDiariaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = []  # Permitir acesso público
    
    def get_queryset(self):
        return Categoria.objects.filter(ativo=True)

class ContaPagarViewSet(viewsets.ModelViewSet):
    serializer_class = ContaPagarSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ContaPagar.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        conta = serializer.save(usuario=self.request.user)
        
        # Se é parcelado, criar as outras parcelas
        if conta.eh_parcelado and conta.numero_parcelas > 1:
            self._criar_parcelas(conta)
    
    def _criar_parcelas(self, conta_principal):
        """Cria as parcelas adicionais para uma conta parcelada"""
        from datetime import timedelta
        from decimal import Decimal
        
        # Calcular valor da parcela (dividir o valor total pelo número de parcelas)
        valor_parcela = conta_principal.valor / conta_principal.numero_parcelas
        
        # Atualizar a primeira parcela (que já foi criada) com o valor correto
        conta_principal.valor = valor_parcela
        conta_principal.valor_parcela = valor_parcela
        conta_principal.save()
        
        # Criar as parcelas adicionais (a partir da segunda)
        for i in range(2, conta_principal.numero_parcelas + 1):
            # Calcular data de vencimento da parcela (30 dias após a anterior)
            # Usar a data de vencimento da primeira parcela como base
            data_vencimento = conta_principal.data_vencimento + timedelta(days=30 * (i - 1))
            
            ContaPagar.objects.create(
                descricao=conta_principal.descricao,
                valor=valor_parcela,
                data_vencimento=data_vencimento,
                status='pendente',
                categoria=conta_principal.categoria,
                observacoes=conta_principal.observacoes,
                usuario=conta_principal.usuario,
                eh_parcelado=True,
                numero_parcelas=conta_principal.numero_parcelas,
                parcela_atual=i,
                valor_parcela=valor_parcela,
                conta_principal=conta_principal
            )
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Retorna todas as contas pendentes"""
        contas = self.get_queryset().filter(status='pendente')
        
        total = contas.aggregate(total=Sum('valor'))['total'] or 0
        quantidade = contas.count()
        
        serializer = self.get_serializer(contas, many=True)
        
        return Response({
            'contas': serializer.data,
            'total': total,
            'quantidade': quantidade
        })
    
    @action(detail=False, methods=['get'])
    def hoje(self, request):
        """Retorna contas que vencem hoje"""
        hoje = timezone.now().date()
        contas = self.get_queryset().filter(
            status='pendente',
            data_vencimento=hoje
        )
        
        total = contas.aggregate(total=Sum('valor'))['total'] or 0
        quantidade = contas.count()
        
        serializer = self.get_serializer(contas, many=True)
        
        return Response({
            'contas': serializer.data,
            'total': total,
            'quantidade': quantidade,
            'data': hoje
        })

    @action(detail=False, methods=['get'])
    def amanha(self, request):
        """Retorna contas que vencem amanhã"""
        amanha = timezone.now().date() + timedelta(days=1)
        contas = self.get_queryset().filter(
            status='pendente',
            data_vencimento=amanha
        )
        
        total = contas.aggregate(total=Sum('valor'))['total'] or 0
        quantidade = contas.count()
        
        serializer = self.get_serializer(contas, many=True)
        
        return Response({
            'contas': serializer.data,
            'total': total,
            'quantidade': quantidade,
            'data': amanha
        })

    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        """Retorna contas vencidas que ainda não foram pagas"""
        hoje = timezone.now().date()
        contas = self.get_queryset().filter(
            status='pendente',
            data_vencimento__lt=hoje
        )
        
        total = contas.aggregate(total=Sum('valor'))['total'] or 0
        quantidade = contas.count()
        
        serializer = self.get_serializer(contas, many=True)
        
        return Response({
            'contas': serializer.data,
            'total': total,
            'quantidade': quantidade,
            'data': hoje
        })
    
    @action(detail=False, methods=['get'])
    def por_fornecedor(self, request):
        """Retorna contas agrupadas por fornecedor"""
        contas = self.get_queryset().filter(status='pendente')
        
        # Agrupar por descrição (fornecedor)
        fornecedores = {}
        for conta in contas:
            fornecedor = conta.descricao
            if fornecedor not in fornecedores:
                fornecedores[fornecedor] = {
                    'fornecedor': fornecedor,
                    'total_valor': 0,
                    'total_parcelas': 0,
                    'parcelas_pagas': 0,
                    'parcelas_pendentes': 0,
                    'primeiro_vencimento': None,
                    'ultimo_vencimento': None,
                    'categoria': conta.categoria.nome,
                    'categoria_cor': conta.categoria.cor,
                    'contas': []
                }
            
            fornecedores[fornecedor]['total_valor'] += float(conta.valor)
            fornecedores[fornecedor]['total_parcelas'] += 1
            
            if conta.status == 'pago':
                fornecedores[fornecedor]['parcelas_pagas'] += 1
            else:
                fornecedores[fornecedor]['parcelas_pendentes'] += 1
            
            if not fornecedores[fornecedor]['primeiro_vencimento'] or conta.data_vencimento < fornecedores[fornecedor]['primeiro_vencimento']:
                fornecedores[fornecedor]['primeiro_vencimento'] = conta.data_vencimento
            
            if not fornecedores[fornecedor]['ultimo_vencimento'] or conta.data_vencimento > fornecedores[fornecedor]['ultimo_vencimento']:
                fornecedores[fornecedor]['ultimo_vencimento'] = conta.data_vencimento
            
            fornecedores[fornecedor]['contas'].append({
                'id': conta.id,
                'valor': conta.valor,
                'data_vencimento': conta.data_vencimento,
                'status': conta.status,
                'eh_parcelado': conta.eh_parcelado,
                'parcela_atual': conta.parcela_atual,
                'numero_parcelas': conta.numero_parcelas
            })
        
        # Ordenar por total de valor (maior primeiro)
        resultado = list(fornecedores.values())
        resultado.sort(key=lambda x: x['total_valor'], reverse=True)
        
        return Response(resultado)
    
    @action(detail=True, methods=['post'])
    def marcar_pago(self, request, pk=None):
        """Marca uma conta como paga"""
        conta = self.get_object()
        conta.status = 'pago'
        conta.data_pagamento = timezone.now().date()
        conta.save()
        serializer = self.get_serializer(conta)
        return Response(serializer.data)

class DespesaDiariaViewSet(viewsets.ModelViewSet):
    serializer_class = DespesaDiariaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = DespesaDiaria.objects.filter(usuario=self.request.user)
        
        # Filtros
        data_inicial = self.request.query_params.get('data_inicial')
        data_final = self.request.query_params.get('data_final')
        categoria = self.request.query_params.get('categoria')
        search = self.request.query_params.get('search')
        
        if data_inicial:
            queryset = queryset.filter(data__gte=data_inicial)
        
        if data_final:
            queryset = queryset.filter(data__lte=data_final)
        
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
        
        if search:
            queryset = queryset.filter(
                Q(descricao__icontains=search) | 
                Q(observacoes__icontains=search)
            )
        
        return queryset.order_by('-data')
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def resumo_mensal(self, request):
        """Retorna resumo de despesas do período"""
        data_inicial = request.query_params.get('data_inicial')
        data_final = request.query_params.get('data_final')
        
        queryset = self.get_queryset()
        
        # Se não especificou datas, usar mês atual
        if not data_inicial and not data_final:
            hoje = timezone.now().date()
            inicio_mes = hoje.replace(day=1)
            queryset = queryset.filter(
                data__gte=inicio_mes,
                data__lte=hoje
            )
        
        total = queryset.aggregate(total=Sum('valor'))['total'] or 0
        quantidade = queryset.count()
        
        return Response({
            'total_mes': total,
            'quantidade': quantidade,
            'media_diaria': total / quantidade if quantidade > 0 else 0,
            'periodo': {
                'inicio': data_inicial,
                'fim': data_final
            }
        })
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Retorna despesas agrupadas por categoria"""
        queryset = self.get_queryset()
        
        # Agrupar por categoria
        categorias = {}
        for despesa in queryset:
            cat_nome = despesa.categoria.nome
            if cat_nome not in categorias:
                categorias[cat_nome] = {
                    'nome': cat_nome,
                    'cor': despesa.categoria.cor,
                    'total': 0,
                    'quantidade': 0
                }
            
            categorias[cat_nome]['total'] += float(despesa.valor)
            categorias[cat_nome]['quantidade'] += 1
        
        return Response(list(categorias.values()))

class RelatorioViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def mensal(self, request):
        """Relatório mensal de contas e despesas"""
        mes = request.query_params.get('mes', timezone.now().month)
        ano = request.query_params.get('ano', timezone.now().year)
        
        # Calcular datas do mês
        data_inicio = datetime(ano, mes, 1).date()
        if mes == 12:
            data_fim = datetime(ano + 1, 1, 1).date() - timedelta(days=1)
        else:
            data_fim = datetime(ano, mes + 1, 1).date() - timedelta(days=1)
        
        # Contas do mês
        contas_mes = ContaPagar.objects.filter(
            usuario=request.user,
            data_vencimento__gte=data_inicio,
            data_vencimento__lte=data_fim
        )
        
        # Despesas do mês
        despesas_mes = DespesaDiaria.objects.filter(
            usuario=request.user,
            data__gte=data_inicio,
            data__lte=data_fim
        )
        
        # Estatísticas de contas
        contas_pendentes = contas_mes.filter(status='pendente')
        contas_pagas = contas_mes.filter(status='pago')
        
        total_contas_pendentes = contas_pendentes.aggregate(total=Sum('valor'))['total'] or 0
        total_contas_pagas = contas_pagas.aggregate(total=Sum('valor'))['total'] or 0
        total_despesas = despesas_mes.aggregate(total=Sum('valor'))['total'] or 0
        
        # Contas por categoria
        contas_por_categoria = {}
        for conta in contas_mes:
            cat_nome = conta.categoria.nome
            if cat_nome not in contas_por_categoria:
                contas_por_categoria[cat_nome] = {
                    'nome': cat_nome,
                    'cor': conta.categoria.cor,
                    'pendente': 0,
                    'pago': 0,
                    'total': 0
                }
            
            contas_por_categoria[cat_nome]['total'] += float(conta.valor)
            if conta.status == 'pendente':
                contas_por_categoria[cat_nome]['pendente'] += float(conta.valor)
            else:
                contas_por_categoria[cat_nome]['pago'] += float(conta.valor)
        
        # Despesas por categoria
        despesas_por_categoria = {}
        for despesa in despesas_mes:
            cat_nome = despesa.categoria.nome
            if cat_nome not in despesas_por_categoria:
                despesas_por_categoria[cat_nome] = {
                    'nome': cat_nome,
                    'cor': despesa.categoria.cor,
                    'total': 0,
                    'quantidade': 0
                }
            
            despesas_por_categoria[cat_nome]['total'] += float(despesa.valor)
            despesas_por_categoria[cat_nome]['quantidade'] += 1
        
        return Response({
            'periodo': {
                'mes': mes,
                'ano': ano,
                'data_inicio': data_inicio,
                'data_fim': data_fim
            },
            'resumo': {
                'contas_pendentes': total_contas_pendentes,
                'contas_pagas': total_contas_pagas,
                'total_contas': total_contas_pendentes + total_contas_pagas,
                'despesas': total_despesas,
                'saldo': (total_contas_pagas - total_despesas)
            },
            'contas_por_categoria': list(contas_por_categoria.values()),
            'despesas_por_categoria': list(despesas_por_categoria.values()),
            'contas_pendentes_detalhadas': ContaPagarSerializer(contas_pendentes, many=True).data,
            'contas_pagas_detalhadas': ContaPagarSerializer(contas_pagas, many=True).data,
            'despesas_detalhadas': DespesaDiariaSerializer(despesas_mes, many=True).data
        })
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Análise detalhada por categoria"""
        data_inicial = request.query_params.get('data_inicial')
        data_final = request.query_params.get('data_final')
        
        # Se não especificou datas, usar últimos 6 meses
        if not data_inicial and not data_final:
            hoje = timezone.now().date()
            data_final = hoje
            data_inicial = hoje - timedelta(days=180)
        
        # Contas por categoria
        contas = ContaPagar.objects.filter(
            usuario=request.user,
            data_vencimento__gte=data_inicial,
            data_vencimento__lte=data_final
        )
        
        # Despesas por categoria
        despesas = DespesaDiaria.objects.filter(
            usuario=request.user,
            data__gte=data_inicial,
            data__lte=data_final
        )
        
        # Agrupar contas por categoria
        contas_por_categoria = {}
        for conta in contas:
            cat_nome = conta.categoria.nome
            if cat_nome not in contas_por_categoria:
                contas_por_categoria[cat_nome] = {
                    'nome': cat_nome,
                    'cor': conta.categoria.cor,
                    'contas_pendentes': 0,
                    'contas_pagas': 0,
                    'total_contas': 0,
                    'quantidade_contas': 0,
                    'despesas': 0,
                    'quantidade_despesas': 0
                }
            
            contas_por_categoria[cat_nome]['total_contas'] += float(conta.valor)
            contas_por_categoria[cat_nome]['quantidade_contas'] += 1
            
            if conta.status == 'pendente':
                contas_por_categoria[cat_nome]['contas_pendentes'] += float(conta.valor)
            else:
                contas_por_categoria[cat_nome]['contas_pagas'] += float(conta.valor)
        
        # Agrupar despesas por categoria
        for despesa in despesas:
            cat_nome = despesa.categoria.nome
            if cat_nome not in contas_por_categoria:
                contas_por_categoria[cat_nome] = {
                    'nome': cat_nome,
                    'cor': despesa.categoria.cor,
                    'contas_pendentes': 0,
                    'contas_pagas': 0,
                    'total_contas': 0,
                    'quantidade_contas': 0,
                    'despesas': 0,
                    'quantidade_despesas': 0
                }
            
            contas_por_categoria[cat_nome]['despesas'] += float(despesa.valor)
            contas_por_categoria[cat_nome]['quantidade_despesas'] += 1
        
        # Calcular totais e percentuais
        resultado = []
        for categoria in contas_por_categoria.values():
            total_categoria = categoria['total_contas'] + categoria['despesas']
            categoria['total_geral'] = total_categoria
            categoria['percentual_contas'] = (categoria['total_contas'] / total_categoria * 100) if total_categoria > 0 else 0
            categoria['percentual_despesas'] = (categoria['despesas'] / total_categoria * 100) if total_categoria > 0 else 0
            resultado.append(categoria)
        
        # Ordenar por total geral
        resultado.sort(key=lambda x: x['total_geral'], reverse=True)
        
        return Response({
            'periodo': {
                'inicio': data_inicial,
                'fim': data_final
            },
            'categorias': resultado,
            'resumo': {
                'total_contas': sum(cat['total_contas'] for cat in resultado),
                'total_despesas': sum(cat['despesas'] for cat in resultado),
                'total_geral': sum(cat['total_geral'] for cat in resultado)
            }
        })
    
    @action(detail=False, methods=['get'])
    def evolucao_gastos(self, request):
        """Evolução de gastos ao longo do tempo"""
        meses = int(request.query_params.get('meses', 6))
        
        hoje = timezone.now().date()
        data_inicial = hoje - timedelta(days=meses * 30)
        
        # Gerar lista de meses
        meses_dados = []
        for i in range(meses):
            data_mes = hoje - timedelta(days=i * 30)
            mes_inicio = data_mes.replace(day=1)
            if data_mes.month == 12:
                mes_fim = data_mes.replace(year=data_mes.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                mes_fim = data_mes.replace(month=data_mes.month + 1, day=1) - timedelta(days=1)
            
            # Contas do mês
            contas_mes = ContaPagar.objects.filter(
                usuario=request.user,
                data_vencimento__gte=mes_inicio,
                data_vencimento__lte=mes_fim
            )
            
            # Despesas do mês
            despesas_mes = DespesaDiaria.objects.filter(
                usuario=request.user,
                data__gte=mes_inicio,
                data__lte=mes_fim
            )
            
            total_contas = contas_mes.aggregate(total=Sum('valor'))['total'] or 0
            total_despesas = despesas_mes.aggregate(total=Sum('valor'))['total'] or 0
            
            meses_dados.append({
                'mes': mes_inicio.strftime('%B/%Y'),
                'mes_numero': mes_inicio.month,
                'ano': mes_inicio.year,
                'contas': float(total_contas),
                'despesas': float(total_despesas),
                'total': float(total_contas + total_despesas),
                'quantidade_contas': contas_mes.count(),
                'quantidade_despesas': despesas_mes.count()
            })
        
        # Ordenar por data (mais antigo primeiro)
        meses_dados.reverse()
        
        return Response({
            'periodo_meses': meses,
            'dados': meses_dados,
            'resumo': {
                'total_contas': sum(mes['contas'] for mes in meses_dados),
                'total_despesas': sum(mes['despesas'] for mes in meses_dados),
                'total_geral': sum(mes['total'] for mes in meses_dados),
                'media_mensal_contas': sum(mes['contas'] for mes in meses_dados) / len(meses_dados),
                'media_mensal_despesas': sum(mes['despesas'] for mes in meses_dados) / len(meses_dados)
            }
        })

