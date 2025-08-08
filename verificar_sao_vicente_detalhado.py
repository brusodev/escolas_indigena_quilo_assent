#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import json
import unicodedata
import re


def normalizar_nome(nome):
    """Normaliza nomes removendo acentos e convertendo para maiúsculas"""
    if not isinstance(nome, str):
        return str(nome).upper()

    # Remove acentos
    nome_normalizado = unicodedata.normalize('NFKD', nome)
    nome_normalizado = ''.join(
        [c for c in nome_normalizado if not unicodedata.combining(c)])

    return nome_normalizado.upper().strip()


def criar_variantes_nome(nome):
    """Cria variantes do nome para comparação"""
    variantes = []

    # Original
    variantes.append(nome)

    # Sem acentos
    nome_sem_acentos = normalizar_nome(nome)
    variantes.append(nome_sem_acentos)

    # Variações específicas para São Vicente
    if 'SAO VICENTE' in nome.upper() or 'SÃO VICENTE' in nome.upper():
        variantes.extend([
            'SAO VICENTE',
            'SÃO VICENTE',
            'VICENTE',
            'S VICENTE',
            'S. VICENTE'
        ])

    return list(set(variantes))


def main():
    print("=== VERIFICAÇÃO DETALHADA DE SÃO VICENTE ===\n")

    # 1. Verificar planilha Excel
    print("1. DADOS DA PLANILHA EXCEL:")
    try:
        df = pd.read_excel('QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx')
        print(f"   Total de diretorias na planilha: {len(df)}")

        # Procurar São Vicente na planilha
        sao_vicente_rows = df[df['DIRETORIA'].str.contains(
            'VICENTE', case=False, na=False)]
        print(f"\n   Entradas contendo 'VICENTE':")
        for idx, row in sao_vicente_rows.iterrows():
            print(
                f"   - {row['DIRETORIA']}: S-1={row['QUANTIDADE S-1']}, S-2={row['QUANTIDADE S-2']}, S-2 4X4={row['QUANTIDADE S-2 4X4']}")

        # Verificar a linha exata de SÃO VICENTE
        sao_vicente_exato = df[df['DIRETORIA'].str.upper(
        ).str.strip() == 'SÃO VICENTE']
        if not sao_vicente_exato.empty:
            row = sao_vicente_exato.iloc[0]
            print(f"\n   ✓ SÃO VICENTE encontrado na planilha:")
            print(f"     S-1: {row['QUANTIDADE S-1']}")
            print(f"     S-2: {row['QUANTIDADE S-2']}")
            print(f"     S-2 4X4: {row['QUANTIDADE S-2 4X4']}")
        else:
            print("\n   ❌ SÃO VICENTE não encontrado na planilha (busca exata)")

    except Exception as e:
        print(f"   ❌ Erro ao ler planilha: {e}")

    # 2. Verificar dados JSON
    print("\n2. DADOS DO ARQUIVO JSON:")
    try:
        with open('dados_veiculos_atualizados.json', 'r', encoding='utf-8') as f:
            dados_json = json.load(f)

        print(f"   Total de diretorias no JSON: {len(dados_json)}")

        # Procurar São Vicente no JSON
        sao_vicente_json = None
        variantes_encontradas = []

        for diretoria, dados in dados_json.items():
            variantes = criar_variantes_nome(diretoria)
            for variante in variantes:
                if 'VICENTE' in variante.upper():
                    variantes_encontradas.append((diretoria, dados))
                    if 'SAO VICENTE' in variante.upper() or 'SÃO VICENTE' in variante.upper():
                        sao_vicente_json = (diretoria, dados)

        if variantes_encontradas:
            print(f"\n   Entradas contendo 'VICENTE' no JSON:")
            for diretoria, dados in variantes_encontradas:
                print(
                    f"   - '{diretoria}': total={dados['total']}, s1={dados['s1']}, s2={dados['s2']}, s2_4x4={dados['s2_4x4']}")

        if sao_vicente_json:
            diretoria, dados = sao_vicente_json
            print(f"\n   ✓ São Vicente encontrado no JSON como '{diretoria}':")
            print(f"     Total: {dados['total']}")
            print(f"     S-1: {dados['s1']}")
            print(f"     S-2: {dados['s2']}")
            print(f"     S-2 4X4: {dados['s2_4x4']}")
        else:
            print("\n   ❌ São Vicente não encontrado no JSON")

    except Exception as e:
        print(f"   ❌ Erro ao ler JSON: {e}")

    # 3. Verificar dashboard HTML
    print("\n3. DADOS NO DASHBOARD HTML:")
    try:
        with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Procurar São Vicente no JavaScript do dashboard
        if 'vehicleData' in html_content:
            # Extrair a parte do vehicleData
            start = html_content.find('const vehicleData = {')
            if start != -1:
                end = html_content.find('};', start) + 2
                vehicle_data_js = html_content[start:end]

                # Procurar por São Vicente
                if 'VICENTE' in vehicle_data_js.upper():
                    print("   ✓ Referências a 'VICENTE' encontradas no vehicleData:")
                    lines = vehicle_data_js.split('\n')
                    for i, line in enumerate(lines):
                        if 'VICENTE' in line.upper():
                            print(f"     Linha {i}: {line.strip()}")
                else:
                    print(
                        "   ❌ Nenhuma referência a 'VICENTE' encontrada no vehicleData")
            else:
                print("   ❌ vehicleData não encontrado no HTML")
        else:
            print("   ❌ vehicleData não encontrado no HTML")

    except Exception as e:
        print(f"   ❌ Erro ao ler HTML: {e}")

    # 4. Criar relatório completo de todas as diretorias
    print("\n4. RELATÓRIO COMPLETO DE VEÍCULOS POR DIRETORIA:")
    try:
        df = pd.read_excel('QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx')

        total_s1 = df['QUANTIDADE S-1'].sum()
        total_s2 = df['QUANTIDADE S-2'].sum()
        total_s2_4x4 = df['QUANTIDADE S-2 4X4'].sum()
        total_geral = total_s1 + total_s2 + total_s2_4x4

        print(f"\n   TOTAIS GERAIS:")
        print(f"   - S-1: {total_s1}")
        print(f"   - S-2: {total_s2}")
        print(f"   - S-2 4X4: {total_s2_4x4}")
        print(f"   - TOTAL: {total_geral}")

        print(f"\n   DETALHAMENTO POR DIRETORIA ({len(df)} diretorias):")
        for idx, row in df.iterrows():
            diretoria = row['DIRETORIA']
            s1 = row['QUANTIDADE S-1']
            s2 = row['QUANTIDADE S-2']
            s2_4x4 = row['QUANTIDADE S-2 4X4']
            total = s1 + s2 + s2_4x4

            # Destacar São Vicente
            if 'VICENTE' in diretoria.upper():
                print(
                    f"   ⭐ {diretoria}: S-1={s1}, S-2={s2}, S-2 4X4={s2_4x4}, TOTAL={total}")
            else:
                print(
                    f"   - {diretoria}: S-1={s1}, S-2={s2}, S-2 4X4={s2_4x4}, TOTAL={total}")

        # Salvar relatório em arquivo
        with open('relatorio_completo_veiculos_diretorias.txt', 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO COMPLETO DE VEÍCULOS POR DIRETORIA\n")
            f.write("=" * 50 + "\n\n")
            f.write(
                f"Data: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write(f"TOTAIS GERAIS:\n")
            f.write(f"- S-1: {total_s1}\n")
            f.write(f"- S-2: {total_s2}\n")
            f.write(f"- S-2 4X4: {total_s2_4x4}\n")
            f.write(f"- TOTAL: {total_geral}\n\n")
            f.write(f"DETALHAMENTO POR DIRETORIA ({len(df)} diretorias):\n")
            f.write("-" * 80 + "\n")

            for idx, row in df.iterrows():
                diretoria = row['DIRETORIA']
                s1 = row['QUANTIDADE S-1']
                s2 = row['QUANTIDADE S-2']
                s2_4x4 = row['QUANTIDADE S-2 4X4']
                total = s1 + s2 + s2_4x4
                f.write(
                    f"{diretoria:<35} | S-1: {s1:>2} | S-2: {s2:>2} | S-2 4X4: {s2_4x4:>2} | TOTAL: {total:>3}\n")

        print(f"\n   ✓ Relatório salvo em 'relatorio_completo_veiculos_diretorias.txt'")

    except Exception as e:
        print(f"   ❌ Erro ao criar relatório: {e}")


if __name__ == "__main__":
    main()
