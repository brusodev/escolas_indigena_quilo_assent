#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para debugar problemas específicos no mapa interativo.
"""

import json


def debug_mapa_interativo():
    """Debuga problemas no mapa interativo."""

    print("🐛 DEBUG DO MAPA INTERATIVO")
    print("=" * 50)

    # Carregar dados das escolas
    try:
        with open(
            "dados/json/dados_escolas_atualizados.json", "r", encoding="utf-8"
        ) as f:
            escolas = json.load(f)
        print(f"✅ Escolas carregadas: {len(escolas)}")
    except Exception as e:
        print(f"❌ Erro ao carregar escolas: {e}")
        return

    # Carregar dados dos veículos do dashboard
    try:
        with open(
            "dashboard/dados_veiculos_diretorias.json", "r", encoding="utf-8"
        ) as f:
            dados_veiculos = json.load(f)
        diretorias_veiculos = dados_veiculos["diretorias"]
        print(f"✅ Dados de veículos carregados: {len(diretorias_veiculos)} diretorias")
    except Exception as e:
        print(f"❌ Erro ao carregar dados de veículos: {e}")
        return

    # Extrair diretorias únicas das escolas
    diretorias_escolas = set(escola["diretoria"] for escola in escolas)
    print(f"\n📊 Diretorias encontradas nas escolas: {len(diretorias_escolas)}")

    # Verificar correspondência
    print(f"\n🔍 VERIFICAÇÃO DE CORRESPONDÊNCIA:")

    # Função de normalização (como no dashboard)
    def normalize_name(name):
        normalized = name.upper().strip()
        mappings = {
            "SAO VICENTE": "SÃO VICENTE ",
            "SÃO VICENTE": "SÃO VICENTE ",
            "SAO BERNARDO DO CAMPO": "SÃO BERNARDO DO CAMPO",
            "SANTO ANASTACIO": "SANTO ANASTÁCIO",
            "PENAPOLIS": "PENÁPOLIS",
            "TUPA": "TUPÃ",
            "ITARARE": "ITARARÉ",
            "LESTE 5": "LESTE 5",
            "SUL 3": "SUL 3",
            "NORTE 1": "NORTE 1",
        }
        return mappings.get(normalized, normalized)

    problemas_encontrados = []

    for diretoria_escola in sorted(diretorias_escolas):
        diretoria_normalizada = normalize_name(diretoria_escola)

        if diretoria_normalizada in diretorias_veiculos:
            dados_veiculo = diretorias_veiculos[diretoria_normalizada]

            # Verificar se todos os campos existem
            campos_obrigatorios = ["total", "s1", "s2", "s2_4x4"]
            campos_faltando = [
                campo for campo in campos_obrigatorios if campo not in dados_veiculo
            ]

            if campos_faltando:
                problemas_encontrados.append(
                    {
                        "tipo": "campos_faltando",
                        "diretoria": diretoria_escola,
                        "normalizada": diretoria_normalizada,
                        "campos_faltando": campos_faltando,
                    }
                )
                print(
                    f"   ⚠️  {diretoria_escola} → {diretoria_normalizada}: Campos faltando: {campos_faltando}"
                )
            else:
                print(
                    f"   ✅ {diretoria_escola} → {diretoria_normalizada}: Total={dados_veiculo['total']} (S1={dados_veiculo['s1']}, S2={dados_veiculo['s2']}, S2_4x4={dados_veiculo['s2_4x4']})"
                )
        else:
            problemas_encontrados.append(
                {
                    "tipo": "nao_encontrada",
                    "diretoria": diretoria_escola,
                    "normalizada": diretoria_normalizada,
                }
            )
            print(f"   ❌ {diretoria_escola} → {diretoria_normalizada}: NÃO ENCONTRADA")

    # Resumo dos problemas
    if problemas_encontrados:
        print(f"\n⚠️  PROBLEMAS ENCONTRADOS: {len(problemas_encontrados)}")
        for problema in problemas_encontrados:
            if problema["tipo"] == "nao_encontrada":
                print(
                    f"   🔍 Verificar se '{problema['diretoria']}' deveria ter mapeamento especial"
                )
            elif problema["tipo"] == "campos_faltando":
                print(
                    f"   🔧 Corrigir dados de '{problema['diretoria']}': adicionar {problema['campos_faltando']}"
                )
    else:
        print(f"\n✅ NENHUM PROBLEMA ENCONTRADO!")
        print(f"   🎯 Todas as diretorias das escolas têm dados de veículos completos")

    # Verificar se existe ITARARE especificamente
    print(f"\n🎯 VERIFICAÇÃO ESPECÍFICA - ITARARE:")
    for escola in escolas:
        if "itarare" in escola["diretoria"].lower():
            diretoria_norm = normalize_name(escola["diretoria"])
            dados = diretorias_veiculos.get(diretoria_norm, {})
            print(f"   Escola: {escola['name']}")
            print(f"   Diretoria original: {escola['diretoria']}")
            print(f"   Diretoria normalizada: {diretoria_norm}")
            print(f"   Dados encontrados: {dados}")
            break

    return len(problemas_encontrados) == 0


if __name__ == "__main__":
    sucesso = debug_mapa_interativo()
    if sucesso:
        print(f"\n🎉 DASHBOARD DEVE ESTAR FUNCIONANDO CORRETAMENTE!")
    else:
        print(f"\n🔧 PROBLEMAS IDENTIFICADOS PRECISAM SER CORRIGIDOS.")
