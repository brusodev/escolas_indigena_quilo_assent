#!/usr/bin/env python3
"""
Script para verificar se os dados dinâmicos estão corretos.
"""

import json
import os


def verificar_dados_finais():
    print("🔍 VERIFICAÇÃO FINAL DOS DADOS DINÂMICOS")
    print("=" * 50)

    base_path = os.path.dirname(os.path.dirname(__file__))

    # Ler dados das escolas
    escolas_file = os.path.join(
        base_path, 'dados', 'json', 'dados_escolas_atualizados.json')
    with open(escolas_file, 'r', encoding='utf-8') as f:
        escolas = json.load(f)

    # Ler dados dos veículos
    veiculos_file = os.path.join(base_path, 'dados_veiculos_diretorias.json')
    with open(veiculos_file, 'r', encoding='utf-8') as f:
        veiculos = json.load(f)

    # Mapeamento de diretorias para corresponder aos nomes
    mapeamento_diretorias = {
        "Itarare": "ITARARÉ",
        "Penapolis": "PENÁPOLIS",
        "Santo Anastacio": "SANTO ANASTÁCIO",
        "Sao Bernardo do Campo": "SÃO BERNARDO DO CAMPO",
        "Tupa": "TUPÃ"
    }

    # Calcular diretorias únicas das escolas
    diretorias_escolas = set(escola['diretoria'] for escola in escolas)

    # Calcular veículos nas diretorias com escolas
    veiculos_relevantes = 0
    if 'diretorias' in veiculos:
        for diretoria in diretorias_escolas:
            # Usar mapeamento se necessário
            nome_veiculo = mapeamento_diretorias.get(
                diretoria, diretoria.upper())
            if nome_veiculo in veiculos['diretorias']:
                veiculos_relevantes += veiculos['diretorias'][nome_veiculo]['total']

    # Calcular escolas > 50km
    escolas_alta_prioridade = len([e for e in escolas if e['distance'] > 50])

    print(f"📊 RESULTADOS ESPERADOS NO DASHBOARD:")
    print(f"🏫 Total de escolas: {len(escolas)}")
    print(f"🚌 Veículos disponíveis: {veiculos_relevantes}")
    print(f"📍 Diretorias: {len(diretorias_escolas)}")
    print(f"🎯 Escolas >50km: {escolas_alta_prioridade}")
    print()

    print("✅ DADOS CORRETOS PARA O DASHBOARD:")
    print("✅ 63 escolas (37 indígenas + 26 quilombolas)")
    print("✅ 39 veículos nas diretorias relevantes")
    print("✅ 19 diretorias de ensino")
    print("✅ 25 escolas com prioridade alta (>50km)")
    print()

    # Verificar se os valores estão corretos
    if (len(escolas) == 63 and
        veiculos_relevantes == 39 and
        len(diretorias_escolas) == 19 and
            escolas_alta_prioridade == 25):
        print("🎉 PERFEITO! TODOS OS DADOS ESTÃO CORRETOS!")
        print("🎯 O dashboard deve mostrar exatamente estes valores.")
    else:
        print("⚠️  ATENÇÃO: Valores diferentes do esperado!")
        print(f"   Escolas: {len(escolas)} (esperado: 63)")
        print(f"   Veículos: {veiculos_relevantes} (esperado: 39)")
        print(f"   Diretorias: {len(diretorias_escolas)} (esperado: 19)")
        print(f"   Alta prioridade: {escolas_alta_prioridade} (esperado: 25)")


if __name__ == "__main__":
    verificar_dados_finais()
