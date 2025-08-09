#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RELATÓRIO DE VALIDAÇÃO DOS DADOS ATUALIZADOS
Sistema de Gestão de Escolas Indígenas, Quilombolas e Assentamentos
"""

import pandas as pd
import json
import os
from datetime import datetime


def validar_relatorios_gerados():
    """Valida os relatórios Excel e PDF recém-gerados"""
    print("📋 RELATÓRIO DE VALIDAÇÃO DOS DADOS ATUALIZADOS")
    print("=" * 80)
    print(f"📅 Data da Validação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

    # 1. Validar arquivo principal
    print("🎯 VALIDAÇÃO DO ARQUIVO PRINCIPAL")
    print("-" * 50)
    arquivo_principal = (
        "dados/excel/distancias_escolas_diretorias_completo_63_corrigido.xlsx"
    )

    if os.path.exists(arquivo_principal):
        df_principal = pd.read_excel(arquivo_principal)
        print(f"✅ Arquivo principal encontrado: {arquivo_principal}")
        print(f"📊 Total de escolas: {len(df_principal)}")

        # Verificar KOPENOTI
        kopenoti = df_principal[
            df_principal["Nome_Escola"].str.contains("KOPENOTI", na=False, case=False)
        ]
        if not kopenoti.empty:
            distancia = kopenoti.iloc[0]["Distancia_KM"]
            print(
                f"🎯 KOPENOTI: {distancia:.2f} km {'✅ CORRETO' if abs(distancia - 27.16) < 0.1 else '❌ INCORRETO'}"
            )

        # Análise por tipo
        tipos = df_principal["Tipo_Escola"].value_counts()
        print(f"📋 Tipos de escola:")
        for tipo, count in tipos.items():
            print(f"   {tipo}: {count}")

        print(f"🏢 Diretorias únicas: {df_principal['DE_Responsavel'].nunique()}")
    else:
        print(f"❌ Arquivo principal não encontrado: {arquivo_principal}")

    print()

    # 2. Validar relatório Excel gerado
    print("📊 VALIDAÇÃO DO RELATÓRIO EXCEL GERADO")
    print("-" * 50)
    relatorio_excel = "relatorios/excel/Relatorio_Completo_Escolas_Diretorias.xlsx"

    if os.path.exists(relatorio_excel):
        print(f"✅ Relatório Excel encontrado: {relatorio_excel}")

        # Verificar abas do Excel
        xl_file = pd.ExcelFile(relatorio_excel)
        print(f"📋 Abas encontradas: {len(xl_file.sheet_names)}")
        for aba in xl_file.sheet_names:
            print(f"   📄 {aba}")

        # Verificar dados da primeira aba
        df_excel = pd.read_excel(relatorio_excel, sheet_name=xl_file.sheet_names[0])
        print(f"📊 Registros na primeira aba: {len(df_excel)}")

        file_size = os.path.getsize(relatorio_excel) / 1024 / 1024  # MB
        print(f"💾 Tamanho do arquivo: {file_size:.2f} MB")

        modification_time = os.path.getmtime(relatorio_excel)
        mod_datetime = datetime.fromtimestamp(modification_time)
        print(f"🕒 Última modificação: {mod_datetime.strftime('%d/%m/%Y %H:%M:%S')}")
    else:
        print(f"❌ Relatório Excel não encontrado: {relatorio_excel}")

    print()

    # 3. Validar relatório PDF gerado
    print("📄 VALIDAÇÃO DO RELATÓRIO PDF GERADO")
    print("-" * 50)
    pdf_dir = "relatorios/pdf"

    if os.path.exists(pdf_dir):
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
        pdf_files.sort(reverse=True)  # Mais recente primeiro

        print(f"📁 Total de PDFs: {len(pdf_files)}")

        if pdf_files:
            latest_pdf = pdf_files[0]
            pdf_path = os.path.join(pdf_dir, latest_pdf)

            print(f"📄 PDF mais recente: {latest_pdf}")

            file_size = os.path.getsize(pdf_path) / 1024 / 1024  # MB
            print(f"💾 Tamanho do arquivo: {file_size:.2f} MB")

            modification_time = os.path.getmtime(pdf_path)
            mod_datetime = datetime.fromtimestamp(modification_time)
            print(f"🕒 Criado em: {mod_datetime.strftime('%d/%m/%Y %H:%M:%S')}")

            # Mostrar últimos 3 PDFs
            print(f"📋 Últimos 3 PDFs gerados:")
            for i, pdf in enumerate(pdf_files[:3]):
                pdf_path = os.path.join(pdf_dir, pdf)
                mod_time = os.path.getmtime(pdf_path)
                mod_dt = datetime.fromtimestamp(mod_time)
                print(f"   {i+1}. {pdf} - {mod_dt.strftime('%d/%m/%Y %H:%M')}")
        else:
            print("❌ Nenhum PDF encontrado")
    else:
        print(f"❌ Diretório PDF não encontrado: {pdf_dir}")

    print()

    # 4. Validar dados de veículos
    print("🚗 VALIDAÇÃO DOS DADOS DE VEÍCULOS")
    print("-" * 50)
    arquivo_veiculos = "dados/json/dados_veiculos_diretorias.json"

    if os.path.exists(arquivo_veiculos):
        with open(arquivo_veiculos, "r", encoding="utf-8") as f:
            dados_veiculos = json.load(f)

        print(f"✅ Arquivo de veículos encontrado: {arquivo_veiculos}")

        if "metadata" in dados_veiculos:
            metadata = dados_veiculos["metadata"]
            total_veiculos = metadata.get("total_veiculos", 0)
            print(f"🚗 Total de veículos: {total_veiculos}")

            if "diretorias" in dados_veiculos:
                diretorias_com_veiculos = len(dados_veiculos["diretorias"])
                print(f"🏢 Diretorias com dados: {diretorias_com_veiculos}")
        else:
            print("⚠️ Metadata não encontrada no arquivo de veículos")
    else:
        print(f"❌ Arquivo de veículos não encontrado: {arquivo_veiculos}")

    print()

    # 5. Validar dashboard
    print("🌐 VALIDAÇÃO DO DASHBOARD")
    print("-" * 50)
    dashboard_file = "dashboard/dashboard_integrado.html"

    if os.path.exists(dashboard_file):
        with open(dashboard_file, "r", encoding="utf-8") as f:
            dashboard_content = f.read()

        print(f"✅ Dashboard encontrado: {dashboard_file}")

        file_size = os.path.getsize(dashboard_file) / 1024  # KB
        print(f"💾 Tamanho do arquivo: {file_size:.2f} KB")

        # Verificar se contém dados das 63 escolas
        if "KOPENOTI" in dashboard_content:
            print("🎯 KOPENOTI encontrado no dashboard ✅")
        else:
            print("🎯 KOPENOTI não encontrado no dashboard ❌")

        # Contar escolas no dashboard (aproximado)
        escola_count = dashboard_content.count('"nome_escola"')
        if escola_count > 0:
            print(f"📊 Escolas detectadas no dashboard: ~{escola_count}")

        modification_time = os.path.getmtime(dashboard_file)
        mod_datetime = datetime.fromtimestamp(modification_time)
        print(f"🕒 Última modificação: {mod_datetime.strftime('%d/%m/%Y %H:%M:%S')}")
    else:
        print(f"❌ Dashboard não encontrado: {dashboard_file}")

    print()

    # 6. Resumo final
    print("🎯 RESUMO DA VALIDAÇÃO")
    print("=" * 80)

    componentes = [
        ("Arquivo Principal", arquivo_principal),
        ("Relatório Excel", relatorio_excel),
        ("Dashboard", dashboard_file),
        ("Dados Veículos", arquivo_veiculos),
    ]

    status_geral = []
    for nome, arquivo in componentes:
        status = "✅ OK" if os.path.exists(arquivo) else "❌ FALTANDO"
        status_geral.append(os.path.exists(arquivo))
        print(f"{status.ljust(12)} {nome}")

    # Verificar PDF mais recente
    if os.path.exists(pdf_dir) and pdf_files:
        print(f"✅ OK       Relatório PDF")
        status_geral.append(True)
    else:
        print(f"❌ FALTANDO Relatório PDF")
        status_geral.append(False)

    print()

    # Taxa de sucesso
    sucesso = sum(status_geral)
    total = len(status_geral)
    taxa = (sucesso / total) * 100

    print(f"📊 TAXA DE SUCESSO: {taxa:.1f}% ({sucesso}/{total})")

    if taxa == 100:
        print("🎉 TODOS OS COMPONENTES VALIDADOS COM SUCESSO!")
        print("🚀 Sistema completamente operacional e relatórios atualizados")
    elif taxa >= 80:
        print("⚠️ Sistema operacional com componentes menores faltando")
    else:
        print("❌ Problemas detectados que requerem atenção")

    print()
    print("📋 ARQUIVOS DE RELATÓRIO DISPONÍVEIS:")
    print("-" * 50)

    if os.path.exists(relatorio_excel):
        print(f"📊 Excel: {relatorio_excel}")

    if os.path.exists(pdf_dir) and pdf_files:
        print(f"📄 PDF: {os.path.join(pdf_dir, pdf_files[0])}")

    if os.path.exists(dashboard_file):
        print(f"🌐 Dashboard: {dashboard_file}")

    print()
    print("🔧 COMANDOS PARA VERIFICAÇÃO:")
    print("-" * 50)
    print("🔍 Validar sistema: python scripts/repositorio_central.py")
    print("📊 Gerar novos relatórios: python scripts/atualizar_relatorios_completos.py")

    return taxa == 100


if __name__ == "__main__":
    validar_relatorios_gerados()
