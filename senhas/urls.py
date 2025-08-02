from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'senhas', views.GerenciadorSenhasViewSet, basename='gerenciador-senhas')

app_name = 'senhas'

urlpatterns = [
    path('', include(router.urls)),
]

