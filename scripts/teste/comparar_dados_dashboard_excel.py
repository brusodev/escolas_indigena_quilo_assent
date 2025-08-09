#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparar dados entre dashboard (63 escolas) e Excel (59 escolas)
Identificar quais escolas estão faltando nos relatórios
"""

import pandas as pd
import re
import json


def extrair_escolas_dashboard():
    """Extrai lista de escolas do dashboard HTML"""
    print("🔍 EXTRAINDO ESCOLAS DO DASHBOARD")
    print("=" * 50)

    try:
        with open("dashboard_integrado.html", "r", encoding="utf-8") as f:
            content = f.read()

        # Buscar o array schoolsData
        match = re.search(r"const schoolsData = \[(.*?)\];", content, re.DOTALL)
        if not match:
            print("❌ Não encontrou schoolsData no dashboard")
            return []

        schools_text = match.group(1)

        # Extrair nomes das escolas usando regex
        name_matches = re.findall(r'"name":\s*"([^"]+)"', schools_text)

        escolas_dashboard = [nome.strip() for nome in name_matches]

        print(f"✅ Encontradas {len(escolas_dashboard)} escolas no dashboard")
        return escolas_dashboard

    except Exception as e:
        print(f"❌ Erro ao extrair escolas do dashboard: {e}")
        return []


def extrair_escolas_excel():
    """Extrai lista de escolas do arquivo Excel"""
    print("\n🔍 EXTRAINDO ESCOLAS DO EXCEL")
    print("=" * 50)

    try:
        df = pd.read_excel("distancias_escolas_diretorias_corrigido.xlsx")
        escolas_excel = df["Nome_Escola"].tolist()

        print(f"✅ Encontradas {len(escolas_excel)} escolas no Excel")
        return escolas_excel

    except Exception as e:
        print(f"❌ Erro ao extrair escolas do Excel: {e}")
        return []


def comparar_escolas(escolas_dashboard, escolas_excel):
    """Compara as listas e identifica diferenças"""
    print("\n🔍 COMPARANDO DADOS")
    print("=" * 50)

    # Converter para sets para comparação
    set_dashboard = set(escola.strip().upper() for escola in escolas_dashboard)
    set_excel = set(escola.strip().upper() for escola in escolas_excel)

    # Escolas que estão no dashboard mas não no Excel
    faltando_excel = set_dashboard - set_excel

    # Escolas que estão no Excel mas não no dashboard
    faltando_dashboard = set_excel - set_dashboard

    print(f"📊 RESULTADOS:")
    print(f"   Dashboard: {len(escolas_dashboard)} escolas")
    print(f"   Excel: {len(escolas_excel)} escolas")
    print(f"   Diferença: {len(escolas_dashboard) - len(escolas_excel)} escolas")

    if faltando_excel:
        print(f"\n🔴 ESCOLAS NO DASHBOARD MAS NÃO NO EXCEL ({len(faltando_excel)}):")
        for i, escola in enumerate(sorted(faltando_excel), 1):
            print(f"   {i}. {escola}")

    if faltando_dashboard:
        print(
            f"\n🟡 ESCOLAS NO EXCEL MAS NÃO NO DASHBOARD ({len(faltando_dashboard)}):"
        )
        for i, escola in enumerate(sorted(faltando_dashboard), 1):
            print(f"   {i}. {escola}")

    if not faltando_excel and not faltando_dashboard:
        print("\n✅ TODOS OS DADOS ESTÃO SINCRONIZADOS!")

    return faltando_excel, faltando_dashboard


def buscar_escolas_originais():
    """Busca no arquivo CSV original para ver se há mais escolas"""
    print("\n🔍 VERIFICANDO ARQUIVO CSV ORIGINAL")
    print("=" * 50)

    try:
        df_csv = pd.read_csv("ENDERECO_ESCOLAS_062025 (1).csv", encoding="utf-8")
        escolas_csv = df_csv["NOME"].tolist() if "NOME" in df_csv.columns else []

        print(f"✅ Arquivo CSV original: {len(escolas_csv)} escolas")

        # Verificar se há escolas no CSV que não estão no Excel
        set_csv = set(
            escola.strip().upper() for escola in escolas_csv if pd.notna(escola)
        )
        set_excel = set()

        try:
            df_excel = pd.read_excel("distancias_escolas_diretorias_corrigido.xlsx")
            set_excel = set(
                escola.strip().upper() for escola in df_excel["Nome_Escola"].tolist()
            )
        except:
            pass

        faltando_no_excel = set_csv - set_excel

        if faltando_no_excel:
            print(
                f"\n🔴 ESCOLAS NO CSV ORIGINAL MAS NÃO NO EXCEL ({len(faltando_no_excel)}):"
            )
            for i, escola in enumerate(sorted(list(faltando_no_excel)[:10]), 1):
                print(f"   {i}. {escola}")
            if len(faltando_no_excel) > 10:
                print(f"   ... e mais {len(faltando_no_excel) - 10} escolas")

        return escolas_csv

    except Exception as e:
        print(f"❌ Erro ao ler CSV original: {e}")
        return []


def verificar_diretorias_completas():
    """Verifica o arquivo completo de diretorias"""
    print("\n🔍 VERIFICANDO ARQUIVO COMPLETO")
    print("=" * 50)

    try:
        df_completo = pd.read_excel("diretorias_ensino_completo.xlsx")
        print(f"✅ Arquivo completo: {len(df_completo)} registros")

        # Verificar colunas
        print(f"📋 Colunas: {list(df_completo.columns)}")

        # Se houver coluna de escola
        if "Nome_Escola" in df_completo.columns:
            escolas_completo = df_completo["Nome_Escola"].dropna().tolist()
            print(f"📊 Escolas únicas: {len(set(escolas_completo))}")

        return df_completo

    except Exception as e:
        print(f"❌ Erro ao ler arquivo completo: {e}")
        return None


def main():
    """Função principal"""
    print("🔍 ANÁLISE COMPARATIVA: DASHBOARD vs EXCEL")
    print("=" * 70)

    # Extrair dados
    escolas_dashboard = extrair_escolas_dashboard()
    escolas_excel = extrair_escolas_excel()

    if not escolas_dashboard or not escolas_excel:
        print("❌ Erro: Não foi possível extrair dados")
        return

    # Comparar
    faltando_excel, faltando_dashboard = comparar_escolas(
        escolas_dashboard, escolas_excel
    )

    # Verificar arquivos originais
    buscar_escolas_originais()
    verificar_diretorias_completas()

    # Salvar resultado
    resultado = {
        "dashboard_total": len(escolas_dashboard),
        "excel_total": len(escolas_excel),
        "diferenca": len(escolas_dashboard) - len(escolas_excel),
        "faltando_no_excel": list(faltando_excel),
        "faltando_no_dashboard": list(faltando_dashboard),
    }

    with open("comparacao_dashboard_excel.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultado salvo em: comparacao_dashboard_excel.json")

    if faltando_excel:
        print(f"\n🎯 PRÓXIMOS PASSOS:")
        print(f"   1. Adicionar {len(faltando_excel)} escolas faltantes ao Excel")
        print(f"   2. Regenerar relatórios Excel e PDF")
        print(f"   3. Verificar se todas as 63 escolas estão incluídas")


if __name__ == "__main__":
    main()
