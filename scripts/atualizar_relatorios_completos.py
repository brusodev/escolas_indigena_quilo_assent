#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualizar relatórios Excel e PDF com dados mais recentes
"""

import pandas as pd
import json
import os
import subprocess
from datetime import datetime


def verificar_dados_atualizados():
    """Verifica se os dados estão atualizados com Haversine"""
    print("🔍 VERIFICANDO DADOS PARA RELATÓRIOS")
    print("=" * 60)

    # Verificar arquivo Excel principal (agora com 63 escolas)
    excel_file = "dados/excel/distancias_escolas_diretorias_completo_63_corrigido.xlsx"
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        print(f"✅ Arquivo Excel: {excel_file}")
        print(f"📊 Total de escolas: {len(df)} (esperado: 63)")

        # Verificar KOPENOTI
        kopenoti = df[df["Nome_Escola"].str.contains("KOPENOTI", na=False, case=False)]
        if not kopenoti.empty:
            distancia = kopenoti.iloc[0]["Distancia_KM"]
            print(f"🎯 KOPENOTI: {distancia:.2f} km")

            if abs(distancia - 27.16) < 0.1:
                print("✅ Dados com Haversine corretos")
                return True
            else:
                print("❌ Dados ainda incorretos")
                return False
        else:
            print("❌ KOPENOTI não encontrado")
            return False
    else:
        print(f"❌ Arquivo não encontrado: {excel_file}")
        return False


def verificar_dados_veiculos():
    """Verifica dados de veículos atualizados"""
    print("\n🚗 VERIFICANDO DADOS DE VEÍCULOS")
    print("-" * 40)

    json_file = "dados/json/dados_veiculos_diretorias.json"
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"✅ Arquivo JSON: {json_file}")

        if "metadata" in data:
            metadata = data["metadata"]
            total_veiculos = metadata.get("total_veiculos", 0)
            print(f"🚗 Total de veículos: {total_veiculos}")

            if total_veiculos == 172:
                print("✅ Dados de veículos corretos")
                return True
            else:
                print("❌ Total de veículos incorreto")
                return False
        else:
            print("❌ Metadata não encontrada")
            return False
    else:
        print(f"❌ Arquivo não encontrado: {json_file}")
        return False


def gerar_relatorio_excel_atualizado():
    """Gera relatório Excel com dados atualizados"""
    print("\n📊 GERANDO RELATÓRIO EXCEL ATUALIZADO")
    print("-" * 50)

    try:
        # Executar script de Excel
        result = subprocess.run(
            ["python", "scripts/geracao/gerar_relatorio_excel.py"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if result.returncode == 0:
            print("✅ Relatório Excel gerado com sucesso")
            print(
                "📄 Output:", result.stdout.strip() if result.stdout else "Sem output"
            )
            return True
        else:
            print("❌ Erro ao gerar relatório Excel")
            print("🔥 Erro:", result.stderr)
            return False

    except Exception as e:
        print(f"❌ Exceção ao gerar Excel: {e}")
        return False


def gerar_relatorio_pdf_atualizado():
    """Gera relatório PDF com dados atualizados"""
    print("\n📄 GERANDO RELATÓRIO PDF ATUALIZADO")
    print("-" * 50)

    try:
        # Executar script de PDF melhorado
        result = subprocess.run(
            ["python", "scripts/geracao/gerar_relatorio_pdf_melhorado.py"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if result.returncode == 0:
            print("✅ Relatório PDF melhorado gerado com sucesso")
            print(
                "📄 Output:", result.stdout.strip() if result.stdout else "Sem output"
            )
            return True
        else:
            print("❌ Erro ao gerar relatório PDF")
            print("🔥 Erro:", result.stderr)
            return False

    except Exception as e:
        print(f"❌ Exceção ao gerar PDF: {e}")
        return False


def main():
    """Função principal"""
    print("🚀 ATUALIZANDO RELATÓRIOS COM DADOS HAVERSINE")
    print("=" * 70)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

    # Verificar dados
    dados_ok = verificar_dados_atualizados()
    veiculos_ok = verificar_dados_veiculos()

    if not dados_ok:
        print("\n❌ ERRO: Dados de escolas não estão atualizados")
        print("💡 Execute primeiro o script de correção de distâncias")
        return False

    if not veiculos_ok:
        print("\n⚠️  AVISO: Dados de veículos podem estar desatualizados")
        print("💡 Continuando com os dados disponíveis...")

    print("\n🔄 INICIANDO GERAÇÃO DE RELATÓRIOS...")
    print("=" * 70)

    # Gerar relatórios
    excel_ok = gerar_relatorio_excel_atualizado()
    pdf_ok = gerar_relatorio_pdf_atualizado()

    # Resumo final
    print("\n🎯 RESUMO FINAL")
    print("=" * 70)

    if excel_ok and pdf_ok:
        print("✅ Todos os relatórios gerados com sucesso!")
        print("📊 Excel: Dados Haversine atualizados")
        print("📄 PDF: Distâncias corrigidas (KOPENOTI: 27.16 km)")
        print("🚀 Relatórios prontos para uso!")
        return True
    else:
        print("❌ Alguns relatórios falharam:")
        print(f"📊 Excel: {'✅ OK' if excel_ok else '❌ FALHOU'}")
        print(f"📄 PDF: {'✅ OK' if pdf_ok else '❌ FALHOU'}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
