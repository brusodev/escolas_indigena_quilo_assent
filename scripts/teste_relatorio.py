#!/usr/bin/env python3
"""
Teste simples dos relatórios
"""

import pandas as pd

# Verificar Excel
file = 'Relatorio_Completo_Escolas_Diretorias.xlsx'
df = pd.read_excel(file, sheet_name='Todas as Escolas')

print(f"Total de escolas: {len(df)}")
print("Colunas:", list(df.columns))

# Procurar KOPENOTI
kopenoti = df[df['Nome da Escola'].str.contains('KOPENOTI', na=False, case=False)]
if not kopenoti.empty:
    distancia = kopenoti.iloc[0]['Distância (km)']
    print(f"KOPENOTI: {distancia:.2f} km")
    
    if abs(distancia - 27.16) < 0.1:
        print("✅ Dados Haversine corretos!")
    else:
        print("❌ Dados incorretos!")
else:
    print("❌ KOPENOTI não encontrado")
