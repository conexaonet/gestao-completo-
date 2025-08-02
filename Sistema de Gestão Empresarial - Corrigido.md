# Sistema de Gestão Empresarial - Corrigido

## Descrição
Sistema Django completo para gestão empresarial com funcionalidades de:
- Contas a pagar
- Despesas diárias
- Gerenciador de senhas
- Notas fiscais

## Estrutura do Projeto
```
GestaoEmpresarialCorrigido/
├── gestao_empresarial/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── contas/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
├── senhas/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
├── notas_fiscais/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
├── templates/
│   ├── dev_base.html
│   ├── dev_dashboard.html
│   ├── contas_pagar.html
│   ├── despesas.html
│   ├── senhas.html
│   └── notas_fiscais.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── media/
├── manage.py
└── requirements.txt
```

## Principais Correções Realizadas

### 1. Estrutura de Arquivos
- ✅ Corrigidos nomes de arquivos (admin.py, apps.py, models.py, etc.)
- ✅ Removidos arquivos duplicados
- ✅ Criados arquivos __init__.py em todos os apps
- ✅ Organizados templates na estrutura correta

### 2. Configurações Django
- ✅ Configurações do settings.py corrigidas
- ✅ URLs principais e dos apps configuradas corretamente
- ✅ WSGI configurado
- ✅ Middleware e apps instalados corretamente

### 3. Models
- ✅ Models do app 'contas' com Categoria, ContaPagar e DespesaDiaria
- ✅ Models do app 'senhas' com GerenciadorSenhas e ChaveCriptografia
- ✅ Models do app 'notas_fiscais' com NotaFiscal e ItemNotaFiscal
- ✅ Relacionamentos e validações implementados

### 4. Views e APIs
- ✅ ViewSets do Django REST Framework implementados
- ✅ Serializers para todas as entidades
- ✅ Endpoints de API funcionais
- ✅ Views para templates implementadas

### 5. Templates e Frontend
- ✅ Template base responsivo com Bootstrap 5
- ✅ Dashboard com estatísticas e gráficos
- ✅ Páginas funcionais para todos os módulos
- ✅ JavaScript customizado com utilitários
- ✅ CSS customizado com design moderno

### 6. Funcionalidades
- ✅ Sistema de autenticação
- ✅ CRUD completo para todas as entidades
- ✅ Criptografia de senhas
- ✅ Upload de arquivos para notas fiscais
- ✅ Filtros e buscas
- ✅ Responsividade mobile

## Como Executar

### 1. Instalar Dependências
```bash
cd GestaoEmpresarialCorrigido
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 3. Executar Servidor
```bash
python manage.py runserver
```

### 4. Acessar Sistema
- URL: http://localhost:8000
- Admin: http://localhost:8000/admin
- Usuário padrão: admin / admin123

## Tecnologias Utilizadas
- Django 4.2.7
- Django REST Framework 3.14.0
- Bootstrap 5.3.0
- Chart.js
- Font Awesome 6.0.0
- Cryptography para senhas
- SQLite (desenvolvimento)

## APIs Disponíveis
- `/api/contas/categorias/` - Categorias
- `/api/contas/contas-pagar/` - Contas a pagar
- `/api/contas/despesas/` - Despesas diárias
- `/api/senhas/gerenciador/` - Gerenciador de senhas
- `/api/notas-fiscais/notas/` - Notas fiscais
- `/api/notas-fiscais/itens/` - Itens de notas fiscais

## Funcionalidades Principais

### Dashboard
- Estatísticas em tempo real
- Gráfico de despesas
- Contas vencidas
- Senhas favoritas
- Ações rápidas

### Contas a Pagar
- Cadastro de contas
- Categorização
- Controle de vencimentos
- Status (pendente, pago, vencido)
- Filtros e buscas

### Despesas Diárias
- Registro de despesas
- Resumo mensal
- Categorização
- Relatórios

### Gerenciador de Senhas
- Armazenamento criptografado
- Gerador de senhas seguras
- Organização por favoritos
- Busca avançada

### Notas Fiscais
- Cadastro completo
- Controle de entrada/saída
- Upload de arquivos
- Itens detalhados
- Resumos financeiros

## Segurança
- Senhas criptografadas com Fernet
- Autenticação obrigatória
- CSRF protection
- Validações de dados
- Permissões por usuário

## Sistema Testado e Funcionando
O sistema foi completamente testado e está funcionando corretamente com todas as funcionalidades implementadas.

