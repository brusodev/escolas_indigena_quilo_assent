#!/usr/bin/env python3
"""
Análise detalhada para encontrar a discrepância entre 39 e 40 veículos
"""

import json
import unicodedata


def normalizar_nome(nome):
    if not nome:
        return ""
    nome_norm = unicodedata.normalize('NFD', nome)
    nome_sem_acento = ''.join(
        c for c in nome_norm if unicodedata.category(c) != 'Mn')
    return nome_sem_acento.upper().strip()


# Carregar dados
with open('dados/json/dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
    escolas = json.load(f)

with open('dados/json/dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
    veiculos_data = json.load(f)

print("🔍 ANÁLISE DETALHADA DA DISCREPÂNCIA 39 vs 40 VEÍCULOS")
print("=" * 60)

# 1. Verificar todas as diretorias com escolas
diretorias_escolas = {}
for escola in escolas:
    diretoria = escola.get('diretoria', '')
    if diretoria:
        if diretoria not in diretorias_escolas:
            diretorias_escolas[diretoria] = 0
        diretorias_escolas[diretoria] += 1

print(f"\n📊 DIRETORIAS QUE ATENDEM ESCOLAS: {len(diretorias_escolas)}")
for diretoria, qtd_escolas in sorted(diretorias_escolas.items()):
    print(f"  • {diretoria}: {qtd_escolas} escolas")

# 2. Mapear com dados de veículos
total_veiculos_encontrados = 0
total_veiculos_nao_encontrados = 0
diretorias_mapeadas = []
diretorias_nao_mapeadas = []

print(f"\n🚗 MAPEAMENTO DE VEÍCULOS:")

for diretoria_escola in sorted(diretorias_escolas.keys()):
    diretoria_norm = normalizar_nome(diretoria_escola)
    encontrada = False

    for nome_veiculo, dados_veiculo in veiculos_data['diretorias'].items():
        nome_veiculo_norm = normalizar_nome(nome_veiculo)
        if diretoria_norm == nome_veiculo_norm:
            veiculos = dados_veiculo['total']
            total_veiculos_encontrados += veiculos
            diretorias_mapeadas.append(
                (diretoria_escola, nome_veiculo, veiculos))
            print(
                f"  ✅ {diretoria_escola} → {nome_veiculo}: {veiculos} veículos")
            encontrada = True
            break

    if not encontrada:
        diretorias_nao_mapeadas.append(diretoria_escola)
        print(f"  ❌ {diretoria_escola}: NÃO ENCONTRADA")

print(f"\n📊 RESUMO:")
print(f"  • Diretorias mapeadas: {len(diretorias_mapeadas)}")
print(f"  • Diretorias não mapeadas: {len(diretorias_nao_mapeadas)}")
print(f"  • Total de veículos calculado: {total_veiculos_encontrados}")

# 3. Verificar se há alguma diretoria que deveria ser incluída
print(f"\n🔍 POSSÍVEIS DIRETORIAS PERDIDAS:")
todas_diretorias_veiculos = set(normalizar_nome(nome)
                                for nome in veiculos_data['diretorias'].keys())
diretorias_escolas_norm = set(normalizar_nome(nome)
                              for nome in diretorias_escolas.keys())

diretorias_perdidas = todas_diretorias_veiculos - diretorias_escolas_norm

if diretorias_perdidas:
    for diretoria_perdida_norm in diretorias_perdidas:
        # Encontrar o nome original
        for nome_original, dados in veiculos_data['diretorias'].items():
            if normalizar_nome(nome_original) == diretoria_perdida_norm:
                print(
                    f"  🤔 {nome_original}: {dados['total']} veículos (não tem escolas mapeadas)")
                break

# 4. Verificar se existe alguma diretoria com 1 veículo extra
print(f"\n🎯 ANÁLISE FINAL:")
print(f"  • Documentação menciona: 40 veículos")
print(f"  • Cálculo atual retorna: {total_veiculos_encontrados} veículos")
print(f"  • Diferença: {40 - total_veiculos_encontrados} veículo(s)")

if total_veiculos_encontrados == 39:
    print(f"\n💡 HIPÓTESES PARA A DIFERENÇA DE 1 VEÍCULO:")
    print(f"  1. Alguma diretoria foi contada diferente na documentação original")
    print(f"  2. Houve atualização nos dados após a documentação")
    print(f"  3. Erro de arredondamento ou contagem manual")

    # Verificar se há diretorias com exatamente 1 veículo que poderiam ser revisadas
    print(f"\n🔍 DIRETORIAS COM POUCOS VEÍCULOS (candidatas a revisão):")
    for diretoria, nome_veiculo, veiculos in diretorias_mapeadas:
        if veiculos <= 2:
            print(f"  • {diretoria}: {veiculos} veículos")
