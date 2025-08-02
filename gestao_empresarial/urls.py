from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from contas.views import ContaPagarViewSet, DespesaDiariaViewSet, CategoriaViewSet, RelatorioViewSet
from senhas.views import GerenciadorSenhasViewSet
from fornecedores.views import FornecedorViewSet, ContatoFornecedorViewSet, CategoriaFornecedorViewSet
from usuarios.views import PerfilUsuarioViewSet, PermissaoViewSet, GrupoPermissaoViewSet

# Configuração do Router para API
router = DefaultRouter()
router.register(r'contas/contas-pagar', ContaPagarViewSet, basename='contapagar')
router.register(r'contas/despesas', DespesaDiariaViewSet, basename='despesadiaria')
router.register(r'contas/categorias', CategoriaViewSet, basename='categoria')
router.register(r'contas/relatorios', RelatorioViewSet, basename='relatorio')
router.register(r'senhas/senhas', GerenciadorSenhasViewSet, basename='senha')
router.register(r'fornecedores/fornecedores', FornecedorViewSet, basename='fornecedor')
router.register(r'fornecedores/contatos', ContatoFornecedorViewSet, basename='contatofornecedor')
router.register(r'fornecedores/categorias', CategoriaFornecedorViewSet, basename='categoriafornecedor')
router.register(r'usuarios/perfis', PerfilUsuarioViewSet, basename='perfilusuario')
router.register(r'usuarios/permissoes', PermissaoViewSet, basename='permissao')
router.register(r'usuarios/grupos', GrupoPermissaoViewSet, basename='grupopermissao')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('core.urls')),
    path('senhas/', include('senhas.urls')),
    path('fornecedores/', include('fornecedores.urls')),
    path('usuarios/', include('usuarios.urls')),
]

