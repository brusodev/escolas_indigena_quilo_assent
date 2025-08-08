#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import json


def verificar_dados_veiculos():
    """Verifica e corrige os dados dos veículos"""

    print("🔍 Verificando dados dos veículos...")

    # Carregar planilha
    df = pd.read_excel('QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx')

    print(f"📊 Planilha carregada com {len(df)} linhas")
    print(f"📋 Colunas: {list(df.columns)}")

    print("\n🔍 Primeiras 10 linhas:")
    print(df.head(10))

    print("\n🔍 Dados únicos por coluna:")
    for col in df.columns:
        print(f"  {col}: {df[col].nunique()} valores únicos")

    # Verificar se há valores vazios
    print("\n❌ Valores vazios por coluna:")
    print(df.isnull().sum())

    # Calcular totais
    print("\n📊 RESUMO DOS VEÍCULOS:")

    if 'S-1' in df.columns:
        total_s1 = df['S-1'].fillna(0).sum()
        print(f"  S-1: {total_s1}")

    if 'S-2' in df.columns:
        total_s2 = df['S-2'].fillna(0).sum()
        print(f"  S-2: {total_s2}")

    if 'S-2 4X4' in df.columns:
        total_s2_4x4 = df['S-2 4X4'].fillna(0).sum()
        print(f"  S-2 4X4: {total_s2_4x4}")

    total_geral = 0
    for col in ['S-1', 'S-2', 'S-2 4X4']:
        if col in df.columns:
            total_geral += df[col].fillna(0).sum()

    print(f"  TOTAL GERAL: {total_geral}")

    print("\n🏢 DIRETORIAS COM VEÍCULOS:")
    for _, row in df.iterrows():
        diretoria = row['DIRETORIA']
        s1 = row.get('S-1', 0) or 0
        s2 = row.get('S-2', 0) or 0
        s2_4x4 = row.get('S-2 4X4', 0) or 0
        total = s1 + s2 + s2_4x4

        if total > 0:
            print(
                f"  • {diretoria}: {total} veículos (S-1: {s1}, S-2: {s2}, S-2 4X4: {s2_4x4})")


def main():
    verificar_dados_veiculos()


if __name__ == "__main__":
    main()
