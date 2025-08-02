from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.usuarios_view, name='usuarios'),
    path('novo/', views.novo_usuario_view, name='novo_usuario'),
    path('<int:pk>/', views.detalhe_usuario_view, name='detalhe_usuario'),
    path('<int:pk>/editar/', views.editar_usuario_view, name='editar_usuario'),
] 