from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class PerfilUsuario(models.Model):
    NIVEL_CHOICES = [
        ('admin', 'Administrador'),
        ('gerente', 'Gerente'),
        ('usuario', 'Usuário'),
        ('visualizador', 'Visualizador'),
    ]
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('suspenso', 'Suspenso'),
    ]
    
    # Relação com User do Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Informações do Perfil
    nivel_acesso = models.CharField(
        max_length=15, 
        choices=NIVEL_CHOICES, 
        default='usuario',
        verbose_name='Nível de Acesso'
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='ativo',
        verbose_name='Status'
    )
    
    # Informações Pessoais
    cpf = models.CharField(
        max_length=14, 
        blank=True,
        verbose_name='CPF',
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF deve estar no formato XXX.XXX.XXX-XX'
            )
        ]
    )
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    celular = models.CharField(max_length=20, blank=True, verbose_name='Celular')
    data_nascimento = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    
    # Endereço
    cep = models.CharField(max_length=9, blank=True, verbose_name='CEP')
    endereco = models.CharField(max_length=200, blank=True, verbose_name='Endereço')
    numero = models.CharField(max_length=10, blank=True, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, blank=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, blank=True, verbose_name='Cidade')
    estado = models.CharField(max_length=2, blank=True, verbose_name='Estado')
    
    # Informações Profissionais
    cargo = models.CharField(max_length=100, blank=True, verbose_name='Cargo')
    departamento = models.CharField(max_length=100, blank=True, verbose_name='Departamento')
    data_admissao = models.DateField(null=True, blank=True, verbose_name='Data de Admissão')
    
    # Configurações
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, verbose_name='Foto')
    tema_escuro = models.BooleanField(default=False, verbose_name='Tema Escuro')
    notificacoes_email = models.BooleanField(default=True, verbose_name='Notificações por E-mail')
    notificacoes_sistema = models.BooleanField(default=True, verbose_name='Notificações do Sistema')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    
    # Controle
    criado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='usuarios_criados',
        verbose_name='Criado por'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    ultimo_acesso = models.DateTimeField(null=True, blank=True, verbose_name='Último Acesso')
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuário'
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} ({self.get_nivel_acesso_display()})"
    
    def get_endereco_completo(self):
        """Retorna o endereço completo formatado"""
        endereco = f"{self.endereco}"
        if self.numero:
            endereco += f", {self.numero}"
        if self.complemento:
            endereco += f" - {self.complemento}"
        if self.bairro:
            endereco += f", {self.bairro}"
        if self.cidade:
            endereco += f", {self.cidade}"
        if self.estado:
            endereco += f" - {self.estado}"
        if self.cep:
            endereco += f", CEP: {self.cep}"
        return endereco
    
    def pode_gerenciar_usuarios(self):
        """Verifica se o usuário pode gerenciar outros usuários"""
        return self.nivel_acesso in ['admin', 'gerente']
    
    def pode_gerenciar_fornecedores(self):
        """Verifica se o usuário pode gerenciar fornecedores"""
        return self.nivel_acesso in ['admin', 'gerente', 'usuario']
    
    def pode_gerenciar_contas(self):
        """Verifica se o usuário pode gerenciar contas"""
        return self.nivel_acesso in ['admin', 'gerente', 'usuario']
    
    def pode_visualizar_relatorios(self):
        """Verifica se o usuário pode visualizar relatórios"""
        return self.nivel_acesso in ['admin', 'gerente', 'usuario']
    
    def pode_gerenciar_sistema(self):
        """Verifica se o usuário pode gerenciar configurações do sistema"""
        return self.nivel_acesso == 'admin'
    
    def pode_acessar_senhas(self):
        """Verifica se o usuário pode acessar o gerenciador de senhas"""
        return self.nivel_acesso in ['admin', 'gerente']
    
    def pode_gerenciar_senhas_outros_usuarios(self):
        """Verifica se o usuário pode gerenciar senhas de outros usuários"""
        return self.nivel_acesso == 'admin'
    
    def pode_exportar_senhas(self):
        """Verifica se o usuário pode exportar senhas"""
        return self.nivel_acesso in ['admin', 'gerente']
    
    def pode_visualizar_logs_senhas(self):
        """Verifica se o usuário pode visualizar logs de senhas"""
        return self.nivel_acesso == 'admin'
    
    def registrar_acesso(self, request, pagina, acao='acesso', sucesso=True):
        """Registra um acesso do usuário"""
        try:
            LogAcesso.objects.create(
                usuario=self,
                ip_address=request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                pagina_acessada=pagina,
                acao=acao,
                sucesso=sucesso
            )
        except Exception as e:
            # Log do erro mas não falhar a operação
            print(f"Erro ao registrar acesso: {e}")
    
    def atualizar_ultimo_acesso(self):
        """Atualiza o timestamp do último acesso"""
        from django.utils import timezone
        self.ultimo_acesso = timezone.now()
        self.save(update_fields=['ultimo_acesso'])

class Permissao(models.Model):
    """Permissões específicas do sistema"""
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    modulo = models.CharField(max_length=50, verbose_name='Módulo')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'
    
    def __str__(self):
        return f"{self.nome} ({self.modulo})"

class GrupoPermissao(models.Model):
    """Grupos de permissões para facilitar gestão"""
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    permissoes = models.ManyToManyField(Permissao, verbose_name='Permissões')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Grupo de Permissão'
        verbose_name_plural = 'Grupos de Permissão'
    
    def __str__(self):
        return self.nome

class UsuarioPermissao(models.Model):
    """Permissões específicas de usuários"""
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, verbose_name='Usuário')
    permissao = models.ForeignKey(Permissao, on_delete=models.CASCADE, verbose_name='Permissão')
    concedida_em = models.DateTimeField(auto_now_add=True, verbose_name='Concedida em')
    concedida_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Concedida por'
    )
    
    class Meta:
        unique_together = ['usuario', 'permissao']
        verbose_name = 'Permissão de Usuário'
        verbose_name_plural = 'Permissões de Usuário'
    
    def __str__(self):
        return f"{self.usuario} - {self.permissao}"

class LogAcesso(models.Model):
    """Log de acessos dos usuários"""
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, verbose_name='Usuário')
    data_acesso = models.DateTimeField(auto_now_add=True, verbose_name='Data de Acesso')
    ip_address = models.GenericIPAddressField(verbose_name='Endereço IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    pagina_acessada = models.CharField(max_length=200, blank=True, verbose_name='Página Acessada')
    acao = models.CharField(max_length=50, blank=True, verbose_name='Ação')
    sucesso = models.BooleanField(default=True, verbose_name='Sucesso')
    
    class Meta:
        ordering = ['-data_acesso']
        verbose_name = 'Log de Acesso'
        verbose_name_plural = 'Logs de Acesso'
    
    def __str__(self):
        return f"{self.usuario} - {self.data_acesso}" 