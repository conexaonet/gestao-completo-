from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notas', views.NotaFiscalViewSet, basename='nota-fiscal')
router.register(r'itens', views.ItemNotaFiscalViewSet, basename='item-nota-fiscal')

app_name = 'notas_fiscais'

urlpatterns = [
    path('', include(router.urls)),
]

