#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula a distância haversine entre dois pontos em km"""
    R = 6371  # Raio da Terra em km

    # Converter para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Diferenças
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def main():
    print("=== CORRIGINDO DISTÂNCIA DA ALDEIA KOPENOTI ===\n")

    # 1. Carregar dados das escolas
    with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        escolas_data = json.load(f)

    # 2. Encontrar e corrigir ALDEIA KOPENOTI
    escola_corrigida = False
    for i, escola in enumerate(escolas_data):
        if escola.get('name') == 'ALDEIA KOPENOTI':
            print(f"1. ESCOLA ENCONTRADA:")
            print(f"   Nome: {escola['name']}")
            print(f"   Distância ANTERIOR: {escola['distance']} km")

            # Recalcular distância correta
            distancia_correta = haversine_distance(
                escola['lat'], escola['lng'],
                escola['de_lat'], escola['de_lng']
            )

            print(f"   Distância CORRETA: {distancia_correta:.2f} km")
            print(
                f"   Diferença: {abs(escola['distance'] - distancia_correta):.2f} km")

            # Atualizar a distância
            escolas_data[i]['distance'] = round(distancia_correta, 2)
            escola_corrigida = True

            print(f"   ✅ Distância corrigida para {distancia_correta:.2f} km")
            break

    if not escola_corrigida:
        print("❌ ALDEIA KOPENOTI não encontrada!")
        return

    # 3. Verificar se há outras escolas com distâncias suspeitas
    print(f"\n2. VERIFICANDO OUTRAS ESCOLAS COM DISTÂNCIAS SUSPEITAS:")
    escolas_suspeitas = []

    for escola in escolas_data:
        if 'lat' in escola and 'lng' in escola and 'de_lat' in escola and 'de_lng' in escola:
            distancia_calculada = haversine_distance(
                escola['lat'], escola['lng'],
                escola['de_lat'], escola['de_lng']
            )

            diferenca = abs(escola['distance'] - distancia_calculada)
            if diferenca > 10:  # Mais de 10 km de diferença
                escolas_suspeitas.append({
                    'name': escola['name'],
                    'distance_atual': escola['distance'],
                    'distance_calculada': distancia_calculada,
                    'diferenca': diferenca
                })

    if escolas_suspeitas:
        print(
            f"   ⚠️  Encontradas {len(escolas_suspeitas)} escolas com distâncias suspeitas:")
        for escola in escolas_suspeitas:
            print(
                f"   - {escola['name']}: {escola['distance_atual']:.2f} km → {escola['distance_calculada']:.2f} km (diff: {escola['diferenca']:.2f} km)")

        # Corrigir todas as escolas suspeitas
        corrigidas = 0
        for i, escola in enumerate(escolas_data):
            for suspeita in escolas_suspeitas:
                if escola.get('name') == suspeita['name']:
                    escolas_data[i]['distance'] = round(
                        suspeita['distance_calculada'], 2)
                    corrigidas += 1

        print(f"   ✅ {corrigidas} escolas com distâncias corrigidas")
    else:
        print(f"   ✅ Nenhuma outra escola com distância suspeita encontrada")

    # 4. Salvar dados corrigidos
    print(f"\n3. SALVANDO DADOS CORRIGIDOS:")
    with open('dados_escolas_atualizados.json', 'w', encoding='utf-8') as f:
        json.dump(escolas_data, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Arquivo 'dados_escolas_atualizados.json' atualizado")

    # 5. Atualizar dashboard HTML
    print(f"\n4. ATUALIZANDO DASHBOARD:")

    try:
        with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Encontrar e substituir os dados das escolas no JavaScript
        start_marker = 'const schoolsData = ['
        end_marker = '];'

        start_pos = html_content.find(start_marker)
        if start_pos != -1:
            end_pos = html_content.find(
                end_marker, start_pos) + len(end_marker)

            # Criar novo JavaScript com dados corrigidos
            js_schools = [start_marker]
            for escola in escolas_data:
                js_line = f"""        {{
          name: "{escola['name']}",
          type: "{escola.get('type', 'N/A')}",
          city: "{escola.get('city', 'N/A')}",
          diretoria: "{escola.get('diretoria', 'N/A')}",
          distance: {escola.get('distance', 0)},
          lat: {escola.get('lat', 0)},
          lng: {escola.get('lng', 0)},
          de_lat: {escola.get('de_lat', 0)},
          de_lng: {escola.get('de_lng', 0)}
        }},"""
                js_schools.append(js_line)

            # Remover vírgula da última entrada
            if js_schools[-1].endswith(','):
                js_schools[-1] = js_schools[-1][:-1]

            js_schools.append('      ' + end_marker)

            new_schools_js = '\n'.join(js_schools)

            # Substituir no HTML
            new_html = html_content[:start_pos] + \
                new_schools_js + html_content[end_pos:]

            with open('distancias_escolas.html', 'w', encoding='utf-8') as f:
                f.write(new_html)

            print(f"   ✅ Dashboard HTML atualizado")
        else:
            print(f"   ❌ Não foi possível encontrar os dados das escolas no HTML")

    except Exception as e:
        print(f"   ❌ Erro ao atualizar HTML: {e}")

    # 6. Relatório final
    print(f"\n5. RELATÓRIO FINAL:")
    kopenoti_final = next(
        (e for e in escolas_data if e.get('name') == 'ALDEIA KOPENOTI'), None)
    if kopenoti_final:
        print(f"   ✅ ALDEIA KOPENOTI corrigida:")
        print(f"      - Distância: {kopenoti_final['distance']} km")
        print(f"      - Localização: {kopenoti_final['city']}")
        print(f"      - Diretoria: {kopenoti_final['diretoria']}")
        print(
            f"      - Coordenadas: {kopenoti_final['lat']}, {kopenoti_final['lng']}")

    if escolas_suspeitas:
        print(
            f"   ✅ {len(escolas_suspeitas)} escolas com distâncias incorretas foram corrigidas")

    print(f"\n✅ CORREÇÃO CONCLUÍDA!")
    print(f"   A escola ALDEIA KOPENOTI agora mostra a distância correta de ~27 km")
    print(f"   em vez dos incorretos 286 km anteriores.")


if __name__ == "__main__":
    main()
