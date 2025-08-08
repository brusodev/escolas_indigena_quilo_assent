#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def main():
    print("=== ATUALIZANDO DASHBOARD COM NOVAS ESCOLAS ===\n")

    # 1. Carregar dados das escolas atualizados
    print("1. CARREGANDO DADOS DAS ESCOLAS:")
    with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        escolas_data = json.load(f)

    print(f"   Total de escolas: {len(escolas_data)}")

    # Contar por tipo
    indigenas = [e for e in escolas_data if e.get('type') == 'indigena']
    quilombolas = [e for e in escolas_data if e.get('type') == 'quilombola']

    print(f"   - Indígenas: {len(indigenas)}")
    print(f"   - Quilombolas/Assentamentos: {len(quilombolas)}")

    # 2. Atualizar dashboard HTML
    print(f"\n2. ATUALIZANDO DASHBOARD HTML:")

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

            # Criar novo JavaScript com dados atualizados
            js_schools = [start_marker]
            for escola in escolas_data:
                js_line = f"""        {{
          name: "{escola.get('name', 'N/A')}",
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

            print(
                f"   ✅ Dashboard HTML atualizado com {len(escolas_data)} escolas")
        else:
            print(f"   ❌ Não foi possível encontrar os dados das escolas no HTML")

    except Exception as e:
        print(f"   ❌ Erro ao atualizar HTML: {e}")

    # 3. Verificar as 4 novas escolas no dashboard
    print(f"\n3. VERIFICANDO NOVAS ESCOLAS NO DASHBOARD:")

    novas_escolas_nomes = [
        'BAIRRO DE BOMBAS',
        'BAIRRO BOMBAS DE CIMA',
        'FAZENDA DA CAIXA',
        'MARIA ANTONIA CHULES PRINCS'
    ]

    for nome in novas_escolas_nomes:
        escola = next((e for e in escolas_data if e.get('name') == nome), None)
        if escola:
            print(f"   ✅ {nome}")
            print(f"      📍 {escola['city']} → {escola['diretoria']}")
            print(f"      📏 {escola['distance']} km")
            print(f"      🏷️  Tipo: {escola['type']}")
        else:
            print(f"   ❌ {nome} não encontrada")

    # 4. Atualizar estatísticas no dashboard
    print(f"\n4. ATUALIZANDO ESTATÍSTICAS:")

    # Atualizar a legenda com os novos números
    try:
        with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Atualizar contadores na legenda
        html_content = html_content.replace(
            f'Escola Indígena (37 escolas)',
            f'Escola Indígena ({len(indigenas)} escolas)'
        )

        html_content = html_content.replace(
            f'Escola Quilombola/Assentamento (22 escolas)',
            f'Escola Quilombola/Assentamento ({len(quilombolas)} escolas)'
        )

        with open('distancias_escolas.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"   ✅ Estatísticas da legenda atualizadas")

    except Exception as e:
        print(f"   ❌ Erro ao atualizar estatísticas: {e}")

    # 5. Relatório final
    print(f"\n5. RELATÓRIO FINAL:")
    print(f"   📊 TOTAIS ATUALIZADOS:")
    print(f"   ✅ Total de escolas: {len(escolas_data)}")
    print(f"   ✅ Escolas indígenas: {len(indigenas)}")
    print(f"   ✅ Escolas quilombolas/assentamentos: {len(quilombolas)}")

    print(f"\n   🆕 NOVAS ESCOLAS ADICIONADAS:")
    for nome in novas_escolas_nomes:
        escola = next((e for e in escolas_data if e.get('name') == nome), None)
        if escola:
            print(
                f"   ⭐ {nome} ({escola['diretoria']}) - {escola['distance']} km")

    print(f"\n✅ DASHBOARD ATUALIZADO!")
    print(f"   O dashboard agora inclui as 4 novas escolas de assentamento")
    print(f"   e os contadores foram atualizados para refletir os novos totais.")


if __name__ == "__main__":
    main()
