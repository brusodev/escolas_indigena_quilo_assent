#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


def main():
    print("=== VERIFICANDO ESTRUTURA DO ARQUIVO DE DIRETORIAS ===\n")

    try:
        df = pd.read_excel('diretorias_com_coordenadas.xlsx')
        print(f"Colunas disponíveis: {list(df.columns)}")
        print(f"Número de linhas: {len(df)}")
        print(f"\nPrimeiras 3 linhas:")
        print(df.head(3))

    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        print("\nTentando outros arquivos de diretorias...")

        # Tentar outros arquivos
        arquivos_diretorias = [
            'diretorias_ensino_completo.xlsx',
            'GEP.xlsx'
        ]

        for arquivo in arquivos_diretorias:
            try:
                print(f"\nTentando: {arquivo}")
                df = pd.read_excel(arquivo)
                print(f"✅ Sucesso! Colunas: {list(df.columns)}")
                print(f"Número de linhas: {len(df)}")
                if len(df) > 0:
                    print(f"Primeira linha: {df.iloc[0].to_dict()}")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
