import pandas as pd

print("=== Verificando Planilha Quilombolas/Assentamentos ===")

try:
    # Ler a planilha de quilombolas
    df = pd.read_excel(
        "Relatorio_Completo_Escolas_Diretorias.xlsx",
        sheet_name="Quilombolas e Assentamentos",
        header=2,
    )

    print(f"📊 Total de escolas quilombolas/assentamentos: {len(df)}")

    if len(df) > 0:
        print("\n📋 Primeira escola quilombola com endereços:")
        escola = df.iloc[0]
        print(f"Nome: {escola['Nome da Escola']}")
        print(f"Endereço da Escola: {escola['Endereço da Escola']}")
        print(f"Diretoria: {escola['Diretoria Responsável']}")
        print(f"Endereço da Diretoria: {escola['Endereço da Diretoria']}")
        print(f"Distância: {escola['Distância (km)']} km")

        # Verificar se todas as escolas têm endereços
        escolas_com_endereco = df[df["Endereço da Escola"].notna()].shape[0]
        diretorias_com_endereco = df[df["Endereço da Diretoria"].notna()].shape[0]

        print(f"\n✅ Escolas com endereço: {escolas_com_endereco}/{len(df)}")
        print(f"✅ Diretorias com endereço: {diretorias_com_endereco}/{len(df)}")

        # Verificar endereços únicos
        print(
            f"\n📍 Diretorias únicas atendendo quilombolas: {df['Diretoria Responsável'].nunique()}"
        )
        print("Diretorias:")
        for diretoria in df["Diretoria Responsável"].unique():
            count = df[df["Diretoria Responsável"] == diretoria].shape[0]
            print(f"  • {diretoria}: {count} escola(s)")

except Exception as e:
    print(f"❌ Erro: {e}")

print("\n=== Verificando Planilha Consolidada ===")

try:
    # Verificar também a planilha consolidada
    df_todas = pd.read_excel(
        "Relatorio_Completo_Escolas_Diretorias.xlsx",
        sheet_name="Todas as Escolas",
        header=2,
    )

    print(f"📊 Total de escolas na planilha consolidada: {len(df_todas)}")

    # Contar por tipo
    indigenas = df_todas[df_todas["Tipo"] == "Indígena"].shape[0]
    quilombolas = df_todas[df_todas["Tipo"] == "Quilombola/Assentamento"].shape[0]

    print(f"   - Indígenas: {indigenas}")
    print(f"   - Quilombolas/Assentamentos: {quilombolas}")

    print(
        f"\n✅ Todas as escolas têm endereços: {df_todas['Endereço da Escola'].notna().all()}"
    )
    print(
        f"✅ Todas as diretorias têm endereços: {df_todas['Endereço da Diretoria'].notna().all()}"
    )

except Exception as e:
    print(f"❌ Erro na planilha consolidada: {e}")
