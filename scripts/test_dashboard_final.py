"""
Teste simulando exatamente o comportamento do dashboard
Data: 07/08/2025
"""

import json


def test_dashboard_behavior():
    """Simular comportamento exato do dashboard"""
    print("=== SIMULAÇÃO DO COMPORTAMENTO DO DASHBOARD ===\n")

    # Carregar dados como o dashboard faz
    with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        schoolsData = json.load(f)

    with open('dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
        vehicle_json = json.load(f)

    vehicleData = vehicle_json['diretorias']
    vehicleMetadata = vehicle_json['metadata']

    print(f"✅ Dados carregados:")
    print(f"  • {len(schoolsData)} escolas")
    print(f"  • {len(vehicleData)} diretorias com dados de veículo")
    print(
        f"  • {vehicleMetadata['total_veiculos']} veículos totais no sistema")
    print()

    # Função de normalização (igual à do dashboard corrigido)
    def normalizeDiretoriaName(name):
        if not name:
            return ''
        normalized = name.upper().strip()
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

    # Simular calculateStats() do dashboard
    totalVehicles = sum(v['total'] for v in vehicleData.values())
    highPrioritySchools = len([s for s in schoolsData if s['distance'] > 50])
    uniqueDiretorias = len(set(s['diretoria'] for s in schoolsData))
    diretoriasComVeiculos = len(
        [k for k, v in vehicleData.items() if v['total'] > 0])

    print("📊 ESTATÍSTICAS CALCULADAS (como o dashboard faz):")
    print(f"  • Total de veículos: {totalVehicles}")
    print(f"  • Escolas >50km: {highPrioritySchools}")
    print(f"  • Diretorias únicas: {uniqueDiretorias}")
    print(f"  • Diretorias com veículos: {diretoriasComVeiculos}")
    print()

    # Verificar algumas escolas específicas que estavam com problema
    escolas_teste = [
        "ALDEIA DE PARANAPUA",
        "ALDEIA NHAMANDU MIRIM",
        "GLEBA XV DE NOVEMBRO",
        "INDIA VANUIRE"
    ]

    print("🔍 VERIFICAÇÃO DE ESCOLAS ESPECÍFICAS:")
    for escola_nome in escolas_teste:
        escola = next(
            (s for s in schoolsData if s['name'] == escola_nome), None)
        if escola:
            diretoria_original = escola['diretoria']
            diretoria_normalizada = normalizeDiretoriaName(diretoria_original)
            vehicles = vehicleData.get(diretoria_normalizada, {'total': 0})

            print(f"  • {escola_nome}")
            print(
                f"    Diretoria: {diretoria_original} → {diretoria_normalizada}")
            print(f"    Veículos: {vehicles['total']}")
            print(f"    Distância: {escola['distance']:.1f} km")
            print()

    # Simular o gráfico de demanda
    print("📈 DADOS DO GRÁFICO VEÍCULOS vs DEMANDA:")
    diretoria_stats = {}

    for escola in schoolsData:
        diretoria_normalizada = normalizeDiretoriaName(escola['diretoria'])

        if diretoria_normalizada not in diretoria_stats:
            veiculos_info = vehicleData.get(
                diretoria_normalizada, {'total': 0, 's1': 0, 's2': 0, 's2_4x4': 0})
            diretoria_stats[diretoria_normalizada] = {
                'nome_original': escola['diretoria'],
                'escolas': 0,
                'veiculos': veiculos_info['total'],
                'veiculos_detalhes': veiculos_info
            }

        diretoria_stats[diretoria_normalizada]['escolas'] += 1

    # Ordenar por veículos (como no gráfico)
    diretorias_ordenadas = sorted(
        diretoria_stats.items(), key=lambda x: x[1]['veiculos'], reverse=True)

    print(f"{'Diretoria':<30} {'Veículos':<8} {'Escolas':<8}")
    print("-" * 50)

    total_veiculos_graf = 0
    total_escolas_graf = 0

    for diretoria_key, dados in diretorias_ordenadas:
        print(
            f"{dados['nome_original']:<30} {dados['veiculos']:<8} {dados['escolas']:<8}")
        total_veiculos_graf += dados['veiculos']
        total_escolas_graf += dados['escolas']

    print("-" * 50)
    print(f"{'TOTAIS':<30} {total_veiculos_graf:<8} {total_escolas_graf:<8}")

    print(f"\n🎯 VALORES FINAIS QUE DEVEM APARECER NO DASHBOARD:")
    print(f"  • Total de Escolas: {len(schoolsData)}")
    # Este deve ser 39, não 6!
    print(f"  • Total de Veículos: {total_veiculos_graf}")
    print(f"  • Diretorias: {uniqueDiretorias}")
    print(
        f"  • Distância Média: {sum(s['distance'] for s in schoolsData) / len(schoolsData):.1f} km")
    print(f"  • Escolas >50km: {highPrioritySchools}")


if __name__ == "__main__":
    test_dashboard_behavior()
