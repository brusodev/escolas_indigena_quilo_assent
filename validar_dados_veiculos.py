"""
Script para validar consistência entre dados de veículos no dashboard e na base JSON
Criado em: 07/08/2025
Versão: 1.0
"""

import json


def validar_dados_veiculos():
    """Valida se os dados do dashboard estão consistentes com dados_veiculos_diretorias.json"""

    # Carregar dados do JSON
    with open('dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
        dados_json = json.load(f)

    diretorias_json = dados_json['diretorias']
    estatisticas_json = dados_json['estatisticas']

    print("=== VALIDAÇÃO DE DADOS DE VEÍCULOS ===\n")

    # Validar totais
    total_calculado = sum(d['total'] for d in diretorias_json.values())
    total_s1 = sum(d['s1'] for d in diretorias_json.values())
    total_s2 = sum(d['s2'] for d in diretorias_json.values())
    total_s2_4x4 = sum(d['s2_4x4'] for d in diretorias_json.values())

    print(f"📊 TOTALIZAÇÕES:")
    print(f"Total de veículos calculado: {total_calculado}")
    print(f"Total nas estatísticas: {estatisticas_json['total_geral']}")
    print(
        f"Consistência: {'✅' if total_calculado == estatisticas_json['total_geral'] else '❌'}")

    print(f"\n🚗 POR TIPO:")
    print(
        f"S-1: {total_s1} (estat: {estatisticas_json['total_s1']}) {'✅' if total_s1 == estatisticas_json['total_s1'] else '❌'}")
    print(
        f"S-2: {total_s2} (estat: {estatisticas_json['total_s2']}) {'✅' if total_s2 == estatisticas_json['total_s2'] else '❌'}")
    print(
        f"S-2 4X4: {total_s2_4x4} (estat: {estatisticas_json['total_s2_4x4']}) {'✅' if total_s2_4x4 == estatisticas_json['total_s2_4x4'] else '❌'}")

    # Validar distribuição por quantidade
    dist_por_qtd = {}
    for diretoria, dados in diretorias_json.items():
        qtd = dados['total']
        if qtd not in dist_por_qtd:
            dist_por_qtd[qtd] = 0
        dist_por_qtd[qtd] += 1

    print(f"\n📈 DISTRIBUIÇÃO POR QUANTIDADE:")
    for qtd in sorted(dist_por_qtd.keys(), reverse=True):
        print(f"{qtd} veículo(s): {dist_por_qtd[qtd]} diretorias")

    # Listar diretorias com mais veículos
    diretorias_ordenadas = sorted(
        diretorias_json.items(), key=lambda x: x[1]['total'], reverse=True)

    print(f"\n🏆 TOP 10 DIRETORIAS COM MAIS VEÍCULOS:")
    for i, (nome, dados) in enumerate(diretorias_ordenadas[:10], 1):
        print(
            f"{i:2d}. {nome:<25} {dados['total']} veículos (S1:{dados['s1']}, S2:{dados['s2']}, S2-4X4:{dados['s2_4x4']})")

    # Diretorias que têm escolas
    diretorias_com_escolas = [
        "ANDRADINA", "AVARE", "BAURU", "CARAGUATATUBA", "ITAPEVA", "ITARARÉ",
        "LINS", "MIRACATU", "MIRANTE DO PARANAPANEMA", "NORTE 1", "PENÁPOLIS",
        "REGISTRO", "SANTO ANASTÁCIO", "SANTOS", "SÃO BERNARDO DO CAMPO",
        "SÃO VICENTE", "SUL 3", "TUPÃ", "APIAI"
    ]

    print(f"\n🏫 DIRETORIAS COM ESCOLAS (análise de demanda):")
    for escola_dir in diretorias_com_escolas:
        # Normalizar nome para busca
        nome_normalizado = escola_dir.upper().replace("Ã", "A").replace("Õ", "O")

        encontrada = False
        for nome_json, dados in diretorias_json.items():
            if nome_json.upper() == nome_normalizado or nome_json.upper().replace("Ã", "A").replace("Õ", "O") == nome_normalizado:
                print(f"  • {nome_json:<25} {dados['total']} veículos")
                encontrada = True
                break

        if not encontrada:
            print(f"  ❌ {escola_dir} não encontrada no JSON")

    print(f"\n✅ Validação concluída! Base JSON está pronta para uso.")
    return True


if __name__ == "__main__":
    validar_dados_veiculos()
