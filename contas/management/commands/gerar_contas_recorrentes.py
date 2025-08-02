from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from contas.models import ContaPagar
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Gera contas recorrentes automaticamente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra o que seria gerado sem criar as contas',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Buscar contas recorrentes que precisam ser geradas
        contas_recorrentes = ContaPagar.objects.filter(
            eh_recorrente=True,
            tipo_recorrencia__isnull=False
        )
        
        contas_geradas = 0
        
        for conta in contas_recorrentes:
            # Verificar se a data de fim da recorrência não foi atingida
            if conta.data_fim_recorrencia and conta.data_fim_recorrencia < timezone.now().date():
                continue
                
            # Calcular próxima data baseada no tipo de recorrência
            proxima_data = self.calcular_proxima_data(conta)
            
            # Se a próxima data é hoje ou no passado, gerar nova conta
            if proxima_data <= timezone.now().date():
                if not dry_run:
                    self.gerar_conta_recorrente(conta, proxima_data)
                contas_geradas += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Gerando conta recorrente: {conta.descricao} - {proxima_data}'
                    )
                )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: {contas_geradas} contas seriam geradas'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'{contas_geradas} contas recorrentes foram geradas'
                )
            )

    def calcular_proxima_data(self, conta):
        """Calcula a próxima data baseada no tipo de recorrência"""
        data_base = conta.data_vencimento
        
        if conta.tipo_recorrencia == 'semanal':
            return data_base + timedelta(days=7)
        elif conta.tipo_recorrencia == 'quinzenal':
            return data_base + timedelta(days=15)
        elif conta.tipo_recorrencia == 'mensal':
            return self.adicionar_meses(data_base, 1)
        elif conta.tipo_recorrencia == 'bimestral':
            return self.adicionar_meses(data_base, 2)
        elif conta.tipo_recorrencia == 'trimestral':
            return self.adicionar_meses(data_base, 3)
        elif conta.tipo_recorrencia == 'semestral':
            return self.adicionar_meses(data_base, 6)
        elif conta.tipo_recorrencia == 'anual':
            return self.adicionar_meses(data_base, 12)
        
        return data_base

    def adicionar_meses(self, data, meses):
        """Adiciona meses a uma data, mantendo o dia do mês quando possível"""
        ano = data.year
        mes = data.month + meses
        
        # Ajustar ano se necessário
        while mes > 12:
            ano += 1
            mes -= 12
        
        # Tentar manter o mesmo dia do mês
        try:
            return data.replace(year=ano, month=mes)
        except ValueError:
            # Se o dia não existe no mês (ex: 31 em fevereiro), usar o último dia do mês
            from calendar import monthrange
            ultimo_dia = monthrange(ano, mes)[1]
            return data.replace(year=ano, month=mes, day=ultimo_dia)

    def gerar_conta_recorrente(self, conta_original, nova_data):
        """Gera uma nova conta baseada na conta recorrente original"""
        nova_conta = ContaPagar.objects.create(
            descricao=conta_original.descricao,
            valor=conta_original.valor,
            data_vencimento=nova_data,
            status='pendente',
            categoria=conta_original.categoria,
            fornecedor=conta_original.fornecedor,
            usuario=conta_original.usuario,
            observacoes=conta_original.observacoes,
            eh_recorrente=False,  # A nova conta não é recorrente
            tipo_recorrencia=None,
            data_fim_recorrencia=None,
            proxima_geracao=None
        )
        
        # Atualizar a próxima geração da conta original
        proxima_data = self.calcular_proxima_data(nova_conta)
        conta_original.proxima_geracao = proxima_data
        conta_original.save()
        
        return nova_conta 