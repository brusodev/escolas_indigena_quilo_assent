import pandas as pd
import os


def mostrar_dados_atuais():
    """Mostra os dados atuais para facilitar a edição"""

    print("=" * 80)
    print("📋 DADOS ATUAIS PARA EDIÇÃO")
    print("=" * 80)

    # 1. Coordenadas das escolas
    print("\n📍 COORDENADAS DAS ESCOLAS (primeiras 10):")
    print("-" * 50)
    try:
        df_escolas = pd.read_excel("distancias_escolas_diretorias.xlsx")
        print("Arquivo: distancias_escolas_diretorias.xlsx")
        print("Colunas para editar: Latitude_Escola (G) e Longitude_Escola (H)")
        print()
        print(
            df_escolas[
                ["Nome_Escola", "Cidade_Escola", "Latitude_Escola", "Longitude_Escola"]
            ]
            .head(10)
            .to_string(index=False)
        )
        print(f"\n... e mais {len(df_escolas)-10} escolas")
    except Exception as e:
        print(f"❌ Erro ao ler coordenadas: {e}")

    # 2. Veículos por diretoria
    print("\n\n🚗 VEÍCULOS POR DIRETORIA:")
    print("-" * 50)
    try:
        df_veiculos = pd.read_excel("QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx")
        print("Arquivo: QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx")
        print("Colunas: DIRETORIA, QUANTIDADE S-1, QUANTIDADE S-2, QUANTIDADE S-2 4X4")
        print()
        print(df_veiculos.to_string(index=False))
    except Exception as e:
        print(f"❌ Erro ao ler veículos: {e}")

    # 3. Supervisão
    print("\n\n👥 SUPERVISÃO (GEP):")
    print("-" * 50)
    try:
        df_gep = pd.read_excel("GEP.xlsx")
        print("Arquivo: GEP.xlsx")
        print(
            "Colunas: REGIÃO, DIRETORIA DE ENSINO SOB SUPERVISÃO, QUANTIDADE DE DEs, SUPERVISOR GEP"
        )
        print()
        print(df_gep.to_string(index=False))
    except Exception as e:
        print(f"❌ Erro ao ler GEP: {e}")

    # 4. Lista de diretorias para referência
    print("\n\n📝 DIRETORIAS DISPONÍVEIS (para referência):")
    print("-" * 50)
    try:
        diretorias_unicas = df_escolas["Nome_Diretoria"].unique()
        print("Use EXATAMENTE estes nomes nas planilhas de veículos e GEP:")
        for i, diretoria in enumerate(sorted(diretorias_unicas), 1):
            print(f"{i:2d}. {diretoria}")
    except:
        print("❌ Não foi possível listar diretorias")

    print("\n" + "=" * 80)
    print("💡 INSTRUÇÕES:")
    print("1. Edite os arquivos Excel conforme necessário")
    print("2. Use a opção 8️⃣ do menu para regenerar TODOS os relatórios")
    print("3. Ou use opção 7️⃣ se alterou coordenadas no CSV original")
    print("=" * 80)


if __name__ == "__main__":
    mostrar_dados_atuais()
