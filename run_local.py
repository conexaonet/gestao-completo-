#!/usr/bin/env python3
"""
Script para rodar o sistema localmente
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar variáveis de ambiente
os.environ.setdefault('SECRET_KEY', 'django-insecure-local-development-key-2024')
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('ALLOWED_HOSTS', 'localhost,127.0.0.1')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_empresarial.settings')
django.setup()

if __name__ == '__main__':
    # Executar migrações
    print("🔄 Executando migrações...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Coletar arquivos estáticos
    print("📦 Coletando arquivos estáticos...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    # Criar superusuário se não existir
    print("👤 Verificando superusuário...")
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            print("Criando superusuário padrão...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Superusuário criado: admin / admin123")
        else:
            print("✅ Superusuário já existe")
    except Exception as e:
        print(f"⚠️ Erro ao verificar superusuário: {e}")
    
    # Rodar servidor
    print("🚀 Iniciando servidor local...")
    print("🌐 Acesse: http://127.0.0.1:8000")
    print("🔐 Admin: http://127.0.0.1:8000/admin/")
    print("👤 Login: admin / admin123")
    print("⏹️ Pressione Ctrl+C para parar")
    
    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000']) 