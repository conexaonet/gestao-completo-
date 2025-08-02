#!/usr/bin/env python3
"""
Script para configurar o projeto para deploy
"""
import os
import secrets
import string
from pathlib import Path

def generate_secret_key():
    """Gera uma nova SECRET_KEY para Django"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(50))

def create_env_file():
    """Cria arquivo .env com configurações básicas"""
    env_content = f"""# Configurações do Django
SECRET_KEY={generate_secret_key()}
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Configurações do Banco de Dados (será configurado pela plataforma)
DATABASE_URL=sqlite:///db.sqlite3

# Configurações de Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app

# Configurações de Criptografia (para senhas)
FERNET_KEY={secrets.token_urlsafe(32)}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado com sucesso!")

def create_gitignore():
    """Cria ou atualiza .gitignore"""
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Media files
media/

# Static files
staticfiles/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Arquivo .gitignore criado com sucesso!")

def check_requirements():
    """Verifica se todos os arquivos necessários existem"""
    required_files = [
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'gestao_empresarial/settings_production.py',
        'DEPLOY.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Arquivos faltando:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Todos os arquivos necessários estão presentes!")
    return True

def main():
    """Função principal"""
    print("🚀 Configurando projeto para deploy...")
    print("=" * 50)
    
    # Criar arquivos necessários
    create_env_file()
    create_gitignore()
    
    # Verificar arquivos
    if check_requirements():
        print("\n🎉 Projeto configurado com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Configure o Git e GitHub")
        print("2. Escolha uma plataforma de hospedagem (Render recomendado)")
        print("3. Siga o guia em DEPLOY.md")
        print("4. Configure as variáveis de ambiente na plataforma")
        print("5. Faça o deploy!")
    else:
        print("\n❌ Alguns arquivos estão faltando. Verifique se todos foram criados.")

if __name__ == "__main__":
    main() 