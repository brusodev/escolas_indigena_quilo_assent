#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar se as diretorias faltantes realmente têm escolas.
"""

import pandas as pd


def verificar_diretorias_faltantes():
    """Verifica se as diretorias faltantes têm escolas indígenas/quilombolas."""

    print("🔍 VERIFICANDO DIRETORIAS FALTANTES")
    print("=" * 50)

    # Carregar dados
    try:
        df = pd.read_excel("dados/excel/diretorias_ensino_completo.xlsx")
        print(f"✅ Planilha carregada: {len(df)} escolas")
        print(f"📊 Colunas: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Erro ao carregar planilha: {e}")
        return

    # Diretorias que estão faltando
    diretorias_faltantes = [
        "BRAGANÇA PAULISTA",
        "FERNANDÓPOLIS",
        "JOSÉ BONIFÁCIO",
        "MARÍLIA",
    ]

    print(f"\n🔍 Verificando diretorias faltantes:")

    for diretoria in diretorias_faltantes:
        escolas = df[df["DIRETORIA"] == diretoria]
        print(f"\n📍 {diretoria}: {len(escolas)} escolas")

        if len(escolas) > 0:
            print("   Escolas encontradas:")
            for idx, escola in escolas.iterrows():
                print(f"   - {escola['ESCOLA']} ({escola.get('TIPO_ESCOLA', 'N/A')})")
        else:
            print("   ❌ Nenhuma escola encontrada")

    # Verificar quais diretorias realmente têm escolas indígenas/quilombolas/assentamento
    print(f"\n🔍 Verificando diretorias com escolas relevantes:")
    diretorias_relevantes = df["DIRETORIA"].unique()

    for diretoria in sorted(diretorias_relevantes):
        escolas = df[df["DIRETORIA"] == diretoria]
        if len(escolas) > 0:
            tipos = (
                escolas.get("TIPO_ESCOLA", pd.Series()).unique()
                if "TIPO_ESCOLA" in escolas.columns
                else ["N/A"]
            )
            print(
                f"   {diretoria}: {len(escolas)} escolas - Tipos: {', '.join([str(t) for t in tipos])}"
            )


if __name__ == "__main__":
    verificar_diretorias_faltantes()
