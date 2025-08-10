#!/usr/bin/env python3
"""
Script para debugar correspondência entre diretorias.
"""

import json
import os


def debug_diretorias():
    print("🔍 DEBUG - CORRESPONDÊNCIA DE DIRETORIAS")
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

    # Extrair diretorias das escolas
    diretorias_escolas = sorted(set(escola['diretoria'] for escola in escolas))

    # Extrair diretorias dos veículos
    diretorias_veiculos = sorted(veiculos['diretorias'].keys())

    print("📋 DIRETORIAS DAS ESCOLAS:")
    for i, diretoria in enumerate(diretorias_escolas, 1):
        print(f"{i:2d}. {diretoria}")

    print(f"\nTotal: {len(diretorias_escolas)} diretorias")

    print("\n🚌 DIRETORIAS DOS VEÍCULOS:")
    for i, diretoria in enumerate(diretorias_veiculos, 1):
        veiculos_total = veiculos['diretorias'][diretoria]['total']
        print(f"{i:2d}. {diretoria} ({veiculos_total} veículos)")

    print(f"\nTotal: {len(diretorias_veiculos)} diretorias")

    # Verificar correspondências
    print("\n🔄 VERIFICANDO CORRESPONDÊNCIAS:")
    veiculos_encontrados = 0
    diretorias_correspondentes = 0

    for escola_dir in diretorias_escolas:
        encontrou = False
        for veiculo_dir in diretorias_veiculos:
            if escola_dir.upper() == veiculo_dir.upper():
                veiculos_count = veiculos['diretorias'][veiculo_dir]['total']
                veiculos_encontrados += veiculos_count
                diretorias_correspondentes += 1
                print(
                    f"✅ {escola_dir} ↔ {veiculo_dir} ({veiculos_count} veículos)")
                encontrou = True
                break

        if not encontrou:
            print(f"❌ {escola_dir} (não encontrada)")

    print(f"\n📊 RESULTADO:")
    print(f"✅ Diretorias correspondentes: {diretorias_correspondentes}")
    print(f"🚌 Total de veículos encontrados: {veiculos_encontrados}")

    if veiculos_encontrados == 39:
        print("🎉 PERFEITO! Total de veículos correto!")
    else:
        print(f"⚠️  Esperado: 39 veículos, encontrado: {veiculos_encontrados}")


if __name__ == "__main__":
    debug_diretorias()
