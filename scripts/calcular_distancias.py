import pandas as pd
import numpy as np
from geopy.distance import geodesic
import openpyxl


def ler_dados():
    """Lê os dados das escolas e diretorias"""
    print("Carregando dados...")

    # Ler escolas (tentando diferentes encodings)
    try:
        escolas_df = pd.read_csv(
            "ENDERECO_ESCOLAS_062025 (1).csv", sep=";", encoding="utf-8"
        )
    except UnicodeDecodeError:
        try:
            escolas_df = pd.read_csv(
                "ENDERECO_ESCOLAS_062025 (1).csv", sep=";", encoding="latin-1"
            )
        except UnicodeDecodeError:
            escolas_df = pd.read_csv(
                "ENDERECO_ESCOLAS_062025 (1).csv", sep=";", encoding="cp1252"
            )

    # Filtrar apenas escolas indígenas e quilombolas/assentamentos
    escolas_filtradas = escolas_df[escolas_df["TIPOESC"].isin([10, 36])].copy()

    # Ler diretorias
    diretorias_df = pd.read_excel("diretorias_ensino_completo.xlsx")

    print(f"Total de escolas encontradas: {len(escolas_filtradas)}")
    print(
        f"- Escolas Indígenas (TIPOESC=10): {len(escolas_filtradas[escolas_filtradas['TIPOESC']==10])}"
    )
    print(
        f"- Escolas Quilombolas/Assentamentos (TIPOESC=36): {len(escolas_filtradas[escolas_filtradas['TIPOESC']==36])}"
    )
    print(f"Total de diretorias: {len(diretorias_df)}")

    return escolas_filtradas, diretorias_df


def geocodificar_diretorias(diretorias_df):
    """Converte endereços das diretorias em coordenadas usando a API do Nominatim"""
    from geopy.geocoders import Nominatim
    from time import sleep

    geolocator = Nominatim(user_agent="escola_distancia_calculator")
    diretorias_coords = []

    print("\nGeocoding diretorias de ensino...")

    for idx, row in diretorias_df.iterrows():
        try:
            # Montar endereço completo
            endereco = f"{row['Logradouro']}, {row['Número']}, {row['Bairro']}, {row['Cidade']}, SP, Brasil"

            print(
                f"Processando {idx+1}/{len(diretorias_df)}: {row['Nome da Diretoria']}"
            )

            location = geolocator.geocode(endereco, timeout=10)

            if location:
                diretorias_coords.append(
                    {
                        "nome": row["Nome da Diretoria"],
                        "cidade": row["Cidade"],
                        "endereco": endereco,
                        "endereco_completo": row["Endereço Completo"],
                        "latitude": location.latitude,
                        "longitude": location.longitude,
                    }
                )
                print(
                    f"  ✓ Coordenadas encontradas: {location.latitude}, {location.longitude}"
                )
            else:
                # Tentar só com cidade
                endereco_simples = f"{row['Cidade']}, SP, Brasil"
                location = geolocator.geocode(endereco_simples, timeout=10)

                if location:
                    diretorias_coords.append(
                        {
                            "nome": row["Nome da Diretoria"],
                            "cidade": row["Cidade"],
                            "endereco": endereco_simples,
                            "endereco_completo": row["Endereço Completo"],
                            "latitude": location.latitude,
                            "longitude": location.longitude,
                        }
                    )
                    print(
                        f"  ⚠ Usando coordenadas da cidade: {location.latitude}, {location.longitude}"
                    )
                else:
                    print(f"  ✗ Não foi possível geocodificar")
                    diretorias_coords.append(
                        {
                            "nome": row["Nome da Diretoria"],
                            "cidade": row["Cidade"],
                            "endereco": endereco,
                            "endereco_completo": row["Endereço Completo"],
                            "latitude": None,
                            "longitude": None,
                        }
                    )

            # Pausa para não sobrecarregar a API
            sleep(1)

        except Exception as e:
            print(f"  ✗ Erro: {e}")
            diretorias_coords.append(
                {
                    "nome": row["Nome da Diretoria"],
                    "cidade": row["Cidade"],
                    "endereco": endereco if "endereco" in locals() else "",
                    "endereco_completo": row["Endereço Completo"],
                    "latitude": None,
                    "longitude": None,
                }
            )

    return pd.DataFrame(diretorias_coords)


