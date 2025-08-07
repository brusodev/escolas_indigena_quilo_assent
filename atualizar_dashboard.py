#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar o dashboard HTML com dados atualizados
"""

import json
import re


def atualizar_dashboard_html():
    """Atualiza o dashboard HTML com dados mais recentes"""

    print("🔄 ATUALIZANDO DASHBOARD HTML...")

    # Carregar dados atualizados
    with open("dados_veiculos_atualizados.json", "r", encoding="utf-8") as f:
        veiculos_dados = json.load(f)

    with open("dados_escolas_atualizados.json", "r", encoding="utf-8") as f:
        escolas_dados = json.load(f)

    with open("estatisticas_atualizadas.json", "r", encoding="utf-8") as f:
        stats = json.load(f)

    # Ler arquivo HTML atual
    with open("distancias_escolas.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # 1. Atualizar dados de veículos no JavaScript
    veiculos_js = "const vehicleData = {\n"
    for key, value in veiculos_dados.items():
        veiculos_js += f'      "{key}": {{"total": {value["total"]}, "s1": {value["s1"]}, "s2": {value["s2"]}, "s2_4x4": {value["s2_4x4"]}}},\n'
    veiculos_js += "    };"

    # Substituir dados de veículos
    pattern = r"const vehicleData = \{[^}]+\};"
    html_content = re.sub(pattern, veiculos_js, html_content, flags=re.DOTALL)

    # 2. Atualizar dados de escolas no JavaScript
    escolas_js = "const schoolsData = [\n"
    for escola in escolas_dados:
        # Converter coordenadas string com vírgula para float
        def converter_coord(coord):
            if isinstance(coord, str):
                return float(coord.replace(",", "."))
            return float(coord) if coord else 0

        lat = converter_coord(escola["lat"])
        lng = converter_coord(escola["lng"])

        escolas_js += "      {\n"
        escolas_js += f'        "name": "{escola["name"]}",\n'
        escolas_js += f'        "type": "{escola["type"]}",\n'
        escolas_js += f'        "city": "{escola["city"]}",\n'
        escolas_js += f'        "diretoria": "{escola["diretoria"]}",\n'
        escolas_js += f'        "distance": {escola["distance"]},\n'
        escolas_js += f'        "lat": {lat},\n'
        escolas_js += f'        "lng": {lng},\n'
        escolas_js += f'        "de_lat": {escola["de_lat"]},\n'
        escolas_js += f'        "de_lng": {escola["de_lng"]}\n'
        escolas_js += "      },\n"
    escolas_js += "    ];"

    # Substituir dados de escolas (mais complexo porque é um array grande)
    pattern_inicio = r"const schoolsData = \["
    pattern_fim = r"\];"

    # Encontrar posição de início e fim dos dados de escolas
    inicio = html_content.find("const schoolsData = [")
    if inicio != -1:
        # Encontrar o final do array
        bracket_count = 0
        pos = inicio + len("const schoolsData = [")
        while pos < len(html_content):
            if html_content[pos] == "[":
                bracket_count += 1
            elif html_content[pos] == "]":
                if bracket_count == 0:
                    fim = pos + 1
                    break
                bracket_count -= 1
            pos += 1

        # Substituir a seção completa
        html_content = html_content[:inicio] + escolas_js + html_content[fim:]

    # 3. Atualizar estatísticas no HTML
    html_content = re.sub(
        r'<div class="stat-number" id="total-schools">\d+</div>',
        f'<div class="stat-number" id="total-schools">{stats["total_escolas"]}</div>',
        html_content,
    )

    html_content = re.sub(
        r'<div class="stat-number" id="total-vehicles">\d+</div>',
        f'<div class="stat-number" id="total-vehicles">{stats["total_veiculos"]}</div>',
        html_content,
    )

    # 4. Corrigir cor das diretorias para diferenciar das escolas indígenas
    html_content = html_content.replace(
        ".diretoria-marker { background-color: #3f51b5; }",
        ".diretoria-marker { background-color: #9c27b0; }",  # Roxo em vez de azul
    )

    # 5. Adicionar dados de supervisão como comentário para futuro uso
    supervisao_comment = "\n    // Dados de supervisão GEP disponíveis em dados_supervisao_atualizados.json\n"
    html_content = html_content.replace(
        "    // Dados dos veículos por diretoria",
        supervisao_comment + "    // Dados dos veículos por diretoria",
    )

    # Salvar arquivo atualizado
    with open("distancias_escolas.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ Dashboard HTML atualizado com sucesso!")
    print(f"   📊 {stats['total_escolas']} escolas")
    print(f"   🚗 {stats['total_veiculos']} veículos")
    print(f"   🎨 Cor das diretorias corrigida (roxo)")
    print(f"   📍 {stats['diretorias_com_veiculos']} diretorias com veículos")

    return True


if __name__ == "__main__":
    atualizar_dashboard_html()
