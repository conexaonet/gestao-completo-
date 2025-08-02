from django.db import models
from django.contrib.auth.models import User

class NotaFiscal(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processada', 'Processada'),
        ('cancelada', 'Cancelada'),
    ]
    
    numero = models.CharField(max_length=50, verbose_name='Número')
    serie = models.CharField(max_length=10, verbose_name='Série')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name='Tipo')
    data_emissao = models.DateField(verbose_name='Data de Emissão')
    data_vencimento = models.DateField(null=True, blank=True, verbose_name='Data de Vencimento')
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor Total')
    valor_impostos = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Valor dos Impostos')
    fornecedor_cliente = models.CharField(max_length=200, verbose_name='Fornecedor/Cliente')
    cnpj_cpf = models.CharField(max_length=18, verbose_name='CNPJ/CPF')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    arquivo = models.FileField(upload_to='notas_fiscais/', null=True, blank=True, verbose_name='Arquivo')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        ordering = ['-data_emissao']
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'
        unique_together = ['numero', 'serie', 'usuario']
    
    def __str__(self):
        return f"NF {self.numero}/{self.serie} - {self.fornecedor_cliente}"

class ItemNotaFiscal(models.Model):
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE, related_name='itens', verbose_name='Nota Fiscal')
    codigo = models.CharField(max_length=50, verbose_name='Código')
    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    quantidade = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='Quantidade')
    unidade = models.CharField(max_length=10, verbose_name='Unidade')
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Unitário')
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor Total')
    
    class Meta:
        verbose_name = 'Item da Nota Fiscal'
        verbose_name_plural = 'Itens da Nota Fiscal'
    
    def __str__(self):
        return f"{self.codigo} - {self.descricao}"
    
    def save(self, *args, **kwargs):
        # Calcula o valor total automaticamente
        self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)

