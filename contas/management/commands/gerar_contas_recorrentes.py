from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from contas.models import ContaPagar
import calendar

class Command(BaseCommand):
    help = 'Gera contas recorrentes automaticamente'

    def handle(self, *args, **options):
        hoje = timezone.now().date()
        contas_geradas = 0
        
        # Buscar contas recorrentes que precisam ser geradas
        contas_recorrentes = ContaPagar.objects.filter(
            eh_recorrente=True,
            proxima_geracao__lte=hoje
        )
        
        for conta in contas_recorrentes:
            # Verificar se ainda não passou da data de fim
            if conta.data_fim_recorrencia and conta.data_fim_recorrencia < hoje:
                continue
                
            # Calcular próxima data baseada no tipo de recorrência
            proxima_data = self.calcular_proxima_data(conta.data_vencimento, conta.tipo_recorrencia)
            
            # Criar nova conta
            nova_conta = ContaPagar.objects.create(
                descricao=conta.descricao,
                valor=conta.valor,
                data_vencimento=proxima_data,
                status='pendente',
                categoria=conta.categoria,
                fornecedor=conta.fornecedor,
                usuario=conta.usuario,
                observacoes=conta.observacoes,
                eh_recorrente=True,
                tipo_recorrencia=conta.tipo_recorrencia,
                data_fim_recorrencia=conta.data_fim_recorrencia,
                proxima_geracao=self.calcular_proxima_data(proxima_data, conta.tipo_recorrencia)
            )
            
            contas_geradas += 1
            self.stdout.write(
                self.style.SUCCESS(f'Conta recorrente gerada: {nova_conta.descricao} - {proxima_data}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Total de contas recorrentes geradas: {contas_geradas}')
        )
    
    def calcular_proxima_data(self, data_atual, tipo_recorrencia):
        """Calcula a próxima data baseada no tipo de recorrência"""
        if tipo_recorrencia == 'semanal':
            return data_atual + timedelta(days=7)
        elif tipo_recorrencia == 'quinzenal':
            return data_atual + timedelta(days=15)
        elif tipo_recorrencia == 'mensal':
            return self.adicionar_meses(data_atual, 1)
        elif tipo_recorrencia == 'bimestral':
            return self.adicionar_meses(data_atual, 2)
        elif tipo_recorrencia == 'trimestral':
            return self.adicionar_meses(data_atual, 3)
        elif tipo_recorrencia == 'semestral':
            return self.adicionar_meses(data_atual, 6)
        elif tipo_recorrencia == 'anual':
            return self.adicionar_meses(data_atual, 12)
        else:
            return data_atual + timedelta(days=30)  # Padrão mensal
    
    def adicionar_meses(self, data, meses):
        """Adiciona meses a uma data, mantendo o dia quando possível"""
        ano = data.year + ((data.month - 1 + meses) // 12)
        mes = ((data.month - 1 + meses) % 12) + 1
        
        # Ajustar o dia se necessário (ex: 31 de janeiro para fevereiro)
        ultimo_dia_mes = calendar.monthrange(ano, mes)[1]
        dia = min(data.day, ultimo_dia_mes)
        
        return data.replace(year=ano, month=mes, day=dia) 