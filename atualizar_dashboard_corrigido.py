#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar o dashboard HTML com dados atualizados - VERSÃO CORRIGIDA
"""

import json
import re


def atualizar_dashboard_html_corrigido():
    """Atualiza o dashboard HTML com dados mais recentes - versão corrigida"""

    print("🔄 ATUALIZANDO DASHBOARD HTML (VERSÃO CORRIGIDA)...")

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
    print("📝 Atualizando dados de veículos...")

    # Construir novo objeto vehicleData com TODAS as diretorias
    veiculos_js = "const vehicleData = {\n"
    for key, value in veiculos_dados.items():
        veiculos_js += f'      "{key}": {{"total": {value["total"]}, "s1": {value["s1"]}, "s2": {value["s2"]}, "s2_4x4": {value["s2_4x4"]}}},\n'
    veiculos_js += "    };"

    # Usar regex mais robusto para substituir o bloco inteiro de vehicleData
    pattern = r"const vehicleData = \{[^}]*(?:\{[^}]*\}[^}]*)*\};"
    new_content = re.sub(pattern, veiculos_js, html_content, flags=re.DOTALL)

    # Se não encontrou, tentar padrão alternativo
    if new_content == html_content:
        print("⚠️  Primeira tentativa falhou, tentando padrão alternativo...")
        pattern2 = r"const vehicleData = \{[\s\S]*?\};"
        new_content = re.sub(pattern2, veiculos_js, html_content)

    if new_content == html_content:
        print("❌ Regex não encontrou o padrão. Vou fazer substituição manual...")
        # Encontrar posição do início e fim do vehicleData
        start_marker = "const vehicleData = {"
        end_marker = "};"

        start_pos = html_content.find(start_marker)
        if start_pos != -1:
            # Encontrar o final do objeto (pode ter objetos aninhados)
            temp_pos = start_pos + len(start_marker)
            brace_count = 1
            end_pos = temp_pos

            while brace_count > 0 and end_pos < len(html_content):
                if html_content[end_pos] == '{':
                    brace_count += 1
                elif html_content[end_pos] == '}':
                    brace_count -= 1
                end_pos += 1

            if brace_count == 0:
                # Encontrou o final, substituir
                before = html_content[:start_pos]
                after = html_content[end_pos:]
                new_content = before + veiculos_js + after
                print("✅ Substituição manual bem-sucedida!")
            else:
                print("❌ Não conseguiu encontrar o final do objeto vehicleData")
        else:
            print("❌ Não encontrou o início do vehicleData")

    html_content = new_content

    # 2. Atualizar estatísticas no HTML
    print("📊 Atualizando estatísticas...")

    # Atualizar número total de veículos
    html_content = re.sub(
        r'<div class="stat-number" id="total-vehicles">\d+</div>',
        f'<div class="stat-number" id="total-vehicles">{stats["total_veiculos"]}</div>',
        html_content,
    )

    # Atualizar número de escolas
    html_content = re.sub(
        r'<div class="stat-number" id="total-schools">\d+</div>',
        f'<div class="stat-number" id="total-schools">{stats["total_escolas"]}</div>',
        html_content,
    )

    # Atualizar escolas de alta prioridade
    html_content = re.sub(
        r'<div class="stat-number" id="high-priority">\d+</div>',
        f'<div class="stat-number" id="high-priority">{stats["escolas_alta_prioridade"]}</div>',
        html_content,
    )

    # 3. Corrigir cor das diretorias para roxo (diferenciar das escolas indígenas)
    html_content = html_content.replace(
        ".diretoria-marker { background-color: #3498db; }",
        # Roxo em vez de azul
        ".diretoria-marker { background-color: #9c27b0; }",
    )

    # 4. Atualizar contadores na legenda
    print("🎨 Atualizando legenda...")

    # Contar escolas por tipo
    escolas_indigenas = sum(
        1 for e in escolas_dados if e.get("type") == "indigena")
    escolas_quilombolas = sum(
        1 for e in escolas_dados if e.get("type") == "quilombola")
    diretorias_com_veiculos = sum(
        1 for v in veiculos_dados.values() if v["total"] > 0)

    # Atualizar texto da legenda
    html_content = re.sub(
        r'<span>Escola Indígena \(\d+ escolas\)</span>',
        f'<span>Escola Indígena ({escolas_indigenas} escolas)</span>',
        html_content
    )

    html_content = re.sub(
        r'<span>Escola Quilombola/Assentamento \(\d+ escolas\)</span>',
        f'<span>Escola Quilombola/Assentamento ({escolas_quilombolas} escolas)</span>',
        html_content
    )

    html_content = re.sub(
        r'<span>Diretoria de Ensino \(🚗 \d+ com veículos\)</span>',
        f'<span>Diretoria de Ensino (🚗 {diretorias_com_veiculos} com veículos)</span>',
        html_content
    )

    # 5. Salvar arquivo atualizado
    print("💾 Salvando arquivo atualizado...")
    with open("distancias_escolas.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ Dashboard HTML atualizado com sucesso!")
    print(f"   📊 {stats['total_escolas']} escolas")
    print(f"   🚗 {stats['total_veiculos']} veículos")
    print(f"   📍 {diretorias_com_veiculos} diretorias com veículos")
    print(f"   🔴 {escolas_indigenas} escolas indígenas")
    print(f"   🟢 {escolas_quilombolas} escolas quilombolas/assentamentos")

    return True


if __name__ == "__main__":
    atualizar_dashboard_html_corrigido()
