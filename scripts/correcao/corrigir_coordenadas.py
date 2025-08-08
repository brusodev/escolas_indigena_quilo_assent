# -*- coding: utf-8 -*-
"""
Script para corrigir coordenadas problemáticas na planilha distancias_escolas_diretorias.xlsx
"""

import pandas as pd
import numpy as np
import re


def corrigir_coordenadas():
    """Corrige coordenadas problemáticas na planilha"""

    print("🔧 CORRIGINDO COORDENADAS PROBLEMÁTICAS...")
    print("=" * 60)

    # Carregar dados
    df = pd.read_excel("distancias_escolas_diretorias.xlsx")

    print(f"📊 Total de registros: {len(df)}")

    # Mapeamento de coordenadas corretas para diretorias (baseado em pesquisa)
    coordenadas_diretorias = {
        "Avare": (-23.0998, -48.9267),
        "Caraguatatuba": (-23.6204, -45.4132),
        "Itarare": (-24.1083, -49.3342),
        "Miracatu": (-24.2854, -47.4588),
        "Mirante do Paranapanema": (-22.2847, -51.9088),  # Adicionado
        "Norte 1": (-23.5240, -46.6883),  # São Paulo - região Norte 1
        "Penapolis": (-21.4327, -50.0766),
        "Registro": (-24.4906, -47.8439),
        "Santo Anastacio": (-21.9758, -51.6514),
        "Santos": (-23.9336, -46.3255),
        "Sao Bernardo do Campo": (-23.7080, -46.5507),
        "Sao Vicente": (-23.9668, -46.3816),
        "Sul 3": (-23.7144, -46.7097),  # São Paulo - região Sul 3
        "Tupa": (-21.9349, -50.5141),
    }

    # Contador de correções
    correcoes = 0

    # Corrigir coordenadas das diretorias
    for i, row in df.iterrows():
        diretoria = row["Nome_Diretoria"]
        lat_atual = row["Latitude_Diretoria"]
        lng_atual = row["Longitude_Diretoria"]

        # Verificar se a coordenada está problemática (notação científica inválida ou fora dos limites)
        problema_lat = abs(lat_atual) > 90 or str(lat_atual).find("E+") != -1
        problema_lng = abs(lng_atual) > 180 or str(lng_atual).find("E+") != -1

        if problema_lat or problema_lng:
            if diretoria in coordenadas_diretorias:
                nova_lat, nova_lng = coordenadas_diretorias[diretoria]
                df.at[i, "Latitude_Diretoria"] = nova_lat
                df.at[i, "Longitude_Diretoria"] = nova_lng
                print(
                    f"✅ {diretoria}: {lat_atual},{lng_atual} → {nova_lat},{nova_lng}"
                )
                correcoes += 1
            else:
                print(f"⚠️  {diretoria}: Coordenadas não encontradas para correção")

    # Verificar coordenadas das escolas também
    escolas_corrigidas = 0
    for i, row in df.iterrows():
        lat_escola = row["Latitude_Escola"]
        lng_escola = row["Longitude_Escola"]

        # Converter strings com vírgula para float se necessário
        if isinstance(lat_escola, str):
            try:
                lat_escola = float(lat_escola.replace(",", "."))
                df.at[i, "Latitude_Escola"] = lat_escola
                escolas_corrigidas += 1
            except:
                pass

        if isinstance(lng_escola, str):
            try:
                lng_escola = float(lng_escola.replace(",", "."))
                df.at[i, "Longitude_Escola"] = lng_escola
                escolas_corrigidas += 1
            except:
                pass

    # Salvar arquivo corrigido
    df.to_excel("distancias_escolas_diretorias.xlsx", index=False)

    print(f"\n📊 RESUMO DAS CORREÇÕES:")
    print(f"   🔧 Diretorias corrigidas: {correcoes}")
    print(f"   🏫 Coordenadas de escolas formatadas: {escolas_corrigidas}")
    print(f"   ✅ Arquivo salvo: distancias_escolas_diretorias.xlsx")

    # Verificar se ainda há problemas
    lat_problemas = df[df["Latitude_Diretoria"].abs() > 90]
    lng_problemas = df[df["Longitude_Diretoria"].abs() > 180]

    if len(lat_problemas) == 0 and len(lng_problemas) == 0:
        print(f"   🎉 Todas as coordenadas estão agora dentro dos limites válidos!")
    else:
        print(
            f"   ⚠️  Ainda há {len(lat_problemas) + len(lng_problemas)} coordenadas problemáticas"
        )

    return df


if __name__ == "__main__":
    df_corrigido = corrigir_coordenadas()
