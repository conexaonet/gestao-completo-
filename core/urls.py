from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contas-pagar/', views.contas_pagar_view, name='contas_pagar'),
    path('despesas/', views.despesas_view, name='despesas'),
    path('senhas/', views.senhas_view, name='senhas'),
    path('senhas/login/', views.senhas_login_view, name='senhas_login'),
    path('notas-fiscais/', views.notas_fiscais_view, name='notas_fiscais'),
    path('relatorio-mensal/', views.relatorio_mensal_view, name='relatorio_mensal'),
    path('relatorio-categoria/', views.relatorio_categoria_view, name='relatorio_categoria'),
    path('relatorio-evolucao/', views.relatorio_evolucao_view, name='relatorio_evolucao'),
]

