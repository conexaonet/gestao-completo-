# 🚀 Deploy Rápido - Sistema de Gestão Empresarial

## ✅ Opções Automatizadas

### **Opção 1: Script PowerShell (Recomendado)**
```powershell
# Execute no PowerShell como Administrador
.\deploy_automatico.ps1
```

### **Opção 2: Script Batch**
```cmd
# Execute no CMD
deploy_simples.bat
```

### **Opção 3: Script Python**
```bash
python deploy_railway.py
```

## 🎯 Pré-requisitos

### 1. **Node.js**
- Baixe em: https://nodejs.org/
- Instale a versão LTS
- Reinicie o computador após instalação

### 2. **Conta Railway**
- Vá para [railway.app](https://railway.app)
- Faça login com GitHub
- Autorize o Railway

## 🚀 Executando o Deploy

### **Passo 1: Abrir PowerShell como Administrador**
1. Pressione `Win + X`
2. Escolha "Windows PowerShell (Administrador)"

### **Passo 2: Navegar para a pasta do projeto**
```powershell
cd "C:\Users\GG\Downloads\Gestao-90d797258eccea9144c00a9b01fad27e57c6f111\Gestao-90d797258eccea9144c00a9b01fad27e57c6f111"
```

### **Passo 3: Executar o script**
```powershell
.\deploy_automatico.ps1
```

## 📋 O que o script faz automaticamente:

1. ✅ **Verifica Node.js**
2. ✅ **Instala Railway CLI**
3. ✅ **Faz login no Railway**
4. ✅ **Cria projeto**
5. ✅ **Configura variáveis de ambiente**
6. ✅ **Adiciona banco PostgreSQL**
7. ✅ **Faz deploy**
8. ✅ **Executa migrações**
9. ✅ **Coleta arquivos estáticos**
10. ✅ **Mostra URL final**

## 🎉 Após o Deploy

### **1. Criar Superusuário**
```bash
railway run python manage.py createsuperuser
```

### **2. Acessar o Sistema**
- **URL**: Será mostrada no final do script
- **Admin**: `https://seu-app.railway.app/admin/`

### **3. Testar Funcionalidades**
- Login no admin
- Criar categorias
- Adicionar contas
- Testar todas as funcionalidades

## 🔧 Comandos Úteis

### **Ver logs**
```bash
railway logs
```

### **Abrir shell**
```bash
railway shell
```

### **Ver domínio**
```bash
railway domain
```

### **Reiniciar**
```bash
railway restart
```

## 🚨 Se algo der errado:

### **Erro de Node.js**
- Instale Node.js: https://nodejs.org/
- Reinicie o computador
- Execute novamente

### **Erro de login**
- Vá para [railway.app](https://railway.app)
- Faça login manualmente
- Execute novamente

### **Erro de deploy**
- Verifique logs: `railway logs`
- Tente novamente: `railway deploy`

## 📞 Suporte

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Discord**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub**: [github.com/railwayapp](https://github.com/railwayapp)

---

**🎯 Execute o script e seu sistema estará online em minutos!** 