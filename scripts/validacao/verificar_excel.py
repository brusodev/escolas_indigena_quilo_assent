import pandas as pd

print("=== Verificando Relatório Excel Completo ===")

try:
    # Ler a planilha com header correto
    df = pd.read_excel(
        "Relatorio_Completo_Escolas_Diretorias.xlsx",
        sheet_name="Escolas Indigenas",
        header=2,
    )

    print("✅ Colunas encontradas:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1}. {col}")

    if len(df) > 0:
        print("\n📋 Primeira escola com endereços:")
        escola = df.iloc[0]
        print(f"Nome: {escola['Nome da Escola']}")
        print(f"Endereço da Escola: {escola['Endereço da Escola']}")
        print(f"Diretoria: {escola['Diretoria Responsável']}")
        print(f"Endereço da Diretoria: {escola['Endereço da Diretoria']}")
        print(f"Distância: {escola['Distância (km)']} km")

        print(f"\n📊 Total de escolas indígenas: {len(df)}")

        # Verificar se todas as escolas têm endereços
        escolas_com_endereco = df[df["Endereço da Escola"].notna()].shape[0]
        diretorias_com_endereco = df[df["Endereço da Diretoria"].notna()].shape[0]

        print(f"✅ Escolas com endereço: {escolas_com_endereco}/{len(df)}")
        print(f"✅ Diretorias com endereço: {diretorias_com_endereco}/{len(df)}")

except Exception as e:
    print(f"❌ Erro: {e}")

    # Tentar ver todas as abas
    try:
        xl_file = pd.ExcelFile("Relatorio_Completo_Escolas_Diretorias.xlsx")
        print(f"\nAbas disponíveis: {xl_file.sheet_names}")
    except Exception as e2:
        print(f"Erro ao ler abas: {e2}")
