from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario

class Command(BaseCommand):
    help = 'Configura permissões para o gerenciador de senhas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Nome do usuário para configurar permissões'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Configurar permissões para todos os usuários'
        )

    def handle(self, *args, **options):
        if options['username']:
            try:
                user = User.objects.get(username=options['username'])
                self.configurar_perfil_usuario(user)
                self.stdout.write(
                    self.style.SUCCESS(f'Permissões configuradas para {user.username}')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Usuário {options["username"]} não encontrado')
                )
        
        elif options['all']:
            users = User.objects.all()
            for user in users:
                self.configurar_perfil_usuario(user)
            self.stdout.write(
                self.style.SUCCESS(f'Permissões configuradas para {users.count()} usuários')
            )
        
        else:
            self.stdout.write(
                self.style.WARNING('Use --username ou --all para especificar usuários')
            )

    def configurar_perfil_usuario(self, user):
        """Configura o perfil do usuário com permissões adequadas"""
        perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=user,
            defaults={
                'nivel_acesso': 'usuario',
                'status': 'ativo'
            }
        )
        
        # Configurar permissões baseadas no tipo de usuário
        if user.is_superuser:
            perfil.nivel_acesso = 'admin'
        elif user.is_staff:
            perfil.nivel_acesso = 'gerente'
        else:
            perfil.nivel_acesso = 'usuario'
        
        perfil.save()
        
        self.stdout.write(
            f'Perfil configurado para {user.username}: {perfil.get_nivel_acesso_display()}'
        ) 