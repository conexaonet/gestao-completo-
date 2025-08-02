from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Fornecedor(models.Model):
    TIPO_CHOICES = [
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica'),
    ]
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('suspenso', 'Suspenso'),
    ]
    
    # Informações Básicas
    nome = models.CharField(max_length=200, verbose_name='Nome/Razão Social')
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='pj', verbose_name='Tipo')
    cnpj_cpf = models.CharField(
        max_length=18, 
        unique=True,
        verbose_name='CNPJ/CPF',
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message='CNPJ/CPF deve estar no formato correto'
            )
        ]
    )
    
    # Informações de Contato
    email = models.EmailField(blank=True, verbose_name='E-mail')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    celular = models.CharField(max_length=20, blank=True, verbose_name='Celular')
    website = models.URLField(blank=True, verbose_name='Website')
    
    # Endereço
    cep = models.CharField(max_length=9, blank=True, verbose_name='CEP')
    endereco = models.CharField(max_length=200, blank=True, verbose_name='Endereço')
    numero = models.CharField(max_length=10, blank=True, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, blank=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, blank=True, verbose_name='Cidade')
    estado = models.CharField(max_length=2, blank=True, verbose_name='Estado')
    
    # Informações Comerciais
    inscricao_estadual = models.CharField(max_length=20, blank=True, verbose_name='Inscrição Estadual')
    inscricao_municipal = models.CharField(max_length=20, blank=True, verbose_name='Inscrição Municipal')
    ramo_atividade = models.CharField(max_length=100, blank=True, verbose_name='Ramo de Atividade')
    
    # Informações Bancárias
    banco = models.CharField(max_length=100, blank=True, verbose_name='Banco')
    agencia = models.CharField(max_length=10, blank=True, verbose_name='Agência')
    conta = models.CharField(max_length=20, blank=True, verbose_name='Conta')
    tipo_conta = models.CharField(
        max_length=10, 
        choices=[('corrente', 'Corrente'), ('poupanca', 'Poupança')],
        blank=True,
        verbose_name='Tipo de Conta'
    )
    
    # Controle
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    favorito = models.BooleanField(default=False, verbose_name='Favorito')
    
    # Usuário responsável
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    
    # Timestamps
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
    
    def __str__(self):
        return self.nome
    
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
    
    def get_documento_formatado(self):
        """Retorna o CNPJ/CPF formatado"""
        return self.cnpj_cpf
    
    def get_contato_principal(self):
        """Retorna o contato principal (celular ou telefone)"""
        return self.celular if self.celular else self.telefone

class ContatoFornecedor(models.Model):
    """Contatos adicionais do fornecedor"""
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='contatos')
    nome = models.CharField(max_length=100, verbose_name='Nome')
    cargo = models.CharField(max_length=100, blank=True, verbose_name='Cargo')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    celular = models.CharField(max_length=20, blank=True, verbose_name='Celular')
    principal = models.BooleanField(default=False, verbose_name='Contato Principal')
    
    class Meta:
        verbose_name = 'Contato do Fornecedor'
        verbose_name_plural = 'Contatos do Fornecedor'
    
    def __str__(self):
        return f"{self.nome} - {self.fornecedor.nome}"

class CategoriaFornecedor(models.Model):
    """Categorias para classificar fornecedores"""
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    cor = models.CharField(max_length=7, default='#007bff', verbose_name='Cor')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Categoria de Fornecedor'
        verbose_name_plural = 'Categorias de Fornecedor'
    
    def __str__(self):
        return self.nome 