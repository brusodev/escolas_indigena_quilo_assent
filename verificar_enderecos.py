import pandas as pd

print("=== Verificando dados das escolas com separador correto ===")

# O arquivo parece ter ; como separador baseado na saída anterior
try:
    df = pd.read_csv("ENDERECO_ESCOLAS_062025 (1).csv", encoding="utf-8", sep=";")
    print("✅ Sucesso com separador ';'")
    print("Colunas:")
    print(df.columns.tolist())

    # Verificar se temos endereços
    if "ENDESC" in df.columns:
        print("\n📍 Coluna ENDESC encontrada (endereço da escola)")
        print("Exemplo de endereços:")
        print(df[["NOMESC", "ENDESC", "NUMESC", "BAIESC", "CEP"]].head(3).to_string())

    # Filtrar escolas indígenas e quilombolas
    escolas_filtradas = df[df["TIPOESC"].isin([10, 36])]
    print(f"\nTotal de escolas indígenas e quilombolas: {len(escolas_filtradas)}")

    print("\nExemplo de dados completos de uma escola:")
    if len(escolas_filtradas) > 0:
        escola_exemplo = escolas_filtradas.iloc[0]
        print(f"Nome: {escola_exemplo['NOMESC']}")
        print(f"Endereço: {escola_exemplo['ENDESC']} {escola_exemplo['NUMESC']}")
        print(f"Bairro: {escola_exemplo['BAIESC']}")
        print(f"CEP: {escola_exemplo['CEP']}")
        print(f"Cidade: {escola_exemplo['MUN']}")

except Exception as e:
    print(f"Erro: {e}")
