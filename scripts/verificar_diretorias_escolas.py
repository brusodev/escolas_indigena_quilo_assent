#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar diretorias no arquivo de escolas.
"""

import json


def verificar_diretorias_escolas():
    """Verifica diretorias no arquivo de escolas."""

    print("🔍 VERIFICANDO DIRETORIAS NO ARQUIVO DE ESCOLAS")
    print("=" * 50)

    # Carregar dados das escolas
    try:
        with open(
            "dados/json/dados_escolas_atualizados.json", "r", encoding="utf-8"
        ) as f:
            escolas = json.load(f)
        print(f"✅ Arquivo de escolas carregado: {len(escolas)} escolas")
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo de escolas: {e}")
        return

    # Extrair diretorias únicas
    diretorias = set([escola["diretoria"] for escola in escolas])

    print(f"\n📊 Total de diretorias com escolas: {len(diretorias)}")
    print("\n🗂️  Diretorias encontradas:")
    for diretoria in sorted(diretorias):
        escolas_dir = [e for e in escolas if e["diretoria"] == diretoria]
        print(f"   - {diretoria}: {len(escolas_dir)} escolas")

    # Verificar diretorias específicas que estavam faltando
    diretorias_procuradas = [
        "BRAGANÇA PAULISTA",
        "FERNANDÓPOLIS",
        "JOSÉ BONIFÁCIO",
        "MARÍLIA",
    ]

    print(f"\n🔍 Verificando diretorias específicas:")
    for diretoria in diretorias_procuradas:
        encontrada = diretoria in diretorias
        status = "✅" if encontrada else "❌"
        print(f"   {status} {diretoria}")

        if encontrada:
            escolas_dir = [e for e in escolas if e["diretoria"] == diretoria]
            print(f"      - {len(escolas_dir)} escolas")
            for escola in escolas_dir:
                print(f"        • {escola['name']} ({escola['type']})")

    # Mapear diretorias com variações de nome
    print(f"\n🔍 Procurando por variações de nome:")
    for diretoria in diretorias_procuradas:
        encontradas = [
            d
            for d in diretorias
            if diretoria.lower() in d.lower() or d.lower() in diretoria.lower()
        ]
        if encontradas:
            print(f"   {diretoria}:")
            for encontrada in encontradas:
                print(f"      → {encontrada}")


if __name__ == "__main__":
    verificar_diretorias_escolas()
