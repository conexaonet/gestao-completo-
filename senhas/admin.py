from django.contrib import admin
from .models import GerenciadorSenhas, ChaveCriptografia

@admin.register(GerenciadorSenhas)
class GerenciadorSenhasAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario_login', 'url', 'favorito', 'arquivo', 'usuario', 'atualizado_em']
    list_filter = ['favorito', 'criado_em', 'atualizado_em']
    search_fields = ['titulo', 'usuario_login', 'url', 'observacoes']
    ordering = ['-atualizado_em']
    readonly_fields = ['senha_criptografada', 'criado_em', 'atualizado_em']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

@admin.register(ChaveCriptografia)
class ChaveCriptografiaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'criado_em']
    readonly_fields = ['chave', 'criado_em']
    
    def has_add_permission(self, request):
        return False  # Não permite adicionar manualmente
    
    def has_change_permission(self, request, obj=None):
        return False  # Não permite editar

