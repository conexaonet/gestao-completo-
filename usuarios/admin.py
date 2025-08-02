from django.contrib import admin
from .models import PerfilUsuario, Permissao, GrupoPermissao, UsuarioPermissao, LogAcesso

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nivel_acesso', 'status', 'cargo', 'departamento', 'ultimo_acesso']
    list_filter = ['nivel_acesso', 'status', 'departamento']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'cargo']
    date_hierarchy = 'criado_em'
    ordering = ['usuario__username']
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('usuario', 'nivel_acesso', 'status')
        }),
        ('Informações Pessoais', {
            'fields': ('cpf', 'telefone', 'celular', 'data_nascimento')
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Informações Profissionais', {
            'fields': ('cargo', 'departamento', 'data_admissao')
        }),
        ('Configurações', {
            'fields': ('foto', 'tema_escuro', 'notificacoes_email', 'notificacoes_sistema')
        }),
        ('Controle', {
            'fields': ('criado_por', 'ultimo_acesso')
        }),
    )
    
    readonly_fields = ['criado_em', 'atualizado_em', 'ultimo_acesso']

@admin.register(Permissao)
class PermissaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'modulo', 'ativo']
    list_filter = ['modulo', 'ativo']
    search_fields = ['nome', 'codigo', 'descricao']
    ordering = ['modulo', 'nome']

@admin.register(GrupoPermissao)
class GrupoPermissaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'descricao']
    filter_horizontal = ['permissoes']
    ordering = ['nome']

@admin.register(UsuarioPermissao)
class UsuarioPermissaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'permissao', 'concedida_em', 'concedida_por']
    list_filter = ['permissao', 'concedida_em']
    search_fields = ['usuario__usuario__username', 'permissao__nome']
    date_hierarchy = 'concedida_em'
    ordering = ['-concedida_em']

@admin.register(LogAcesso)
class LogAcessoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'data_acesso', 'ip_address', 'pagina_acessada', 'sucesso']
    list_filter = ['sucesso', 'data_acesso']
    search_fields = ['usuario__usuario__username', 'ip_address', 'pagina_acessada']
    date_hierarchy = 'data_acesso'
    ordering = ['-data_acesso']
    readonly_fields = ['data_acesso'] 