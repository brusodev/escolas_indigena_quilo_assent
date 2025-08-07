import pandas as pd

print("=== Verificando dados das escolas ===")

# Tentar diferentes encodings
for encoding in ["utf-8", "latin-1", "cp1252"]:
    for sep in [",", ";", "\t"]:
        try:
            df = pd.read_csv(
                "ENDERECO_ESCOLAS_062025 (1).csv", encoding=encoding, sep=sep, nrows=5
            )
            print(f"\n✅ Sucesso com encoding={encoding}, sep='{sep}'")
            print("Colunas:")
            print(df.columns.tolist())

            # Verificar colunas de endereço
            cols_endereco = [
                col
                for col in df.columns
                if any(
                    word in col.upper()
                    for word in [
                        "ENDERECO",
                        "ENDEREÇO",
                        "LOGRADOURO",
                        "RUA",
                        "AVENIDA",
                        "ADDRESS",
                    ]
                )
            ]
            if cols_endereco:
                print(f"Colunas de endereço encontradas: {cols_endereco}")
            else:
                print("❌ Nenhuma coluna de endereço identificada")

            print("\nPrimeiro registro:")
            print(df.iloc[0].to_string())
            break
        except Exception as e:
            continue
    else:
        continue
    break

print("\n=== Verificando dados processados ===")

# Verificar dados já processados
df_processado = pd.read_excel("distancias_escolas_diretorias.xlsx")
print("Colunas no arquivo processado:")
print(df_processado.columns.tolist())

print(f"\nTotal de escolas processadas: {len(df_processado)}")
print(
    f"Escolas indígenas: {len(df_processado[df_processado['Tipo_Escola'] == 'Indígena'])}"
)
print(
    f"Escolas quilombolas/assentamento: {len(df_processado[df_processado['Tipo_Escola'] == 'Quilombola/Assentamento'])}"
)
