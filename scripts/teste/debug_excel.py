#!/usr/bin/env python3
import pandas as pd

# Ler Excel
df = pd.read_excel(
    "Relatorio_Completo_Escolas_Diretorias.xlsx", sheet_name="Todas as Escolas"
)

print("Estrutura do Excel:")
print("Colunas:", list(df.columns))
print("\nPrimeiras 3 linhas:")
print(df.head(3).to_string())

print("\nProcurando KOPENOTI nas primeiras colunas:")
for col in df.columns[:3]:
    if df[col].astype(str).str.contains("KOPENOTI", na=False, case=False).any():
        print(f"KOPENOTI encontrado na coluna: {col}")
        kopenoti_row = df[
            df[col].astype(str).str.contains("KOPENOTI", na=False, case=False)
        ]
        print("Dados da linha KOPENOTI:")
        print(kopenoti_row.iloc[0].to_string())
        break