def relacionar_escola_diretoria(escolas_df, diretorias_df):
    """Relaciona cada escola com sua diretoria baseado no campo DE"""
    print("\nRelacionando escolas com diretorias...")

    # Criar mapeamento de diretorias
    mapeamento_diretorias = {}

    for _, diretoria in diretorias_df.iterrows():
        nome_diretoria = diretoria["nome"].upper().strip()

        # Mapeamentos conhecidos (você pode expandir esta lista)
        mapeamentos = {
            "NORTE 2": ["NOGUEIRA"],
            "CENTRO": ["SAO PAULO"],
            "CENTRO OESTE": ["SAO PAULO"],
            "CENTRO SUL": ["SAO PAULO"],
            "LESTE 1": ["SAO PAULO"],
            "LESTE 2": ["SAO PAULO"],
            "LESTE 3": ["SAO PAULO"],
            "LESTE 4": ["SAO PAULO"],
            "LESTE 5": ["SAO PAULO"],
            "NORTE 1": ["SAO PAULO"],
            "SUL 1": ["SAO PAULO"],
            "SUL 2": ["SAO PAULO"],
            "SUL 3": ["SAO PAULO"],
        }

        if nome_diretoria in mapeamentos:
            for cidade in mapeamentos[nome_diretoria]:
                mapeamento_diretorias[cidade] = diretoria
        else:
            # Para outras diretorias, usar o nome da cidade
            cidade_diretoria = diretoria["cidade"].upper().strip()
            mapeamento_diretorias[cidade_diretoria] = diretoria

    resultados = []

    for _, escola in escolas_df.iterrows():
        de_escola = escola["DE"].upper().strip()
        cidade_escola = escola["MUN"].upper().strip()

        # Tentar encontrar a diretoria
        diretoria_encontrada = None

        # Primeiro, tentar pelo nome da DE
        if de_escola in mapeamento_diretorias:
            diretoria_encontrada = mapeamento_diretorias[de_escola]
        # Se não encontrar, tentar pela cidade
        elif cidade_escola in mapeamento_diretorias:
            diretoria_encontrada = mapeamento_diretorias[cidade_escola]

        if diretoria_encontrada is not None:
            # Calcular distância se ambas as coordenadas existem
            distancia_km = None
            if (
                pd.notna(escola["DS_LATITUDE"])
                and pd.notna(escola["DS_LONGITUDE"])
                and pd.notna(diretoria_encontrada["latitude"])
                and pd.notna(diretoria_encontrada["longitude"])
            ):

                try:
                    # Converter coordenadas (substituir vírgula por ponto)
                    lat_escola = float(str(escola["DS_LATITUDE"]).replace(",", "."))
                    lng_escola = float(str(escola["DS_LONGITUDE"]).replace(",", "."))

                    coord_escola = (lat_escola, lng_escola)
                    coord_diretoria = (
                        diretoria_encontrada["latitude"],
                        diretoria_encontrada["longitude"],
                    )

                    distancia_km = round(
                        geodesic(coord_escola, coord_diretoria).kilometers, 2
                    )
                except:
                    distancia_km = "Erro no cálculo"

            tipo_escola = (
                "Indígena" if escola["TIPOESC"] == 10 else "Quilombola/Assentamento"
            )

            # Montar endereço completo da escola
            endereco_escola = f"{escola['ENDESC']}"
            if pd.notna(escola["NUMESC"]) and escola["NUMESC"] != "S/N":
                endereco_escola += f", {escola['NUMESC']}"
            if pd.notna(escola["BAIESC"]):
                endereco_escola += f", {escola['BAIESC']}"
            if pd.notna(escola["CEP"]):
                endereco_escola += f", CEP: {escola['CEP']}"

            resultados.append(
                {
                    "Nome_Escola": escola["NOMESC"],
                    "Tipo_Escola": tipo_escola,
                    "Cidade_Escola": escola["MUN"],
                    "Endereco_Escola": endereco_escola,
                    "DE_Responsavel": escola["DE"],
                    "Zona": "Rural" if escola["ZONA"] == 2 else "Urbana",
                    "Latitude_Escola": escola["DS_LATITUDE"],
                    "Longitude_Escola": escola["DS_LONGITUDE"],
                    "Nome_Diretoria": diretoria_encontrada["nome"],
                    "Cidade_Diretoria": diretoria_encontrada["cidade"],
                    "Endereco_Diretoria": diretoria_encontrada["endereco_completo"],
                    "Latitude_Diretoria": diretoria_encontrada["latitude"],
                    "Longitude_Diretoria": diretoria_encontrada["longitude"],
                    "Distancia_KM": distancia_km,
                }
            )
        else:
            # Escola sem diretoria encontrada
            tipo_escola = (
                "Indígena" if escola["TIPOESC"] == 10 else "Quilombola/Assentamento"
            )

            # Montar endereço completo da escola
            endereco_escola = f"{escola['ENDESC']}"
            if pd.notna(escola["NUMESC"]) and escola["NUMESC"] != "S/N":
                endereco_escola += f", {escola['NUMESC']}"
            if pd.notna(escola["BAIESC"]):
                endereco_escola += f", {escola['BAIESC']}"
            if pd.notna(escola["CEP"]):
                endereco_escola += f", CEP: {escola['CEP']}"

            resultados.append(
                {
                    "Nome_Escola": escola["NOMESC"],
                    "Tipo_Escola": tipo_escola,
                    "Cidade_Escola": escola["MUN"],
                    "Endereco_Escola": endereco_escola,
                    "DE_Responsavel": escola["DE"],
                    "Zona": "Rural" if escola["ZONA"] == 2 else "Urbana",
                    "Latitude_Escola": escola["DS_LATITUDE"],
                    "Longitude_Escola": escola["DS_LONGITUDE"],
                    "Nome_Diretoria": "NÃO ENCONTRADA",
                    "Cidade_Diretoria": "",
                    "Endereco_Diretoria": "",
                    "Latitude_Diretoria": None,
                    "Longitude_Diretoria": None,
                    "Distancia_KM": "N/A",
                }
            )

    return pd.DataFrame(resultados)


