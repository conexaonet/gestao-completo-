from django.urls import path
from . import views

app_name = 'fornecedores'

urlpatterns = [
    path('', views.fornecedores_view, name='fornecedores'),
    path('novo/', views.novo_fornecedor_view, name='novo_fornecedor'),
    path('<int:pk>/', views.detalhe_fornecedor_view, name='detalhe_fornecedor'),
    path('<int:pk>/editar/', views.editar_fornecedor_view, name='editar_fornecedor'),
] 