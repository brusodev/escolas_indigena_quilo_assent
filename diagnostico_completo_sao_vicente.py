#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import json
import unicodedata


def main():
    print("=== DIAGNÓSTICO COMPLETO DE SÃO VICENTE E CONTAGEM DE DIRETORIAS ===\n")

    # 1. Verificar colunas da planilha Excel
    print("1. VERIFICANDO COLUNAS DA PLANILHA:")
    try:
        df = pd.read_excel('QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx')
        print(f"   Colunas encontradas: {list(df.columns)}")
        print(f"   Total de diretorias: {len(df)}")

        # Encontrar São Vicente
        sao_vicente_mask = df['DIRETORIA'].str.contains(
            'VICENTE', case=False, na=False)
        sao_vicente_rows = df[sao_vicente_mask]

        print(f"\n   Entradas contendo 'VICENTE':")
        for idx, row in sao_vicente_rows.iterrows():
            print(f"   - '{row['DIRETORIA']}'")
            for col in df.columns:
                if col != 'DIRETORIA':
                    print(f"     {col}: {row[col]}")

        # Verificar São Vicente especificamente
        sao_vicente_exato = df[df['DIRETORIA'].str.strip(
        ).str.upper() == 'SÃO VICENTE']
        if not sao_vicente_exato.empty:
            row = sao_vicente_exato.iloc[0]
            print(f"\n   ✓ SÃO VICENTE encontrado:")
            for col in df.columns:
                if col != 'DIRETORIA':
                    print(f"     {col}: {row[col]}")

    except Exception as e:
        print(f"   ❌ Erro: {e}")

    # 2. Verificar dados JSON
    print("\n2. VERIFICANDO DADOS JSON:")
    try:
        with open('dados_veiculos_atualizados.json', 'r', encoding='utf-8') as f:
            dados_json = json.load(f)

        print(f"   Total de diretorias no JSON: {len(dados_json)}")

        # Procurar São Vicente
        sao_vicente_encontrado = False
        for diretoria, dados in dados_json.items():
            if 'VICENTE' in diretoria.upper():
                print(f"   ✓ Encontrado: '{diretoria}' = {dados}")
                sao_vicente_encontrado = True

        if not sao_vicente_encontrado:
            print("   ❌ São Vicente não encontrado no JSON")

    except Exception as e:
        print(f"   ❌ Erro: {e}")

    # 3. Verificar contagem no dashboard
    print("\n3. VERIFICANDO CONTAGEM NO DASHBOARD:")
    try:
        with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Extrair vehicleData
        start = html_content.find('const vehicleData = {')
        if start != -1:
            end = html_content.find('};', start) + 2
            vehicle_data_js = html_content[start:end]

            # Contar entradas no vehicleData
            lines = vehicle_data_js.split('\n')
            vehicle_entries = 0
            vicente_entries = 0
            duplicates = []

            for line in lines:
                if '":' in line and '{' in line:
                    vehicle_entries += 1
                    if 'VICENTE' in line.upper():
                        vicente_entries += 1
                        duplicates.append(line.strip())

            print(f"   Total de entradas no vehicleData: {vehicle_entries}")
            print(f"   Entradas contendo 'VICENTE': {vicente_entries}")

            if duplicates:
                print(f"   Entradas de Vicente encontradas:")
                for dup in duplicates:
                    print(f"     {dup}")

            # Verificar se há duplicatas
            if vehicle_entries > 91:
                print(
                    f"\n   ⚠️  PROBLEMA: {vehicle_entries} entradas quando deveria ser 91!")
                print("   Procurando duplicatas...")

                # Extrair chaves
                chaves = []
                for line in lines:
                    if '":' in line and '{' in line:
                        key_start = line.find('"') + 1
                        key_end = line.find('"', key_start)
                        if key_start > 0 and key_end > key_start:
                            chave = line[key_start:key_end]
                            chaves.append(chave)

                # Encontrar duplicatas
                from collections import Counter
                contadores = Counter(chaves)
                duplicatas = {k: v for k, v in contadores.items() if v > 1}

                if duplicatas:
                    print(f"   🔍 Duplicatas encontradas:")
                    for chave, count in duplicatas.items():
                        print(f"     '{chave}': {count} vezes")
                else:
                    print("   Nenhuma duplicata de chave encontrada")

    except Exception as e:
        print(f"   ❌ Erro: {e}")

    # 4. Verificar dados de escolas
    print("\n4. VERIFICANDO DADOS DE ESCOLAS:")
    try:
        with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
            dados_escolas = json.load(f)

        # Contar diretorias únicas nas escolas
        diretorias_escolas = set()
        sao_vicente_escolas = []

        for escola in dados_escolas:
            if 'diretoria' in escola:
                diretorias_escolas.add(escola['diretoria'])
                if 'VICENTE' in escola['diretoria'].upper():
                    sao_vicente_escolas.append(escola['nome'])

        print(f"   Diretorias únicas nas escolas: {len(diretorias_escolas)}")

        if sao_vicente_escolas:
            print(f"   Escolas de São Vicente ({len(sao_vicente_escolas)}):")
            for escola in sao_vicente_escolas:
                print(f"     - {escola}")
        else:
            print("   Nenhuma escola de São Vicente encontrada")

    except Exception as e:
        print(f"   ❌ Erro: {e}")


if __name__ == "__main__":
    main()
