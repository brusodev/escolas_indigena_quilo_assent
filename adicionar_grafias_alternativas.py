#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar entradas com múltiplas grafias no dashboard
"""

import json
import re


def adicionar_grafias_alternativas():
    """Adiciona entradas com múltiplas grafias no dashboard"""
    print("🔧 ADICIONANDO GRAFIAS ALTERNATIVAS NO DASHBOARD...")

    # Ler o HTML atual
    with open("distancias_escolas.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Mapeamentos de grafias alternativas
    mapeamentos = {
        "ITARARE": "ITARARÉ",
        "REGISTRO ": "REGISTRO",  # Pode ter espaço extra
        "SANTOS ": "SANTOS",
        "SAO VICENTE ": "SÃO VICENTE",
        "SAO BERNARDO DO CAMPO": "SÃO BERNARDO DO CAMPO",
        "SANTO ANASTACIO": "SANTO ANASTÁCIO",
        "PENAPOLIS": "PENÁPOLIS",
        "TUPA": "TUPÃ"
    }

    # Encontrar a seção vehicleData
    start_marker = "const vehicleData = {"
    end_marker = "};"

    start_pos = html_content.find(start_marker)
    if start_pos == -1:
        print("❌ Não encontrou vehicleData")
        return False

    # Encontrar o final do objeto
    temp_pos = start_pos + len(start_marker)
    brace_count = 1
    end_pos = temp_pos

    while brace_count > 0 and end_pos < len(html_content):
        if html_content[end_pos] == '{':
            brace_count += 1
        elif html_content[end_pos] == '}':
            brace_count -= 1
        end_pos += 1

    if brace_count != 0:
        print("❌ Não conseguiu encontrar o final do vehicleData")
        return False

    # Extrair o conteúdo atual do vehicleData
    vehicle_data_str = html_content[start_pos:end_pos]

    # Adicionar entradas alternativas antes do fechamento
    entradas_extras = []

    for grafia_sem_acento, grafia_com_acento in mapeamentos.items():
        # Procurar se já existe a grafia com acento
        if f'"{grafia_com_acento}":' in vehicle_data_str:
            # Extrair os dados da grafia com acento
            pattern = rf'"{re.escape(grafia_com_acento)}":\s*(\{{[^}}]+\}})'
            match = re.search(pattern, vehicle_data_str)
            if match:
                dados = match.group(1)
                entrada_extra = f'      "{grafia_sem_acento}": {dados},'
                entradas_extras.append(entrada_extra)
                print(
                    f"   ✅ Adicionando {grafia_sem_acento} → {grafia_com_acento}")

    if entradas_extras:
        # Inserir as entradas extras antes do fechamento
        pos_fechar = vehicle_data_str.rfind("}")
        if pos_fechar != -1:
            # Inserir as novas entradas
            novas_entradas = "\n" + "\n".join(entradas_extras) + "\n    "
            novo_vehicle_data = vehicle_data_str[:pos_fechar] + \
                novas_entradas + vehicle_data_str[pos_fechar:]

            # Substituir no HTML
            novo_html = html_content[:start_pos] + \
                novo_vehicle_data + html_content[end_pos:]

            # Salvar
            with open("distancias_escolas.html", "w", encoding="utf-8") as f:
                f.write(novo_html)

            print(
                f"   ✅ {len(entradas_extras)} entradas alternativas adicionadas")
            return True

    print("   ⚠️  Nenhuma entrada alternativa necessária")
    return True


if __name__ == "__main__":
    if adicionar_grafias_alternativas():
        print("✅ Grafias alternativas adicionadas com sucesso!")
    else:
        print("❌ Erro ao adicionar grafias alternativas")
