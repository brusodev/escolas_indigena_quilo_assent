#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import json
import re


def main():
    print("=== CORRIGINDO DASHBOARD - REMOVENDO DUPLICATAS ===\n")

    # 1. Ler dados corretos da planilha
    print("1. LENDO DADOS DA PLANILHA:")
    df = pd.read_excel('QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx')

    # Corrigir nome da coluna (tem espaço extra)
    df.columns = ['DIRETORIA', 'QUANTIDADE S-1',
                  'QUANTIDADE S-2', 'QUANTIDADE S-2 4X4']

    print(f"   Total de diretorias: {len(df)}")

    # 2. Criar dados limpos para o dashboard
    print("\n2. CRIANDO DADOS LIMPOS:")
    vehicle_data_clean = {}

    for idx, row in df.iterrows():
        diretoria = row['DIRETORIA'].strip()
        s1 = int(row['QUANTIDADE S-1'])
        s2 = int(row['QUANTIDADE S-2'])
        s2_4x4 = int(row['QUANTIDADE S-2 4X4'])
        total = s1 + s2 + s2_4x4

        vehicle_data_clean[diretoria] = {
            "total": total,
            "s1": s1,
            "s2": s2,
            "s2_4x4": s2_4x4
        }

    print(f"   Dados criados para {len(vehicle_data_clean)} diretorias")

    # Verificar São Vicente especificamente
    if 'SÃO VICENTE' in vehicle_data_clean:
        sao_vicente_data = vehicle_data_clean['SÃO VICENTE']
        print(
            f"   ✓ São Vicente: S-1={sao_vicente_data['s1']}, S-2={sao_vicente_data['s2']}, S-2 4X4={sao_vicente_data['s2_4x4']}, Total={sao_vicente_data['total']}")

    # 3. Atualizar dashboard HTML
    print("\n3. ATUALIZANDO DASHBOARD:")
    try:
        with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Criar novo vehicleData JavaScript
        js_lines = ['        const vehicleData = {']

        for diretoria, dados in sorted(vehicle_data_clean.items()):
            js_line = f'            "{diretoria}": {{"total": {dados["total"]}, "s1": {dados["s1"]}, "s2": {dados["s2"]}, "s2_4x4": {dados["s2_4x4"]}}},'
            js_lines.append(js_line)

        # Remover vírgula da última linha
        if js_lines[-1].endswith(','):
            js_lines[-1] = js_lines[-1][:-1]

        js_lines.append('        };')

        new_vehicle_data = '\n'.join(js_lines)

        # Substituir no HTML
        start_pattern = r'const vehicleData = \{'
        end_pattern = r'\};'

        start_match = re.search(start_pattern, html_content)
        if start_match:
            # Encontrar o final do objeto
            brace_count = 0
            start_pos = start_match.start()
            current_pos = start_pos

            while current_pos < len(html_content):
                char = html_content[current_pos]
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = current_pos + 1
                        break
                current_pos += 1

            # Substituir
            new_html = html_content[:start_pos] + \
                new_vehicle_data + html_content[end_pos:]

            # Salvar
            with open('distancias_escolas.html', 'w', encoding='utf-8') as f:
                f.write(new_html)

            print("   ✅ Dashboard atualizado com dados limpos")

            # Verificar resultado
            with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
                new_content = f.read()

            new_start = new_content.find('const vehicleData = {')
            if new_start != -1:
                new_end = new_content.find('};', new_start) + 2
                new_vehicle_section = new_content[new_start:new_end]

                # Contar entradas
                entry_count = new_vehicle_section.count('":')
                print(
                    f"   ✅ Verificação: {entry_count} entradas no vehicleData (deveria ser 91)")

                # Verificar São Vicente
                if 'SÃO VICENTE' in new_vehicle_section:
                    print("   ✅ São Vicente encontrado no dashboard atualizado")
                else:
                    print("   ❌ São Vicente não encontrado no dashboard")

    except Exception as e:
        print(f"   ❌ Erro ao atualizar dashboard: {e}")

    # 4. Atualizar arquivo JSON também
    print("\n4. ATUALIZANDO ARQUIVO JSON:")
    try:
        json_data = {}
        for diretoria, dados in vehicle_data_clean.items():
            json_data[diretoria] = {
                **dados,
                'diretoria_original': diretoria
            }

        with open('dados_veiculos_atualizados.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        print(f"   ✅ JSON atualizado com {len(json_data)} diretorias")

    except Exception as e:
        print(f"   ❌ Erro ao atualizar JSON: {e}")

    # 5. Relatório final
    print(f"\n5. RELATÓRIO FINAL:")
    total_s1 = sum(dados['s1'] for dados in vehicle_data_clean.values())
    total_s2 = sum(dados['s2'] for dados in vehicle_data_clean.values())
    total_s2_4x4 = sum(dados['s2_4x4']
                       for dados in vehicle_data_clean.values())
    total_geral = total_s1 + total_s2 + total_s2_4x4

    print(f"   📊 TOTAIS:")
    print(f"   - Diretorias: {len(vehicle_data_clean)}")
    print(f"   - S-1: {total_s1}")
    print(f"   - S-2: {total_s2}")
    print(f"   - S-2 4X4: {total_s2_4x4}")
    print(f"   - TOTAL VEÍCULOS: {total_geral}")

    # Verificar São Vicente especificamente
    if 'SÃO VICENTE' in vehicle_data_clean:
        sv_data = vehicle_data_clean['SÃO VICENTE']
        print(f"\n   ⭐ SÃO VICENTE:")
        print(f"   - S-1: {sv_data['s1']}")
        print(f"   - S-2: {sv_data['s2']}")
        print(f"   - S-2 4X4: {sv_data['s2_4x4']}")
        print(f"   - TOTAL: {sv_data['total']}")


if __name__ == "__main__":
    main()