def main():
    print(
        "=== CALCULADORA DE DISTÂNCIAS: ESCOLAS INDÍGENAS/QUILOMBOLAS → DIRETORIAS DE ENSINO ===\n"
    )

    try:
        # 1. Ler dados
        escolas_df, diretorias_df = ler_dados()

        # 2. Geocodificar diretorias (se necessário)
        print("\n" + "=" * 60)
        opcao = (
            input("Deseja geocodificar as diretorias automaticamente? (s/n): ")
            .lower()
            .strip()
        )

        if opcao == "s":
            diretorias_coords = geocodificar_diretorias(diretorias_df)
            # Salvar coordenadas das diretorias
            diretorias_coords.to_excel("diretorias_com_coordenadas.xlsx", index=False)
            print(
                "\n✓ Coordenadas das diretorias salvas em 'diretorias_com_coordenadas.xlsx'"
            )
        else:
            # Tentar carregar coordenadas já salvas
            try:
                diretorias_coords = pd.read_excel("diretorias_com_coordenadas.xlsx")
                print("✓ Coordenadas das diretorias carregadas do arquivo existente")
            except FileNotFoundError:
                print(
                    "⚠ Arquivo de coordenadas não encontrado. Usando geocoding básico..."
                )
                diretorias_coords = geocodificar_diretorias(diretorias_df)

        # 3. Relacionar escolas com diretorias e calcular distâncias
        resultados = relacionar_escola_diretoria(escolas_df, diretorias_coords)

        # 4. Salvar resultados
        arquivo_resultado = "distancias_escolas_diretorias.xlsx"
        resultados.to_excel(arquivo_resultado, index=False)

        # 5. Exibir estatísticas
        print("\n" + "=" * 60)
        print("RESULTADOS:")
        print(f"✓ Total de escolas processadas: {len(resultados)}")
        print(
            f"  - Escolas Indígenas: {len(resultados[resultados['Tipo_Escola']=='Indígena'])}"
        )
        print(
            f"  - Escolas Quilombolas/Assentamentos: {len(resultados[resultados['Tipo_Escola']=='Quilombola/Assentamento'])}"
        )
        print(
            f"✓ Escolas com distância calculada: {len(resultados[pd.notna(resultados['Distancia_KM']) & (resultados['Distancia_KM'] != 'N/A')])}"
        )
        print(f"✓ Arquivo salvo: {arquivo_resultado}")

        # Mostrar algumas amostras
        print("\n📋 PRIMEIRAS 10 ESCOLAS:")
        print("-" * 80)
        for _, row in resultados.head(10).iterrows():
            print(f"🏫 {row['Nome_Escola']}")
            print(f"   Tipo: {row['Tipo_Escola']} | Cidade: {row['Cidade_Escola']}")
            print(f"   Diretoria: {row['Nome_Diretoria']} ({row['Cidade_Diretoria']})")
            print(f"   Distância: {row['Distancia_KM']} km")
            print()

        # Estatísticas de distância
        distancias_validas = resultados[
            pd.notna(resultados["Distancia_KM"])
            & (resultados["Distancia_KM"] != "N/A")
            & (resultados["Distancia_KM"] != "Erro no cálculo")
        ]
        if len(distancias_validas) > 0:
            distancias_numericas = pd.to_numeric(distancias_validas["Distancia_KM"])
            print(f"\n📊 ESTATÍSTICAS DE DISTÂNCIA:")
            print(f"   Distância média: {distancias_numericas.mean():.2f} km")
            print(f"   Distância mínima: {distancias_numericas.min():.2f} km")
            print(f"   Distância máxima: {distancias_numericas.max():.2f} km")
            print(f"   Mediana: {distancias_numericas.median():.2f} km")

    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
