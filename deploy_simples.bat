@echo off
echo 🚀 Deploy Automatizado - Sistema de Gestão Empresarial
echo ======================================================

echo.
echo 📦 Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não encontrado. Instale em: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js encontrado!

echo.
echo 📦 Instalando Railway CLI...
npm install -g @railway/cli

echo.
echo 🔐 Fazendo login no Railway...
railway login

echo.
echo 🚀 Criando projeto...
railway init

echo.
echo 🔧 Configurando variáveis de ambiente...
railway variables set SECRET_KEY=chave-secreta-muito-segura-para-producao-2024
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=.railway.app

echo.
echo 🗄️ Adicionando banco PostgreSQL...
railway add

echo.
echo 🚀 Fazendo deploy...
railway deploy

echo.
echo ⏳ Aguardando deploy...
timeout /t 30 /nobreak

echo.
echo 🔧 Executando migrações...
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput

echo.
echo 🌐 Obtendo URL...
railway domain

echo.
echo ======================================================
echo 🎉 DEPLOY CONCLUÍDO COM SUCESSO!
echo ======================================================
echo.
echo 📋 Próximos passos:
echo 1. Acesse o admin e crie um superusuário
echo 2. Configure dados iniciais
echo 3. Teste todas as funcionalidades
echo.
echo 🔧 Para gerenciar:
echo - Dashboard: https://railway.app
echo - Logs: railway logs
echo - Shell: railway shell
echo.
pause 