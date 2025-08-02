from django.contrib import admin
from .models import Fornecedor, ContatoFornecedor, CategoriaFornecedor

@admin.register(CategoriaFornecedor)
class CategoriaFornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cor', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'cnpj_cpf', 'cidade', 'estado', 'status', 'favorito', 'usuario']
    list_filter = ['tipo', 'status', 'favorito', 'cidade', 'estado']
    search_fields = ['nome', 'cnpj_cpf', 'email', 'cidade']
    date_hierarchy = 'criado_em'
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo', 'cnpj_cpf', 'ramo_atividade')
        }),
        ('Contato', {
            'fields': ('email', 'telefone', 'celular', 'website')
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Informações Comerciais', {
            'fields': ('inscricao_estadual', 'inscricao_municipal')
        }),
        ('Informações Bancárias', {
            'fields': ('banco', 'agencia', 'conta', 'tipo_conta')
        }),
        ('Controle', {
            'fields': ('status', 'favorito', 'observacoes', 'usuario')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

@admin.register(ContatoFornecedor)
class ContatoFornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cargo', 'email', 'telefone', 'fornecedor', 'principal']
    list_filter = ['principal', 'fornecedor']
    search_fields = ['nome', 'email', 'fornecedor__nome']
    ordering = ['fornecedor', 'nome'] 