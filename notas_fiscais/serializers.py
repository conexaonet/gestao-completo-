from rest_framework import serializers
from .models import NotaFiscal, ItemNotaFiscal

class ItemNotaFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemNotaFiscal
        fields = [
            'id', 'codigo', 'descricao', 'quantidade', 'unidade',
            'valor_unitario', 'valor_total'
        ]
        read_only_fields = ['valor_total']

class NotaFiscalSerializer(serializers.ModelSerializer):
    itens = ItemNotaFiscalSerializer(many=True, read_only=True)
    total_itens = serializers.SerializerMethodField()
    
    class Meta:
        model = NotaFiscal
        fields = [
            'id', 'numero', 'serie', 'tipo', 'data_emissao', 'data_vencimento',
            'valor_total', 'valor_impostos', 'fornecedor_cliente', 'cnpj_cpf',
            'descricao', 'observacoes', 'status', 'arquivo', 'itens',
            'total_itens', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']
    
    def get_total_itens(self, obj):
        return obj.itens.count()

class NotaFiscalListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem"""
    total_itens = serializers.SerializerMethodField()
    
    class Meta:
        model = NotaFiscal
        fields = [
            'id', 'numero', 'serie', 'tipo', 'data_emissao',
            'valor_total', 'fornecedor_cliente', 'status',
            'total_itens', 'criado_em'
        ]
    
    def get_total_itens(self, obj):
        return obj.itens.count()

