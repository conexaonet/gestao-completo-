# 🚀 Instruções de Deploy no Render

## ✅ Pré-requisitos Concluídos

- ✅ Projeto configurado no Git
- ✅ Arquivos de configuração criados
- ✅ Dependências configuradas
- ✅ Script de build criado

## 🎯 Próximos Passos

### 1. Acessar o Render
1. Vá para [render.com](https://render.com)
2. Faça login com sua conta GitHub
3. Clique em "New +" → "Web Service"

### 2. Conectar ao Repositório
1. Selecione o repositório: `conexaonet/gestao-completo-`
2. Clique em "Connect"

### 3. Configurar o Serviço
- **Name**: `gestao-empresarial`
- **Environment**: `Python 3`
- **Region**: Escolha a mais próxima (ex: US East)
- **Branch**: `main`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn gestao_empresarial.wsgi:application`

### 4. Configurar Variáveis de Ambiente
Na seção "Environment Variables", adicione:

```
SECRET_KEY= (será gerado automaticamente)
DEBUG=False
ALLOWED_HOSTS=.onrender.com
```

### 5. Configurar Banco de Dados
1. Vá em "New +" → "PostgreSQL"
2. Nome: `gestao-db`
3. Database: `gestao_empresarial`
4. User: `gestao_user`
5. Copie a URL do banco para a variável `DATABASE_URL`

### 6. Deploy Automático
1. Clique em "Create Web Service"
2. O Render fará o deploy automaticamente
3. Aguarde a conclusão (pode levar alguns minutos)

## 🔧 Pós-Deploy

### 1. Criar Superusuário
Após o deploy, acesse o terminal do Render e execute:
```bash
python manage.py createsuperuser
```

### 2. Verificar Funcionamento
- Acesse: `https://seu-app.onrender.com/admin/`
- Teste o login com o superusuário criado

## 📊 Monitoramento

### Logs
- Dashboard → Seu serviço → Logs
- Monitore erros e performance

### Métricas
- Dashboard → Seu serviço → Metrics
- Acompanhe uso de recursos

## 🔒 Segurança

### HTTPS
- Render oferece HTTPS automaticamente
- Configure domínio personalizado se necessário

### Backup
- Configure backup automático do banco
- Teste restauração periodicamente

## 🚨 Troubleshooting

### Erro 500
1. Verifique logs no dashboard
2. Confirme variáveis de ambiente
3. Teste localmente com `DEBUG=False`

### Erro de Banco
1. Verifique se PostgreSQL está ativo
2. Confirme `DATABASE_URL`
3. Execute migrações manualmente

### Erro de Arquivos Estáticos
1. Verifique se `collectstatic` foi executado
2. Confirme configuração do WhiteNoise

## 📞 Suporte

- **Render Docs**: [docs.render.com](https://docs.render.com)
- **Django Docs**: [docs.djangoproject.com](https://docs.djangoproject.com)
- **Comunidade**: Stack Overflow, Reddit r/django

---

**🎉 Seu sistema estará online em alguns minutos!** 