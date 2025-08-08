#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNÓSTICO - Correspondência entre Diretorias e Dados de Veículos
"""

import pandas as pd
import json
import os


def diagnosticar_correspondencia():
    """Verifica correspondência entre diretorias das escolas e dados de veículos"""
    print("🔍 DIAGNÓSTICO DE CORRESPONDÊNCIA")
    print("=" * 50)

    # Carregar dados das escolas
    arquivo_escolas = (
        "dados/excel/distancias_escolas_diretorias_completo_63_corrigido.xlsx"
    )
    df_escolas = pd.read_excel(arquivo_escolas)

    # Carregar dados de veículos ORIGINAIS CORRETOS
    arquivo_veiculos = "dados/json/dados_veiculos_originais_corretos.json"
    with open(arquivo_veiculos, "r", encoding="utf-8") as f:
        dados_veiculos_reais = json.load(f)

    # Diretorias das escolas
    diretorias_escolas = set(df_escolas["DE_Responsavel"].unique())

    # Diretorias dos veículos
    diretorias_veiculos = set(dados_veiculos_reais.keys())

    print(f"📋 Total de diretorias nas escolas: {len(diretorias_escolas)}")
    print(f"🚗 Total de diretorias nos veículos: {len(diretorias_veiculos)}")
    print()

    print("🏫 DIRETORIAS DAS ESCOLAS:")
    for i, diretoria in enumerate(sorted(diretorias_escolas), 1):
        print(f"   {i:2d}. {diretoria}")
    print()

    # Verificar correspondência
    encontradas = []
    nao_encontradas = []

    for diretoria in diretorias_escolas:
        # Tentar várias variações
        variacoes = [
            diretoria,
            diretoria.upper(),
            diretoria.strip(),
            diretoria.strip().upper(),
            diretoria.replace("ã", "a").replace("ç", "c").replace("õ", "o"),
            diretoria.replace("Ã", "A").replace("Ç", "C").replace("Õ", "O"),
        ]

        encontrou = False
        veiculos_info = None

        for variacao in variacoes:
            if variacao in dados_veiculos_reais:
                encontradas.append(
                    (diretoria, variacao, dados_veiculos_reais[variacao])
                )
                encontrou = True
                break

        if not encontrou:
            nao_encontradas.append(diretoria)

    print(f"✅ DIRETORIAS ENCONTRADAS ({len(encontradas)}):")
    total_veiculos_encontrados = 0
    for original, encontrada, info in encontradas:
        total_veiculos_encontrados += info["total"]
        print(f"   📍 {original}")
        print(f"      ↳ Corresponde a: {encontrada}")
        print(
            f"      ↳ Veículos: {info['total']} (S1: {info['s1']}, S2: {info['s2']}, S2_4x4: {info['s2_4x4']})"
        )
        print()

    print(f"❌ DIRETORIAS NÃO ENCONTRADAS ({len(nao_encontradas)}):")
    for diretoria in nao_encontradas:
        print(f"   📍 {diretoria}")
    print()

    print("🔍 SUGESTÕES DE CORRESPONDÊNCIA:")
    for diretoria in nao_encontradas:
        print(f"\n📍 Procurando correspondência para: {diretoria}")
        # Buscar diretorias similares nos dados de veículos
        candidatos = []
        for veiculo_dir in diretorias_veiculos:
            # Verifica se há palavras em comum
            palavras_escola = set(diretoria.upper().split())
            palavras_veiculo = set(veiculo_dir.upper().split())

            if palavras_escola.intersection(palavras_veiculo):
                candidatos.append(veiculo_dir)

        if candidatos:
            print(f"   🎯 Possíveis correspondências:")
            for candidato in candidatos:
                info = dados_veiculos_reais[candidato]
                print(f"      - {candidato} ({info['total']} veículos)")
        else:
            print(f"   ⚠️  Nenhuma correspondência óbvia encontrada")

    print(f"\n📊 RESUMO:")
    print(f"   ✅ Diretorias com veículos: {len(encontradas)}")
    print(f"   ❌ Diretorias sem veículos: {len(nao_encontradas)}")
    print(f"   🚗 Total de veículos alocados: {total_veiculos_encontrados}")
    print(
        f"   📋 Taxa de correspondência: {len(encontradas)/len(diretorias_escolas)*100:.1f}%"
    )


if __name__ == "__main__":
    diagnosticar_correspondencia()
