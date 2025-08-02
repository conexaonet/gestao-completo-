from rest_framework import serializers
from .models import Categoria, ContaPagar, DespesaDiaria
from fornecedores.models import Fornecedor

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['id', 'nome', 'tipo', 'cnpj_cpf', 'cidade', 'estado']

class ContaPagarSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.IntegerField(write_only=True)
    fornecedor = FornecedorSerializer(read_only=True)
    fornecedor_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    valor_formatado = serializers.ReadOnlyField()
    status_display_class = serializers.ReadOnlyField()
    esta_vencida = serializers.ReadOnlyField()
    dias_para_vencimento = serializers.ReadOnlyField()
    
    class Meta:
        model = ContaPagar
        fields = '__all__'
        read_only_fields = ['usuario', 'criado_em', 'atualizado_em']
    
    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

class ContaPagarListSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    fornecedor = FornecedorSerializer(read_only=True)
    valor_formatado = serializers.ReadOnlyField()
    status_display_class = serializers.ReadOnlyField()
    esta_vencida = serializers.ReadOnlyField()
    dias_para_vencimento = serializers.ReadOnlyField()
    
    class Meta:
        model = ContaPagar
        fields = [
            'id', 'descricao', 'valor', 'valor_formatado', 'data_vencimento',
            'status', 'status_display_class', 'categoria', 'fornecedor',
            'eh_parcelado', 'numero_parcelas', 'parcela_atual', 'esta_vencida',
            'dias_para_vencimento', 'observacoes', 'criado_em'
        ]

class DespesaDiariaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.IntegerField(write_only=True)
    valor_formatado = serializers.ReadOnlyField()
    
    class Meta:
        model = DespesaDiaria
        fields = '__all__'
        read_only_fields = ['usuario', 'criado_em']
    
    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

