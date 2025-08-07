import pandas as pd

print("=== Verificando dados das escolas ===")

# Tentar com diferentes encodings
encodings = ["latin-1", "cp1252", "iso-8859-1"]

for encoding in encodings:
    try:
        print(f"\nTentando encoding: {encoding}")
        df = pd.read_csv("ENDERECO_ESCOLAS_062025 (1).csv", encoding=encoding, sep=";")
        print("✅ Sucesso!")
        print("Colunas:")
        print(df.columns.tolist())

        # Verificar se temos endereços
        if "ENDESC" in df.columns:
            print("\n📍 Coluna ENDESC encontrada (endereço da escola)")

            # Filtrar escolas indígenas e quilombolas
            escolas_filtradas = df[df["TIPOESC"].isin([10, 36])].copy()
            print(
                f"\nTotal de escolas indígenas e quilombolas: {len(escolas_filtradas)}"
            )

            if len(escolas_filtradas) > 0:
                print("\nExemplo de dados completos de uma escola:")
                escola_exemplo = escolas_filtradas.iloc[0]
                print(f"Nome: {escola_exemplo['NOMESC']}")
                print(
                    f"Endereço: {escola_exemplo['ENDESC']} {escola_exemplo['NUMESC']}"
                )
                print(f"Bairro: {escola_exemplo['BAIESC']}")
                print(f"CEP: {escola_exemplo['CEP']}")
                print(f"Cidade: {escola_exemplo['MUN']}")
                print(f"Zona: {escola_exemplo['ZONA']}")
                print(f"Tipo: {escola_exemplo['TIPOESC']}")

                # Mostrar os primeiros 3 registros com endereços
                print("\nPrimeiros 3 registros com endereços:")
                colunas_endereco = [
                    "NOMESC",
                    "ENDESC",
                    "NUMESC",
                    "BAIESC",
                    "CEP",
                    "MUN",
                ]
                print(
                    escolas_filtradas[colunas_endereco].head(3).to_string(index=False)
                )

        break  # Se funcionou, parar aqui

    except Exception as e:
        print(f"❌ Erro com {encoding}: {e}")
        continue
