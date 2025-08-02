from django.db import models
from django.contrib.auth.models import User
from fornecedores.models import Fornecedor

class Categoria(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    cor = models.CharField(max_length=7, default='#007bff', verbose_name='Cor')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return self.nome

class ContaPagar(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('vencido', 'Vencido'),
        ('cancelado', 'Cancelado'),
    ]
    
    # Informações Básicas
    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    data_vencimento = models.DateField(verbose_name='Data de Vencimento')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    
    # Relacionamentos
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria')
    fornecedor = models.ForeignKey(
        Fornecedor, 
        on_delete=models.CASCADE, 
        verbose_name='Fornecedor',
        null=True,
        blank=True
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    
    # Parcelamento
    eh_parcelado = models.BooleanField(default=False, verbose_name='É Parcelado')
    numero_parcelas = models.IntegerField(default=1, verbose_name='Número de Parcelas')
    parcela_atual = models.IntegerField(default=1, verbose_name='Parcela Atual')
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Valor da Parcela')
    conta_principal = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='parcelas',
        verbose_name='Conta Principal'
    )
    
    # Controle
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    data_pagamento = models.DateField(null=True, blank=True, verbose_name='Data de Pagamento')
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Valor Pago')
    
    # Timestamps
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        ordering = ['data_vencimento']
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
    
    def __str__(self):
        if self.eh_parcelado and self.numero_parcelas > 1:
            return f"{self.descricao} - Parcela {self.parcela_atual}/{self.numero_parcelas}"
        return self.descricao
    
    def get_valor_formatado(self):
        """Retorna o valor formatado em reais"""
        return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def get_status_display_class(self):
        """Retorna a classe CSS para o status"""
        classes = {
            'pendente': 'warning',
            'pago': 'success',
            'vencido': 'danger',
            'cancelado': 'secondary'
        }
        return classes.get(self.status, 'info')
    
    def esta_vencida(self):
        """Verifica se a conta está vencida"""
        from django.utils import timezone
        return self.status == 'pendente' and self.data_vencimento < timezone.now().date()
    
    def dias_para_vencimento(self):
        """Retorna os dias para o vencimento"""
        from django.utils import timezone
        delta = self.data_vencimento - timezone.now().date()
        return delta.days

class DespesaDiaria(models.Model):
    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    data = models.DateField(verbose_name='Data')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        ordering = ['-data']
        verbose_name = 'Despesa Diária'
        verbose_name_plural = 'Despesas Diárias'
    
    def __str__(self):
        return f"{self.descricao} - {self.data}"
    
    def get_valor_formatado(self):
        """Retorna o valor formatado em reais"""
        return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

