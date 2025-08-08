#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrigir dados faltantes nas escolas adicionadas
"""

import pandas as pd


def corrigir_dados_escolas():
    """Corrige dados faltantes nas escolas"""
    print("🔧 CORRIGINDO DADOS DAS ESCOLAS")
    print("=" * 50)

    # Carregar arquivo
    df = pd.read_excel("distancias_escolas_diretorias_completo_63.xlsx")
    print(f"📊 Total de escolas: {len(df)}")

    # Verificar dados faltantes
    print("\n📋 Dados faltantes:")
    nans = df.isnull().sum()
    for col, count in nans.items():
        if count > 0:
            print(f"   {col}: {count} valores NaN")

    # Corrigir Zona para escolas sem zona (assumir Rural por serem indígenas/quilombolas)
    df["Zona"] = df["Zona"].fillna("Rural")

    # Corrigir outros campos vazios
    df["Endereco_Escola"] = df["Endereco_Escola"].fillna("Não informado")

    # Verificar escolas específicas que foram adicionadas
    escolas_adicionadas = [
        "BAIRRO DE BOMBAS",
        "BAIRRO BOMBAS DE CIMA",
        "FAZENDA DA CAIXA",
        "MARIA ANTONIA CHULES PRINCS",
    ]

    print(f"\n✅ ESCOLAS ADICIONADAS:")
    for escola in escolas_adicionadas:
        row = df[df["Nome_Escola"].str.contains(escola, na=False, case=False)]
        if not row.empty:
            idx = row.index[0]
            print(f"   {escola}: Zona = {df.loc[idx, 'Zona']}")

            # Garantir que tipo está correto
            if pd.isna(df.loc[idx, "Tipo_Escola"]) or df.loc[idx, "Tipo_Escola"] == "":
                df.loc[idx, "Tipo_Escola"] = "Quilombola/Assentamento"
                print(f"      Tipo corrigido para: Quilombola/Assentamento")

    # Salvar arquivo corrigido
    df.to_excel("distancias_escolas_diretorias_completo_63.xlsx", index=False)

    print(f"\n💾 Arquivo salvo com correções")

    # Verificar novamente
    print(f"\n🔍 VERIFICAÇÃO FINAL:")
    nans_final = df.isnull().sum()
    for col, count in nans_final.items():
        if count > 0:
            print(f"   {col}: {count} valores NaN restantes")

    if nans_final.sum() == 0:
        print("✅ Todos os dados obrigatórios preenchidos!")

    return df


if __name__ == "__main__":
    df = corrigir_dados_escolas()
