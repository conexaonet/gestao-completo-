# 🚀 Guia de Deploy - Sistema de Gestão Empresarial

## 📋 Pré-requisitos

- Conta no GitHub
- Conta na plataforma de hospedagem escolhida
- Python 3.11+ instalado localmente

## 🎯 Opções de Hospedagem Recomendadas

### 1. **Render (Recomendado - Gratuito)**
- ✅ Deploy automático do GitHub
- ✅ PostgreSQL incluído
- ✅ SSL gratuito
- ✅ Muito fácil de configurar

### 2. **Railway**
- ✅ Deploy direto do GitHub
- ✅ Banco PostgreSQL incluído
- ✅ Interface simples

### 3. **Heroku**
- ⚠️ Pago (não tem mais plano gratuito)
- ✅ Muito popular e bem documentado

## 🔧 Preparação do Projeto

### 1. **Configurar Git (se ainda não feito)**
```bash
git init
git add .
git commit -m "Initial commit"
```

### 2. **Criar repositório no GitHub**
- Vá para github.com
- Crie um novo repositório
- Siga as instruções para conectar seu projeto local

### 3. **Configurar variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🚀 Deploy no Render

### 1. **Conectar ao Render**
- Acesse render.com
- Faça login com sua conta GitHub
- Clique em "New +" → "Web Service"

### 2. **Configurar o serviço**
- **Name**: gestao-empresarial
- **Repository**: Seu repositório GitHub
- **Branch**: main
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn gestao_empresarial.wsgi:application`

### 3. **Configurar variáveis de ambiente**
Na seção "Environment Variables":
```
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seu-app.onrender.com
DATABASE_URL=postgresql://... (fornecido pelo Render)
```

### 4. **Configurar banco PostgreSQL**
- Vá em "New +" → "PostgreSQL"
- Configure o banco
- Copie a URL do banco para a variável `DATABASE_URL`

## 🚀 Deploy no Railway

### 1. **Conectar ao Railway**
- Acesse railway.app
- Faça login com GitHub
- Clique em "New Project" → "Deploy from GitHub repo"

### 2. **Configurar variáveis**
- Vá em "Variables"
- Adicione as variáveis de ambiente necessárias

### 3. **Configurar banco**
- Railway oferece PostgreSQL automaticamente
- A URL do banco será configurada automaticamente

## 🔧 Configurações Pós-Deploy

### 1. **Executar migrações**
```bash
python manage.py migrate
```

### 2. **Criar superusuário**
```bash
python manage.py createsuperuser
```

### 3. **Coletar arquivos estáticos**
```bash
python manage.py collectstatic --noinput
```

## 🔒 Configurações de Segurança

### 1. **Gerar nova SECRET_KEY**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 2. **Configurar HTTPS**
- Render e Railway oferecem HTTPS automaticamente
- Configure `SECURE_SSL_REDIRECT = True` em produção

### 3. **Configurar CORS**
Atualize `CORS_ALLOWED_ORIGINS` em `settings_production.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://seu-dominio.com",
    "https://www.seu-dominio.com",
]
```

## 📊 Monitoramento

### 1. **Logs**
- Render: Dashboard → Seu serviço → Logs
- Railway: Dashboard → Seu projeto → Deployments → Logs

### 2. **Métricas**
- Ambos oferecem métricas básicas gratuitamente

## 🛠️ Comandos Úteis

### **Verificar status do deploy**
```bash
# Render
curl https://seu-app.onrender.com/health/

# Railway
curl https://seu-app.railway.app/health/
```

### **Acessar logs**
- Use o dashboard da plataforma escolhida
- Ou configure integração com serviços de log

## 🔧 Troubleshooting

### **Erro 500**
1. Verifique os logs
2. Confirme se as variáveis de ambiente estão corretas
3. Teste localmente com `DEBUG=False`

### **Erro de banco**
1. Verifique se o banco PostgreSQL está ativo
2. Confirme a URL do banco
3. Execute as migrações

### **Erro de arquivos estáticos**
1. Execute `collectstatic`
2. Verifique se o WhiteNoise está configurado

## 📞 Suporte

- **Render**: Documentação excelente e suporte ativo
- **Railway**: Comunidade ativa no Discord
- **Heroku**: Documentação extensa

## 🎉 Próximos Passos

1. **Configurar domínio personalizado** (opcional)
2. **Configurar backup automático** do banco
3. **Implementar CI/CD** para deploy automático
4. **Configurar monitoramento** avançado
5. **Implementar cache** (Redis)

---

**🎯 Recomendação**: Comece com **Render** - é gratuito, fácil e confiável para projetos Django! 