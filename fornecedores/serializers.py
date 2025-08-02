from rest_framework import serializers
from .models import Fornecedor, ContatoFornecedor, CategoriaFornecedor

class CategoriaFornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaFornecedor
        fields = '__all__'

class ContatoFornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoFornecedor
        fields = '__all__'

class FornecedorSerializer(serializers.ModelSerializer):
    contatos = ContatoFornecedorSerializer(many=True, read_only=True)
    endereco_completo = serializers.ReadOnlyField()
    documento_formatado = serializers.ReadOnlyField()
    contato_principal = serializers.ReadOnlyField()
    
    class Meta:
        model = Fornecedor
        fields = '__all__'
        read_only_fields = ['usuario', 'criado_em', 'atualizado_em']
    
    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

class FornecedorListSerializer(serializers.ModelSerializer):
    contatos_count = serializers.SerializerMethodField()
    contas_count = serializers.SerializerMethodField()
    total_contas = serializers.SerializerMethodField()
    
    class Meta:
        model = Fornecedor
        fields = [
            'id', 'nome', 'tipo', 'cnpj_cpf', 'email', 'telefone', 'celular',
            'cidade', 'estado', 'status', 'favorito', 'contatos_count',
            'contas_count', 'total_contas', 'criado_em'
        ]
    
    def get_contatos_count(self, obj):
        return obj.contatos.count()
    
    def get_contas_count(self, obj):
        from contas.models import ContaPagar
        return ContaPagar.objects.filter(fornecedor=obj).count()
    
    def get_total_contas(self, obj):
        from contas.models import ContaPagar
        from django.db.models import Sum
        total = ContaPagar.objects.filter(
            fornecedor=obj, 
            status='pendente'
        ).aggregate(total=Sum('valor'))['total'] or 0
        return float(total)

class FornecedorDetailSerializer(serializers.ModelSerializer):
    contatos = ContatoFornecedorSerializer(many=True, read_only=True)
    endereco_completo = serializers.ReadOnlyField()
    documento_formatado = serializers.ReadOnlyField()
    contato_principal = serializers.ReadOnlyField()
    contas_pendentes = serializers.SerializerMethodField()
    contas_pagas = serializers.SerializerMethodField()
    total_pendente = serializers.SerializerMethodField()
    total_pago = serializers.SerializerMethodField()
    
    class Meta:
        model = Fornecedor
        fields = '__all__'
    
    def get_contas_pendentes(self, obj):
        from contas.models import ContaPagar
        contas = ContaPagar.objects.filter(
            fornecedor=obj, 
            status='pendente'
        ).order_by('data_vencimento')
        
        return [{
            'id': conta.id,
            'descricao': conta.descricao,
            'valor': float(conta.valor),
            'data_vencimento': conta.data_vencimento,
            'status': conta.status,
            'categoria': conta.categoria.nome
        } for conta in contas]
    
    def get_contas_pagas(self, obj):
        from contas.models import ContaPagar
        contas = ContaPagar.objects.filter(
            fornecedor=obj, 
            status='pago'
        ).order_by('-data_pagamento')
        
        return [{
            'id': conta.id,
            'descricao': conta.descricao,
            'valor': float(conta.valor),
            'data_pagamento': conta.data_pagamento,
            'categoria': conta.categoria.nome
        } for conta in contas]
    
    def get_total_pendente(self, obj):
        from contas.models import ContaPagar
        from django.db.models import Sum
        total = ContaPagar.objects.filter(
            fornecedor=obj, 
            status='pendente'
        ).aggregate(total=Sum('valor'))['total'] or 0
        return float(total)
    
    def get_total_pago(self, obj):
        from contas.models import ContaPagar
        from django.db.models import Sum
        total = ContaPagar.objects.filter(
            fornecedor=obj, 
            status='pago'
        ).aggregate(total=Sum('valor'))['total'] or 0
        return float(total) 