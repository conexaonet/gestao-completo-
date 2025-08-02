from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64
import os
from datetime import datetime, timedelta

class GerenciadorSenhas(models.Model):
    CATEGORIA_CHOICES = [
        ('banco', 'Banco'),
        ('email', 'E-mail'),
        ('social', 'Rede Social'),
        ('trabalho', 'Trabalho'),
        ('pessoal', 'Pessoal'),
        ('outros', 'Outros'),
    ]
    
    titulo = models.CharField(max_length=100, verbose_name='Título')
    url = models.URLField(blank=True, verbose_name='URL')
    usuario_login = models.CharField(max_length=100, verbose_name='Usuário/Login')
    senha_criptografada = models.BinaryField(verbose_name='Senha Criptografada')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    arquivo = models.FileField(upload_to='senhas_arquivos/', blank=True, null=True, verbose_name='Arquivo')
    favorito = models.BooleanField(default=False, verbose_name='Favorito')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='outros', verbose_name='Categoria')
    tags = models.CharField(max_length=200, blank=True, verbose_name='Tags (separadas por vírgula)')
    data_expiracao = models.DateField(blank=True, null=True, verbose_name='Data de Expiração')
    forca_senha = models.IntegerField(default=0, verbose_name='Força da Senha (0-100)')
    ultima_alteracao = models.DateTimeField(auto_now=True, verbose_name='Última Alteração')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    def set_senha(self, senha_texto):
        """Criptografa e armazena a senha"""
        # Gera uma chave única para este usuário
        key = self._get_or_create_user_key()
        f = Fernet(key)
        senha_bytes = senha_texto.encode('utf-8')
        self.senha_criptografada = f.encrypt(senha_bytes)
        # Calcula força da senha
        self.forca_senha = self._calcular_forca_senha(senha_texto)
    
    def get_senha(self):
        """Descriptografa e retorna a senha"""
        try:
            key = self._get_or_create_user_key()
            f = Fernet(key)
            senha_bytes = f.decrypt(self.senha_criptografada)
            return senha_bytes.decode('utf-8')
        except Exception as e:
            return "Erro ao descriptografar"
    
    def _calcular_forca_senha(self, senha):
        """Calcula a força da senha (0-100)"""
        score = 0
        
        # Comprimento
        if len(senha) >= 8:
            score += 20
        if len(senha) >= 12:
            score += 10
        
        # Caracteres especiais
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in senha):
            score += 20
        
        # Números
        if any(c.isdigit() for c in senha):
            score += 20
        
        # Letras maiúsculas e minúsculas
        if any(c.isupper() for c in senha) and any(c.islower() for c in senha):
            score += 20
        
        # Variedade de caracteres
        unique_chars = len(set(senha))
        if unique_chars >= 8:
            score += 10
        
        return min(score, 100)
    
    def esta_expirada(self):
        """Verifica se a senha está expirada"""
        if self.data_expiracao:
            return datetime.now().date() > self.data_expiracao
        return False
    
    def dias_para_expiracao(self):
        """Retorna dias até a expiração"""
        if self.data_expiracao:
            delta = self.data_expiracao - datetime.now().date()
            return delta.days
        return None
    
    def get_tags_list(self):
        """Retorna lista de tags"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def _get_or_create_user_key(self):
        """Obtém ou cria uma chave de criptografia para o usuário"""
        chave_obj, created = ChaveCriptografia.objects.get_or_create(
            usuario=self.usuario,
            defaults={'chave': base64.b64encode(Fernet.generate_key()).decode()}
        )
        return base64.b64decode(chave_obj.chave.encode())
    
    class Meta:
        ordering = ['-atualizado_em']
        verbose_name = 'Senha'
        verbose_name_plural = 'Senhas'
    
    def __str__(self):
        return self.titulo

class ChaveCriptografia(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    chave = models.TextField(verbose_name='Chave')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Chave de Criptografia'
        verbose_name_plural = 'Chaves de Criptografia'
    
    def __str__(self):
        return f"Chave de {self.usuario.username}"

