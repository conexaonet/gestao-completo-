from django.contrib import admin
from .models import Categoria, ContaPagar, DespesaDiaria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cor', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome']
    ordering = ['nome']

@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'valor', 'data_vencimento', 'status', 'categoria', 'fornecedor', 'usuario']
    list_filter = ['status', 'categoria', 'data_vencimento', 'criado_em']
    search_fields = ['descricao', 'observacoes']
    date_hierarchy = 'data_vencimento'
    ordering = ['-data_vencimento']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

@admin.register(DespesaDiaria)
class DespesaDiariaAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'valor', 'data', 'categoria', 'usuario']
    list_filter = ['categoria', 'data']
    search_fields = ['descricao', 'observacoes']
    date_hierarchy = 'data'
    ordering = ['-data']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

