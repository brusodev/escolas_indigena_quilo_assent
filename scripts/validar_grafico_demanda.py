"""
Script para validar se o gráfico "Veículos vs Demanda" está correto
Criado em: 07/08/2025
Versão: 1.0
"""

import json


def normalizeDiretoriaName(name):
    """Função de normalização igual à do JavaScript"""
    if not name:
        return ''

    # Converter para maiúsculo e remover espaços extras (manter acentos)
    normalized = name.upper().strip()

    # Mapeamentos específicos para casos especiais
    mappings = {
        'SAO VICENTE': 'SÃO VICENTE',
        'SAO BERNARDO DO CAMPO': 'SÃO BERNARDO DO CAMPO',
        'SANTO ANASTACIO': 'SANTO ANASTÁCIO',
        'PENAPOLIS': 'PENÁPOLIS',
        'TUPA': 'TUPÃ',
        'ITARARE': 'ITARARÉ',
        'LESTE 5': 'LESTE 5',
        'SUL 3': 'SUL 3',
        'NORTE 1': 'NORTE 1'
    }

    return mappings.get(normalized, normalized)


def calcular_prioridade(escola, veiculos_diretoria):
    """Calcula prioridade da escola baseada na distância e veículos"""
    vehicles = veiculos_diretoria.get('total', 0)
    distance = escola['distance']

    if distance > 50 and vehicles == 0:
        return 'high'
    elif distance > 30 and vehicles == 0:
        return 'medium'
    else:
        return 'low'


def validar_grafico_demanda():
    """Valida se o gráfico de demanda está correto"""
    print("=== VALIDAÇÃO DO GRÁFICO VEÍCULOS vs DEMANDA ===\n")

    # Carregar dados
    with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        escolas = json.load(f)

    with open('dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
        dados_veiculos = json.load(f)

    veiculos = dados_veiculos['diretorias']

    # Preparar estatísticas por diretoria
    diretoria_stats = {}

    print("📊 Processando escolas por diretoria:")
    for escola in escolas:
        nome_normalizado = normalizeDiretoriaName(escola['diretoria'])

        if nome_normalizado not in diretoria_stats:
            veiculos_diretoria = veiculos.get(
                nome_normalizado, {'total': 0, 's1': 0, 's2': 0, 's2_4x4': 0})
            diretoria_stats[nome_normalizado] = {
                'nome_original': escola['diretoria'],
                'escolas': 0,
                'alta_prioridade': 0,
                'veiculos': veiculos_diretoria['total'],
                'veiculos_detalhes': veiculos_diretoria
            }

        # Calcular prioridade
        prioridade = calcular_prioridade(
            escola, veiculos.get(nome_normalizado, {}))

        diretoria_stats[nome_normalizado]['escolas'] += 1
        if prioridade == 'high':
            diretoria_stats[nome_normalizado]['alta_prioridade'] += 1

    # Ordenar por número de veículos (descendente)
    diretorias_ordenadas = sorted(
        diretoria_stats.items(), key=lambda x: x[1]['veiculos'], reverse=True)

    print(f"\n📈 DADOS PARA O GRÁFICO (ordenado por veículos):")
    print(f"{'Diretoria':<25} {'Veículos':<8} {'Escolas':<8} {'Alta Prior.':<10} {'S1':<3} {'S2':<3} {'4X4':<3}")
    print("-" * 80)

    total_veiculos = 0
    total_escolas = 0
    total_alta_prioridade = 0

    for nome_norm, dados in diretorias_ordenadas:
        print(f"{dados['nome_original']:<25} {dados['veiculos']:<8} {dados['escolas']:<8} {dados['alta_prioridade']:<10} {dados['veiculos_detalhes']['s1']:<3} {dados['veiculos_detalhes']['s2']:<3} {dados['veiculos_detalhes']['s2_4x4']:<3}")

        total_veiculos += dados['veiculos']
        total_escolas += dados['escolas']
        total_alta_prioridade += dados['alta_prioridade']

    print("-" * 80)
    print(f"{'TOTAIS':<25} {total_veiculos:<8} {total_escolas:<8} {total_alta_prioridade:<10}")

    # Verificar problemas
    print(f"\n🔍 VERIFICAÇÕES:")
    problemas = []

    for nome_norm, dados in diretorias_ordenadas:
        if dados['veiculos'] == 0 and dados['escolas'] > 0:
            problemas.append(
                f"❌ {dados['nome_original']}: {dados['escolas']} escolas mas 0 veículos")
        elif dados['alta_prioridade'] > 0 and dados['veiculos'] == 0:
            problemas.append(
                f"⚠️  {dados['nome_original']}: {dados['alta_prioridade']} escolas alta prioridade mas 0 veículos")

    if problemas:
        print("\n🚨 PROBLEMAS ENCONTRADOS:")
        for problema in problemas[:5]:  # Mostrar apenas os primeiros 5
            print(f"  {problema}")
    else:
        print("✅ Nenhum problema encontrado na correlação veículos vs demanda")

    print(f"\n📊 RESUMO FINAL:")
    print(f"  • Diretorias com escolas: {len(diretorias_ordenadas)}")
    print(f"  • Total de escolas: {total_escolas}")
    print(
        f"  • Total de veículos nas diretorias com escolas: {total_veiculos}")
    print(f"  • Escolas de alta prioridade: {total_alta_prioridade}")

    return diretorias_ordenadas


if __name__ == "__main__":
    validar_grafico_demanda()
