import pandas as pd
import json


def converter_excel_para_js():
    """Converte o arquivo Excel de distâncias para dados JavaScript"""
    try:
        # Ler o arquivo Excel gerado
        df = pd.read_excel("distancias_escolas_diretorias.xlsx")

        # Converter para formato JavaScript
        schools_data = []

        for _, row in df.iterrows():
            # Determinar tipo
            tipo = "indigena" if row["Tipo_Escola"] == "Indígena" else "quilombola"

            school_data = {
                "name": row["Nome_Escola"],
                "type": tipo,
                "city": row["Cidade_Escola"],
                "diretoria": row["Nome_Diretoria"],
                "distance": (
                    float(row["Distancia_KM"])
                    if pd.notna(row["Distancia_KM"]) and row["Distancia_KM"] != "N/A"
                    else 0
                ),
                "lat": (
                    float(str(row["Latitude_Escola"]).replace(",", "."))
                    if pd.notna(row["Latitude_Escola"])
                    else 0
                ),
                "lng": (
                    float(str(row["Longitude_Escola"]).replace(",", "."))
                    if pd.notna(row["Longitude_Escola"])
                    else 0
                ),
                "de_lat": (
                    float(row["Latitude_Diretoria"])
                    if pd.notna(row["Latitude_Diretoria"])
                    else 0
                ),
                "de_lng": (
                    float(row["Longitude_Diretoria"])
                    if pd.notna(row["Longitude_Diretoria"])
                    else 0
                ),
            }

            schools_data.append(school_data)

        # Gerar código JavaScript
        js_code = f"""        // Dados das escolas com distâncias (gerado automaticamente)
        const schoolsData = {json.dumps(schools_data, indent=12, ensure_ascii=False)};"""

        # Ler o arquivo HTML atual
        with open("distancias_escolas.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        # Substituir os dados simulados pelos dados reais
        start_marker = "        // Dados das escolas com distâncias"
        end_marker = "        ];"

        start_index = html_content.find(start_marker)
        end_index = html_content.find(end_marker, start_index) + len(end_marker)

        if start_index != -1 and end_index != -1:
            new_html = html_content[:start_index] + js_code + html_content[end_index:]

            # Salvar arquivo atualizado
            with open("distancias_escolas.html", "w", encoding="utf-8") as f:
                f.write(new_html)

            print(f"✓ Arquivo HTML atualizado com {len(schools_data)} escolas")

            # Estatísticas
            indigenas = len([s for s in schools_data if s["type"] == "indigena"])
            quilombolas = len([s for s in schools_data if s["type"] == "quilombola"])
            distancias_validas = [
                s["distance"] for s in schools_data if s["distance"] > 0
            ]

            if distancias_validas:
                distancia_media = sum(distancias_validas) / len(distancias_validas)
                distancia_min = min(distancias_validas)
                distancia_max = max(distancias_validas)

                print(f"📊 ESTATÍSTICAS:")
                print(f"   - Escolas Indígenas: {indigenas}")
                print(f"   - Escolas Quilombolas/Assentamentos: {quilombolas}")
                print(f"   - Distância média: {distancia_media:.2f} km")
                print(f"   - Distância mínima: {distancia_min:.2f} km")
                print(f"   - Distância máxima: {distancia_max:.2f} km")

                # Atualizar estatísticas no HTML
                html_content = new_html
                html_content = html_content.replace(
                    'id="total-schools">59', f'id="total-schools">{len(schools_data)}'
                )
                html_content = html_content.replace(
                    'id="indigena-schools">43', f'id="indigena-schools">{indigenas}'
                )
                html_content = html_content.replace(
                    'id="quilombola-schools">16',
                    f'id="quilombola-schools">{quilombolas}',
                )
                html_content = html_content.replace(
                    'id="avg-distance">50.6', f'id="avg-distance">{distancia_media:.1f}'
                )

                with open("distancias_escolas.html", "w", encoding="utf-8") as f:
                    f.write(html_content)

                print("✓ Estatísticas atualizadas no HTML")
        else:
            print("❌ Erro: Não foi possível encontrar os marcadores no HTML")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("=== CONVERTENDO DADOS EXCEL PARA HTML ===")
    converter_excel_para_js()
