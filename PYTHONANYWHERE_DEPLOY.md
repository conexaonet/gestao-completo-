# 🚀 Deploy no PythonAnywhere - Guia Completo

## ✅ Por que PythonAnywhere?

- 🆓 **Gratuito** para projetos Django
- 🐍 **Especializado em Python**
- 🗄️ **MySQL incluído** (gratuito)
- 🔧 **Interface web** para gerenciar
- 📊 **Logs detalhados**
- 🎯 **Perfeito para Django**

## 🎯 Passo a Passo - PythonAnywhere

### 1. Criar Conta
1. Vá para [pythonanywhere.com](https://pythonanywhere.com)
2. Clique em **"Create a Beginner account"** (gratuito)
3. Confirme seu email

### 2. Configurar Git
1. Vá em **"Consoles"** → **"Bash"**
2. Execute:
```bash
git clone https://github.com/conexaonet/gestao-completo-.git
cd gestao-completo-
```

### 3. Configurar Ambiente Virtual
```bash
python3 -m venv gestao_env
source gestao_env/bin/activate
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados
1. Vá em **"Databases"**
2. Crie um banco MySQL (gratuito)
3. Anote as credenciais

### 5. Configurar Web App
1. Vá em **"Web"** → **"Add a new web app"**
2. Escolha **"Manual configuration"**
3. Escolha **"Python 3.11"**

### 6. Configurar WSGI
1. Clique em **"WSGI configuration file"**
2. Substitua o conteúdo por:
```python
import os
import sys

path = '/home/seu-usuario/gestao-completo-'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'gestao_empresarial.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 7. Configurar Variáveis de Ambiente
1. Vá em **"Files"** → **".bashrc"**
2. Adicione:
```bash
export SECRET_KEY="sua-chave-secreta-aqui"
export DEBUG=False
export ALLOWED_HOSTS="seu-usuario.pythonanywhere.com"
```

### 8. Executar Migrações
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 9. Criar Superusuário
```bash
python manage.py createsuperuser
```

### 10. Reiniciar Web App
1. Vá em **"Web"**
2. Clique em **"Reload"**

## 🔧 Configurações Específicas

### settings.py para PythonAnywhere
```python
# Adicione ao settings.py
ALLOWED_HOSTS = ['seu-usuario.pythonanywhere.com']

# Para arquivos estáticos
STATIC_ROOT = '/home/seu-usuario/gestao-completo-/staticfiles'
STATIC_URL = '/static/'
```

### Banco MySQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'seu-usuario$gestao',
        'USER': 'seu-usuario',
        'PASSWORD': 'sua-senha',
        'HOST': 'seu-usuario.mysql.pythonanywhere-services.com',
    }
}
```

## 📊 Monitoramento

### Logs
- **Web** → **"Log files"**
- **Error log** e **Server log**

### Console
- **Consoles** → **"Bash"**
- Execute comandos Django

## 🔒 Segurança

### HTTPS
- PythonAnywhere oferece HTTPS
- Configure em **"Web"** → **"Security"**

### Backup
- Faça backup regular do banco
- Use **"Files"** para gerenciar arquivos

## 🚨 Troubleshooting

### Erro 500
1. Verifique **"Error log"**
2. Confirme variáveis de ambiente
3. Teste no console

### Erro de Banco
1. Verifique credenciais MySQL
2. Confirme se o banco existe
3. Execute migrações

### Erro de Arquivos Estáticos
1. Execute `collectstatic`
2. Verifique `STATIC_ROOT`
3. Confirme permissões

## 💡 Dicas Importantes

### 1. Limites Gratuitos
- 512MB de espaço
- 1 web app
- 1 banco MySQL
- CPU limitado

### 2. Performance
- Use `DEBUG=False`
- Configure cache se necessário
- Otimize consultas

### 3. Domínio
- Formato: `seu-usuario.pythonanywhere.com`
- Pode configurar domínio personalizado (pago)

## 📞 Suporte

- **Docs**: [help.pythonanywhere.com](https://help.pythonanywhere.com)
- **Forum**: [forum.pythonanywhere.com](https://forum.pythonanywhere.com)
- **Email**: support@pythonanywhere.com

## 🎉 Vantagens do PythonAnywhere

- ✅ **Especializado em Python/Django**
- ✅ **Interface web completa**
- ✅ **Logs detalhados**
- ✅ **Console interativo**
- ✅ **Suporte excelente**

---

**🚀 PythonAnywhere é perfeito para projetos Django!** 