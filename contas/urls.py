from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')
router.register(r'contas-pagar', views.ContaPagarViewSet, basename='conta-pagar')
router.register(r'despesas', views.DespesaDiariaViewSet, basename='despesa')
router.register(r'relatorios', views.RelatorioViewSet, basename='relatorio')

app_name = 'contas'

urlpatterns = [
    path('', include(router.urls)),
]

