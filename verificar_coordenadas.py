#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar coordenadas no CSV das escolas
"""

import pandas as pd

def verificar_coordenadas():
    csv_path = "dados/ENDERECO_ESCOLAS_062025 (1).csv"
    
    # Carregar dados
    df = pd.read_csv(csv_path, delimiter=';', encoding='latin-1')
    
    print(f"Total de registros: {len(df)}")
    print(f"Coordenadas latitude válidas: {df['DS_LATITUDE'].notna().sum()}")
    print(f"Coordenadas longitude válidas: {df['DS_LONGITUDE'].notna().sum()}")
    print(f"Ambas coordenadas válidas: {(df['DS_LATITUDE'].notna() & df['DS_LONGITUDE'].notna()).sum()}")
    
    # Verificar algumas escolas com coordenadas
    with_coords = df[(df['DS_LATITUDE'].notna()) & (df['DS_LONGITUDE'].notna())].head(3)
    print("\nEscolas com coordenadas (primeiras 3):")
    for _, escola in with_coords.iterrows():
        print(f"- {escola['NOMESC']}: ({escola['DS_LATITUDE']}, {escola['DS_LONGITUDE']})")
    
    # Verificar escolas indígenas especificamente
    indigenas = df[df['TIPOESC'] == 10]
    indigenas_com_coords = indigenas[(indigenas['DS_LATITUDE'].notna()) & (indigenas['DS_LONGITUDE'].notna())]
    
    print(f"\nEscolas Indígenas: {len(indigenas)} total")
    print(f"Escolas Indígenas com coordenadas: {len(indigenas_com_coords)}")
    
    if len(indigenas_com_coords) > 0:
        print("Exemplos de escolas indígenas com coordenadas:")
        for _, escola in indigenas_com_coords.head(3).iterrows():
            print(f"- {escola['NOMESC']}: ({escola['DS_LATITUDE']}, {escola['DS_LONGITUDE']})")

if __name__ == "__main__":
    verificar_coordenadas()
