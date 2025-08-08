# -*- coding: utf-8 -*-
import pandas as pd
import json
import os


def analisar_planilha_veiculos():
    """Analisa a estrutura da planilha de veículos"""
    print("🔍 ANALISANDO PLANILHA DE VEÍCULOS...")
    print("=" * 60)

    try:
        # Carregar a planilha
        df = pd.read_excel("QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx")

        print(f"📊 Dados carregados: {len(df)} linhas")
        print(f"📋 Colunas: {list(df.columns)}")
        print("\n📝 Primeiras 10 linhas:")
        print(df.head(10).to_string())

        print("\n📈 Estatísticas básicas:")
        print(df.describe())

        print("\n🚗 Resumo de veículos por tipo:")
        if 'QUANTIDADE S-1' in df.columns:
            print(f"   S-1: {df['QUANTIDADE S-1'].sum()}")
        if 'QUANTIDADE S-2' in df.columns:
            print(f"   S-2: {df['QUANTIDADE S-2'].sum()}")
        if 'QUANTIDADE S-2 4X4' in df.columns:
            print(f"   S-2 4X4: {df['QUANTIDADE S-2 4X4'].sum()}")

        # Verificar valores nulos
        print("\n❌ Valores nulos por coluna:")
        print(df.isnull().sum())

        # Verificar diretorias únicas
        if 'DIRETORIA' in df.columns:
            print(f"\n📍 Total de diretorias: {df['DIRETORIA'].nunique()}")
            print("\n📋 Lista de diretorias:")
            for i, diretoria in enumerate(sorted(df['DIRETORIA'].unique()), 1):
                print(f"   {i:2d}. {diretoria}")

        return df

    except Exception as e:
        print(f"❌ Erro ao analisar planilha: {e}")
        return None


if __name__ == "__main__":
    analisar_planilha_veiculos()
