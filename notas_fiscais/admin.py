from django.contrib import admin
from .models import NotaFiscal, ItemNotaFiscal

class ItemNotaFiscalInline(admin.TabularInline):
    model = ItemNotaFiscal
    extra = 1
    fields = ['codigo', 'descricao', 'quantidade', 'unidade', 'valor_unitario', 'valor_total']
    readonly_fields = ['valor_total']

@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = ['numero', 'serie', 'tipo', 'data_emissao', 'fornecedor_cliente', 'valor_total', 'status', 'usuario']
    list_filter = ['tipo', 'status', 'data_emissao', 'criado_em']
    search_fields = ['numero', 'serie', 'fornecedor_cliente', 'cnpj_cpf', 'descricao']
    date_hierarchy = 'data_emissao'
    ordering = ['-data_emissao']
    inlines = [ItemNotaFiscalInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero', 'serie', 'tipo', 'status')
        }),
        ('Datas', {
            'fields': ('data_emissao', 'data_vencimento')
        }),
        ('Valores', {
            'fields': ('valor_total', 'valor_impostos')
        }),
        ('Fornecedor/Cliente', {
            'fields': ('fornecedor_cliente', 'cnpj_cpf')
        }),
        ('Detalhes', {
            'fields': ('descricao', 'observacoes', 'arquivo')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

@admin.register(ItemNotaFiscal)
class ItemNotaFiscalAdmin(admin.ModelAdmin):
    list_display = ['nota_fiscal', 'codigo', 'descricao', 'quantidade', 'unidade', 'valor_unitario', 'valor_total']
    list_filter = ['unidade', 'nota_fiscal__tipo']
    search_fields = ['codigo', 'descricao', 'nota_fiscal__numero']
    readonly_fields = ['valor_total']

