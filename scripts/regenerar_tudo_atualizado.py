#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para regenerar todos os relatórios com dados atualizados
"""

import pandas as pd
import json
from datetime import datetime
import subprocess
import os


def regenerar_relatorios_atualizados():
    """Regenera todos os relatórios usando dados atualizados"""

    print("🔄 REGENERANDO RELATÓRIOS COM DADOS ATUALIZADOS...")
    print("=" * 60)
    print(f"📅 Data/hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

    # Verificar se arquivos de dados existem
    arquivos_necessarios = [
        "distancias_escolas_diretorias.xlsx",
        "QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx",
        "GEP.xlsx",
        "dados_veiculos_atualizados.json",
        "dados_escolas_atualizados.json",
        "estatisticas_atualizadas.json",
    ]

    print("📋 Verificando arquivos necessários...")
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} - AUSENTE")
            return False

    print("\n🎯 EXECUTANDO REGENERAÇÃO COMPLETA...")
    print("-" * 40)

    # 1. Relatório Excel Completo
    print("📊 1/4: Gerando Relatório Excel Completo...")
    try:
        result = subprocess.run(
            [
                r"C:\Users\es.bruno.vargas\Desktop\escolas_indigina_quilo_assent\.venv\Scripts\python.exe",
                "gerar_relatorio_excel.py",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("   ✅ Relatório Excel gerado com sucesso!")
        else:
            print(f"   ⚠️  Aviso no Excel: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Erro no Excel: {e}")

    # 2. Relatório PDF
    print("\n📄 2/4: Gerando Relatório PDF...")
    try:
        result = subprocess.run(
            [
                r"C:\Users\es.bruno.vargas\Desktop\escolas_indigina_quilo_assent\.venv\Scripts\python.exe",
                "gerar_relatorio_pdf.py",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("   ✅ Relatório PDF gerado com sucesso!")
        else:
            print(f"   ⚠️  Aviso no PDF: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Erro no PDF: {e}")

    # 3. Análise de Frota Integrada
    print("\n🚗 3/4: Gerando Análise de Frota Integrada...")
    try:
        result = subprocess.run(
            [
                r"C:\Users\es.bruno.vargas\Desktop\escolas_indigina_quilo_assent\.venv\Scripts\python.exe",
                "analise_frota_integrada.py",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("   ✅ Análise de Frota gerada com sucesso!")
        else:
            print(f"   ⚠️  Aviso na Frota: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Erro na Frota: {e}")

    # 4. Gráficos de Análise
    print("\n📊 4/4: Gerando Gráficos de Análise...")
    try:
        result = subprocess.run(
            [
                r"C:\Users\es.bruno.vargas\Desktop\escolas_indigina_quilo_assent\.venv\Scripts\python.exe",
                "gerar_graficos_frota.py",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("   ✅ Gráficos gerados com sucesso!")
        else:
            print(f"   ⚠️  Aviso nos Gráficos: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Erro nos Gráficos: {e}")

    # 5. Verificar arquivos gerados
    print("\n📁 VERIFICANDO ARQUIVOS GERADOS:")
    print("-" * 30)

    arquivos_saida = [
        ("Excel Completo", "Relatorio_Completo_Escolas_Diretorias.xlsx"),
        ("PDF Paisagem", "Relatorio_Paisagem_*.pdf"),
        ("Análise de Frota", "Analise_Integrada_Escolas_Frota_Supervisao.xlsx"),
        ("Gráficos PNG", "Graficos_Analise_Frota.png"),
        ("Mapa de Calor", "Mapa_Calor_Necessidade_Veiculos.png"),
        ("Dashboard HTML", "distancias_escolas.html"),
    ]

    for desc, arquivo in arquivos_saida:
        if "*" in arquivo:
            # Listar arquivos com padrão
            import glob

            files = glob.glob(arquivo)
            if files:
                print(f"✅ {desc}: {len(files)} arquivo(s)")
                for f in files[:2]:  # Mostrar até 2 arquivos
                    tamanho = os.path.getsize(f) / 1024
                    print(f"   📄 {f} ({tamanho:.1f} KB)")
            else:
                print(f"❌ {desc}: Não encontrado")
        else:
            if os.path.exists(arquivo):
                tamanho = os.path.getsize(arquivo) / 1024
                print(f"✅ {desc}: {arquivo} ({tamanho:.1f} KB)")
            else:
                print(f"❌ {desc}: Não encontrado")

    # 6. Resumo das atualizações
    print("\n📊 RESUMO DAS ATUALIZAÇÕES:")
    print("=" * 40)

    try:
        with open("estatisticas_atualizadas.json", "r", encoding="utf-8") as f:
            stats = json.load(f)

        print(f"🏫 Total de escolas: {stats['total_escolas']}")
        print(f"🔴 Escolas indígenas: {stats['escolas_indigenas']}")
        print(f"🟢 Escolas quilombolas/assentamentos: {stats['escolas_quilombolas']}")
        print(f"🚗 Total de veículos: {stats['total_veiculos']}")
        print(f"📍 Diretorias com veículos: {stats['diretorias_com_veiculos']}")
        print(f"⚠️  Escolas alta prioridade: {stats['escolas_alta_prioridade']}")
        if stats["distancia_media"] > 0:
            print(f"📏 Distância média: {stats['distancia_media']} km")

    except Exception as e:
        print(f"Erro ao ler estatísticas: {e}")

    # 7. Dados de supervisão GEP
    print(f"\n👥 SUPERVISÃO GEP INTEGRADA:")
    try:
        with open("dados_supervisao_atualizados.json", "r", encoding="utf-8") as f:
            supervisao = json.load(f)

        print(f"   📋 {len(supervisao)} regiões de supervisão mapeadas")
        for regiao, dados in list(supervisao.items())[:3]:  # Mostrar 3 primeiras
            print(f"   🌍 {regiao}: {dados['supervisor']}")

        if len(supervisao) > 3:
            print(f"   ... e mais {len(supervisao) - 3} regiões")

    except Exception as e:
        print(f"   ⚠️ Dados de supervisão não disponíveis: {e}")

    print(f"\n✅ REGENERAÇÃO COMPLETA FINALIZADA!")
    print(f"📅 Concluído em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"\n🎯 Próximas ações sugeridas:")
    print(f"   1. Verificar dashboard HTML atualizado")
    print(f"   2. Revisar relatórios Excel e PDF")
    print(f"   3. Analisar gráficos de demanda de frota")
    print(f"   4. Confirmar integração dos dados GEP")

    return True


if __name__ == "__main__":
    success = regenerar_relatorios_atualizados()
    if not success:
        print("\n❌ Falha na regeneração. Verifique os arquivos de entrada.")
        exit(1)
