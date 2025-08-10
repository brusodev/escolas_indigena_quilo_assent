#!/usr/bin/env python3
"""
Verificação manual do total de veículos
"""

import unicodedata
import json

# Carregar estatísticas
with open('dados/json/estatisticas_atualizadas.json', 'r', encoding='utf-8') as f:
    stats = json.load(f)

# Somar manualmente
detalhamento = stats['detalhamento']
total_manual = sum(detalhamento.values())

print('📊 VERIFICAÇÃO MANUAL DOS VEÍCULOS:')
print(
    f'Total no resumo: {stats["resumo"]["total_veiculos_diretorias_relevantes"]}')
print(f'Total calculado: {total_manual}')
print()
print('📋 Detalhamento por diretoria:')
for diretoria, veiculos in sorted(detalhamento.items()):
    print(f'  • {diretoria}: {veiculos} veículos')

print(f'\n🎯 SOMA TOTAL: {total_manual} veículos')

# Verificar também nos dados originais
print('\n🔍 VERIFICAÇÃO NOS DADOS ORIGINAIS:')
with open('dados/json/dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
    escolas = json.load(f)

with open('dados/json/dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
    veiculos_data = json.load(f)

diretorias_com_escolas = set(escola['diretoria'] for escola in escolas)
print(f'Diretorias que atendem escolas: {len(diretorias_com_escolas)}')


def normalizar_nome(nome):
    if not nome:
        return ""
    nome_norm = unicodedata.normalize('NFD', nome)
    nome_sem_acento = ''.join(
        c for c in nome_norm if unicodedata.category(c) != 'Mn')
    return nome_sem_acento.upper().strip()


# Recalcular
total_veiculos_recalculado = 0
for diretoria in diretorias_com_escolas:
    diretoria_norm = normalizar_nome(diretoria)

    for nome_veiculo, dados_veiculo in veiculos_data['diretorias'].items():
        nome_veiculo_norm = normalizar_nome(nome_veiculo)
        if diretoria_norm == nome_veiculo_norm:
            total_veiculos_recalculado += dados_veiculo['total']
            print(
                f'  ✅ {diretoria} ({nome_veiculo}): {dados_veiculo["total"]} veículos')
            break

print(f'\n🎯 TOTAL RECALCULADO: {total_veiculos_recalculado} veículos')
