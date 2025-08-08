#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para diagnosticar diferenças entre os dados corretos e a base principal.
"""

import json


def diagnosticar_diferencias():
    """Diagnostica diferenças entre os arquivos de dados."""

    print("🔍 DIAGNÓSTICO DE DIFERENÇAS NOS DADOS")
    print("=" * 50)

    # Diretorias relevantes
    diretorias_relevantes = [
        "ADAMANTINA",
        "AMERICANA",
        "ARAÇATUBA",
        "ARARAQUARA",
        "BAURU",
        "BOTUCATU",
        "BRAGANÇA PAULISTA",
        "CARAPICUÍBA",
        "DIADEMA",
        "FERNANDÓPOLIS",
        "GUARULHOS NORTE",
        "GUARULHOS SUL",
        "ITAPECERICA DA SERRA",
        "JALES",
        "JOSÉ BONIFÁCIO",
        "MARÍLIA",
        "OSASCO",
        "PRESIDENTE PRUDENTE",
        "TUPÃ",
    ]

    # Carregar ambos os arquivos
    try:
        with open(
            "dados/json/dados_veiculos_originais_corretos.json", "r", encoding="utf-8"
        ) as f:
            dados_corretos = json.load(f)

        with open(
            "dados/json/dados_veiculos_atualizados.json", "r", encoding="utf-8"
        ) as f:
            dados_atualizados = json.load(f)

        print("✅ Ambos os arquivos carregados com sucesso")
    except Exception as e:
        print(f"❌ Erro ao carregar arquivos: {e}")
        return

    print(f"\n📊 Diretorias relevantes esperadas: {len(diretorias_relevantes)}")

    # Verificar presença de cada diretoria
    print("\n🔍 Verificando presença das diretorias relevantes:")
    diretorias_presentes_corretos = 0
    diretorias_presentes_atualizados = 0
    diretorias_faltando = []

    for diretoria in diretorias_relevantes:
        presente_corretos = diretoria in dados_corretos
        presente_atualizados = diretoria in dados_atualizados

        status_corretos = "✅" if presente_corretos else "❌"
        status_atualizados = "✅" if presente_atualizados else "❌"

        print(
            f"   {diretoria:25} | Corretos: {status_corretos} | Atualizados: {status_atualizados}"
        )

        if presente_corretos:
            diretorias_presentes_corretos += 1
        if presente_atualizados:
            diretorias_presentes_atualizados += 1
        if not presente_atualizados:
            diretorias_faltando.append(diretoria)

    print(f"\n📈 Resumo:")
    print(
        f"   Presentes em dados corretos: {diretorias_presentes_corretos}/{len(diretorias_relevantes)}"
    )
    print(
        f"   Presentes em dados atualizados: {diretorias_presentes_atualizados}/{len(diretorias_relevantes)}"
    )

    if diretorias_faltando:
        print(f"\n⚠️  Diretorias faltando nos dados atualizados:")
        for diretoria in diretorias_faltando:
            print(f"   - {diretoria}")

    # Calcular totais de veículos
    print(f"\n🚗 Contagem de veículos:")

    # Dados corretos
    total_corretos = 0
    s1_corretos = 0
    s2_corretos = 0
    s2_4x4_corretos = 0

    for diretoria in diretorias_relevantes:
        if diretoria in dados_corretos:
            dados_dir = dados_corretos[diretoria]
            total_corretos += dados_dir.get("total", 0)
            s1_corretos += dados_dir.get("s1", 0)
            s2_corretos += dados_dir.get("s2", 0)
            s2_4x4_corretos += dados_dir.get("s2_4x4", 0)

    # Dados atualizados
    total_atualizados = 0
    s1_atualizados = 0
    s2_atualizados = 0
    s2_4x4_atualizados = 0

    for diretoria in diretorias_relevantes:
        if diretoria in dados_atualizados:
            dados_dir = dados_atualizados[diretoria]
            total_atualizados += dados_dir.get("total", 0)
            s1_atualizados += dados_dir.get("s1", 0)
            s2_atualizados += dados_dir.get("s2", 0)
            s2_4x4_atualizados += dados_dir.get("s2_4x4", 0)

    print(
        f"   Dados corretos: {total_corretos} veículos (S1={s1_corretos}, S2={s2_corretos}, S2_4x4={s2_4x4_corretos})"
    )
    print(
        f"   Dados atualizados: {total_atualizados} veículos (S1={s1_atualizados}, S2={s2_atualizados}, S2_4x4={s2_4x4_atualizados})"
    )

    # Verificar diferenças detalhadas
    print(f"\n🔍 Diferenças detalhadas por diretoria:")
    for diretoria in diretorias_relevantes:
        if diretoria in dados_corretos and diretoria in dados_atualizados:
            correto = dados_corretos[diretoria]
            atualizado = dados_atualizados[diretoria]

            if (
                correto.get("total", 0) != atualizado.get("total", 0)
                or correto.get("s1", 0) != atualizado.get("s1", 0)
                or correto.get("s2", 0) != atualizado.get("s2", 0)
                or correto.get("s2_4x4", 0) != atualizado.get("s2_4x4", 0)
            ):

                print(f"   ⚠️  {diretoria}:")
                print(
                    f"      Correto: {correto.get('total', 0)} (S1={correto.get('s1', 0)}, S2={correto.get('s2', 0)}, S2_4x4={correto.get('s2_4x4', 0)})"
                )
                print(
                    f"      Atual:   {atualizado.get('total', 0)} (S1={atualizado.get('s1', 0)}, S2={atualizado.get('s2', 0)}, S2_4x4={atualizado.get('s2_4x4', 0)})"
                )


if __name__ == "__main__":
    diagnosticar_diferencias()
