#!/usr/bin/env python3
"""
Script para automatizar deploy no Railway
"""
import os
import requests
import json
import time
import subprocess
from pathlib import Path

def gerar_secret_key():
    """Gera uma SECRET_KEY segura"""
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(50))

def verificar_railway_cli():
    """Verifica se o Railway CLI está instalado"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def instalar_railway_cli():
    """Instala o Railway CLI"""
    print("📦 Instalando Railway CLI...")
    try:
        subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        print("✅ Railway CLI instalado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar Railway CLI")
        return False

def fazer_login_railway():
    """Faz login no Railway"""
    print("🔐 Fazendo login no Railway...")
    try:
        subprocess.run(['railway', 'login'], check=True)
        print("✅ Login realizado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro no login do Railway")
        return False

def criar_projeto_railway():
    """Cria um novo projeto no Railway"""
    print("🚀 Criando projeto no Railway...")
    try:
        # Verifica se já existe um projeto
        result = subprocess.run(['railway', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Projeto já configurado!")
            return True
        
        # Cria novo projeto
        subprocess.run(['railway', 'init'], check=True)
        print("✅ Projeto criado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao criar projeto")
        return False

def configurar_variaveis():
    """Configura as variáveis de ambiente"""
    print("🔧 Configurando variáveis de ambiente...")
    
    secret_key = gerar_secret_key()
    
    variaveis = {
        'SECRET_KEY': secret_key,
        'DEBUG': 'False',
        'ALLOWED_HOSTS': '.railway.app'
    }
    
    try:
        for key, value in variaveis.items():
            subprocess.run(['railway', 'variables', 'set', f'{key}={value}'], check=True)
            print(f"✅ {key} configurado")
        
        print("✅ Todas as variáveis configuradas!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao configurar variáveis")
        return False

def adicionar_banco_postgres():
    """Adiciona banco PostgreSQL"""
    print("🗄️ Configurando banco PostgreSQL...")
    try:
        # Adiciona PostgreSQL
        subprocess.run(['railway', 'add'], check=True)
        print("✅ PostgreSQL adicionado!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao adicionar PostgreSQL")
        return False

def fazer_deploy():
    """Faz o deploy do projeto"""
    print("🚀 Iniciando deploy...")
    try:
        subprocess.run(['railway', 'deploy'], check=True)
        print("✅ Deploy iniciado!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro no deploy")
        return False

def obter_url():
    """Obtém a URL do projeto"""
    try:
        result = subprocess.run(['railway', 'domain'], capture_output=True, text=True)
        if result.returncode == 0:
            url = result.stdout.strip()
            print(f"🌐 URL do projeto: {url}")
            return url
        return None
    except:
        return None

def executar_comandos_django():
    """Executa comandos Django necessários"""
    print("🔧 Executando comandos Django...")
    
    comandos = [
        'python manage.py migrate',
        'python manage.py collectstatic --noinput'
    ]
    
    try:
        for comando in comandos:
            print(f"Executando: {comando}")
            subprocess.run(['railway', 'run', comando], check=True)
            print(f"✅ {comando} executado!")
        
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar comandos Django")
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando deploy automatizado no Railway...")
    print("=" * 50)
    
    # Verificar Railway CLI
    if not verificar_railway_cli():
        if not instalar_railway_cli():
            print("❌ Não foi possível instalar Railway CLI")
            return
    
    # Login
    if not fazer_login_railway():
        print("❌ Falha no login")
        return
    
    # Criar projeto
    if not criar_projeto_railway():
        print("❌ Falha ao criar projeto")
        return
    
    # Configurar variáveis
    if not configurar_variaveis():
        print("❌ Falha ao configurar variáveis")
        return
    
    # Adicionar banco
    if not adicionar_banco_postgres():
        print("❌ Falha ao adicionar banco")
        return
    
    # Deploy
    if not fazer_deploy():
        print("❌ Falha no deploy")
        return
    
    # Aguardar deploy
    print("⏳ Aguardando conclusão do deploy...")
    time.sleep(30)
    
    # Executar comandos Django
    if not executar_comandos_django():
        print("❌ Falha nos comandos Django")
        return
    
    # Obter URL
    url = obter_url()
    
    print("=" * 50)
    print("🎉 DEPLOY CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    
    if url:
        print(f"🌐 Seu sistema está online em: {url}")
        print(f"🔐 Admin: {url}/admin/")
    
    print("\n📋 Próximos passos:")
    print("1. Acesse o admin e crie um superusuário")
    print("2. Configure dados iniciais")
    print("3. Teste todas as funcionalidades")
    
    print("\n🔧 Para gerenciar:")
    print("- Dashboard: https://railway.app")
    print("- Logs: railway logs")
    print("- Shell: railway shell")

if __name__ == "__main__":
    main() 