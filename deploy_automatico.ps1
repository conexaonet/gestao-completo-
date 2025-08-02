# Deploy Automatizado - Sistema de Gestão Empresarial
Write-Host "🚀 Deploy Automatizado - Sistema de Gestão Empresarial" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green

# Função para verificar se um comando existe
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Verificar Node.js
Write-Host "`n📦 Verificando Node.js..." -ForegroundColor Yellow
if (-not (Test-Command "node")) {
    Write-Host "❌ Node.js não encontrado!" -ForegroundColor Red
    Write-Host "📥 Instale Node.js em: https://nodejs.org/" -ForegroundColor Cyan
    Write-Host "⏳ Aguardando instalação..." -ForegroundColor Yellow
    Start-Process "https://nodejs.org/"
    Read-Host "Pressione Enter após instalar o Node.js"
}

Write-Host "✅ Node.js encontrado!" -ForegroundColor Green

# Instalar Railway CLI
Write-Host "`n📦 Instalando Railway CLI..." -ForegroundColor Yellow
try {
    npm install -g @railway/cli
    Write-Host "✅ Railway CLI instalado!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao instalar Railway CLI" -ForegroundColor Red
    exit 1
}

# Login no Railway
Write-Host "`n🔐 Fazendo login no Railway..." -ForegroundColor Yellow
try {
    railway login
    Write-Host "✅ Login realizado!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro no login" -ForegroundColor Red
    exit 1
}

# Criar projeto
Write-Host "`n🚀 Criando projeto no Railway..." -ForegroundColor Yellow
try {
    railway init
    Write-Host "✅ Projeto criado!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao criar projeto" -ForegroundColor Red
    exit 1
}

# Configurar variáveis de ambiente
Write-Host "`n🔧 Configurando variáveis de ambiente..." -ForegroundColor Yellow
$secretKey = -join ((33..126) | Get-Random -Count 50 | ForEach-Object {[char]$_})

try {
    railway variables set "SECRET_KEY=$secretKey"
    railway variables set "DEBUG=False"
    railway variables set "ALLOWED_HOSTS=.railway.app"
    Write-Host "✅ Variáveis configuradas!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao configurar variáveis" -ForegroundColor Red
}

# Adicionar banco PostgreSQL
Write-Host "`n🗄️ Adicionando banco PostgreSQL..." -ForegroundColor Yellow
try {
    railway add
    Write-Host "✅ PostgreSQL adicionado!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao adicionar PostgreSQL" -ForegroundColor Red
}

# Fazer deploy
Write-Host "`n🚀 Iniciando deploy..." -ForegroundColor Yellow
try {
    railway deploy
    Write-Host "✅ Deploy iniciado!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro no deploy" -ForegroundColor Red
    exit 1
}

# Aguardar deploy
Write-Host "`n⏳ Aguardando conclusão do deploy..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Executar comandos Django
Write-Host "`n🔧 Executando comandos Django..." -ForegroundColor Yellow
try {
    Write-Host "Executando migrações..." -ForegroundColor Cyan
    railway run python manage.py migrate
    
    Write-Host "Coletando arquivos estáticos..." -ForegroundColor Cyan
    railway run python manage.py collectstatic --noinput
    
    Write-Host "✅ Comandos Django executados!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro nos comandos Django" -ForegroundColor Red
}

# Obter URL
Write-Host "`n🌐 Obtendo URL do projeto..." -ForegroundColor Yellow
try {
    $url = railway domain
    Write-Host "✅ URL obtida: $url" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao obter URL" -ForegroundColor Red
    $url = "https://seu-app.railway.app"
}

# Resultado final
Write-Host "`n" -NoNewline
Write-Host "======================================================" -ForegroundColor Green
Write-Host "🎉 DEPLOY CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green

Write-Host "`n🌐 Seu sistema está online em: $url" -ForegroundColor Cyan
Write-Host "🔐 Admin: $url/admin/" -ForegroundColor Cyan

Write-Host "`n📋 Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Acesse o admin e crie um superusuário" -ForegroundColor White
Write-Host "2. Configure dados iniciais" -ForegroundColor White
Write-Host "3. Teste todas as funcionalidades" -ForegroundColor White

Write-Host "`n🔧 Para gerenciar:" -ForegroundColor Yellow
Write-Host "- Dashboard: https://railway.app" -ForegroundColor White
Write-Host "- Logs: railway logs" -ForegroundColor White
Write-Host "- Shell: railway shell" -ForegroundColor White

Write-Host "`n🎯 Para criar superusuário:" -ForegroundColor Yellow
Write-Host "railway run python manage.py createsuperuser" -ForegroundColor Cyan

Read-Host "`nPressione Enter para sair" 