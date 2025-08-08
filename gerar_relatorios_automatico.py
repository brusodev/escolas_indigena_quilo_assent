#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar relatórios automaticamente com os dados atualizados
"""

import json
import pandas as pd
from datetime import datetime
import os


def gerar_relatorios_automatico():
    """Gera relatórios automaticamente sem interação do usuário"""

    print("🔄 GERANDO RELATÓRIOS ATUALIZADOS...")
    print("=" * 60)

    try:
        # 1. Carregar dados atualizados
        print("📂 Carregando dados atualizados...")

        with open("dados_escolas_atualizados.json", "r", encoding="utf-8") as f:
            escolas_dados = json.load(f)

        with open("dados_veiculos_atualizados.json", "r", encoding="utf-8") as f:
            veiculos_dados = json.load(f)

        with open("estatisticas_atualizadas.json", "r", encoding="utf-8") as f:
            stats = json.load(f)

        print(f"   ✅ {len(escolas_dados)} escolas carregadas")
        print(f"   ✅ {len(veiculos_dados)} diretorias com dados de veículos")

        # 2. Preparar dados para Excel
        print("\n📊 Preparando dados para relatório Excel...")

        # Criar DataFrame das escolas
        df_escolas = pd.DataFrame(escolas_dados)

        # Adicionar dados de veículos correspondentes
        df_escolas['veiculos_total'] = df_escolas.apply(
            lambda row: veiculos_dados.get(
                row['diretoria'].upper(), {}).get('total', 0),
            axis=1
        )
        df_escolas['veiculos_s1'] = df_escolas.apply(
            lambda row: veiculos_dados.get(
                row['diretoria'].upper(), {}).get('s1', 0),
            axis=1
        )
        df_escolas['veiculos_s2'] = df_escolas.apply(
            lambda row: veiculos_dados.get(
                row['diretoria'].upper(), {}).get('s2', 0),
            axis=1
        )
        df_escolas['veiculos_s2_4x4'] = df_escolas.apply(
            lambda row: veiculos_dados.get(
                row['diretoria'].upper(), {}).get('s2_4x4', 0),
            axis=1
        )

        # Calcular prioridade
        def calcular_prioridade(row):
            if row['distance'] > 50 and row['veiculos_total'] == 0:
                return 'Alta'
            elif row['distance'] > 30 and row['veiculos_total'] == 0:
                return 'Média'
            else:
                return 'Baixa'

        df_escolas['prioridade'] = df_escolas.apply(
            calcular_prioridade, axis=1)

        # 3. Gerar relatório Excel
        print("\n📄 Gerando relatório Excel...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"Relatorio_Completo_Atualizado_{timestamp}.xlsx"

        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            # Aba principal - Dados das escolas
            df_escolas_excel = df_escolas[[
                'name', 'type', 'city', 'diretoria', 'distance',
                'veiculos_total', 'veiculos_s1', 'veiculos_s2', 'veiculos_s2_4x4',
                'prioridade', 'lat', 'lng'
            ]].copy()

            # Renomear colunas para português
            df_escolas_excel.columns = [
                'Nome_Escola', 'Tipo_Escola', 'Cidade', 'Diretoria', 'Distancia_KM',
                'Veiculos_Total', 'Veiculos_S1', 'Veiculos_S2', 'Veiculos_S2_4x4',
                'Prioridade', 'Latitude', 'Longitude'
            ]

            df_escolas_excel.to_excel(
                writer, sheet_name='Escolas_Completo', index=False)

            # Aba de estatísticas por diretoria
            df_diretorias = []
            for diretoria_key, dados_veiculos in veiculos_dados.items():
                escolas_na_diretoria = df_escolas[df_escolas['diretoria'].str.upper(
                ) == diretoria_key]

                df_diretorias.append({
                    'Diretoria': dados_veiculos['diretoria_original'],
                    'Total_Escolas': len(escolas_na_diretoria),
                    'Escolas_Indigenas': len(escolas_na_diretoria[escolas_na_diretoria['type'] == 'indigena']),
                    'Escolas_Quilombolas': len(escolas_na_diretoria[escolas_na_diretoria['type'] == 'quilombola']),
                    'Distancia_Media': round(escolas_na_diretoria['distance'].mean(), 2) if len(escolas_na_diretoria) > 0 else 0,
                    'Escolas_Alta_Prioridade': len(escolas_na_diretoria[escolas_na_diretoria['prioridade'] == 'Alta']),
                    'Veiculos_Total': dados_veiculos['total'],
                    'Veiculos_S1': dados_veiculos['s1'],
                    'Veiculos_S2': dados_veiculos['s2'],
                    'Veiculos_S2_4x4': dados_veiculos['s2_4x4']
                })

            df_diretorias = pd.DataFrame(df_diretorias)
            df_diretorias.to_excel(
                writer, sheet_name='Resumo_Diretorias', index=False)

            # Aba de estatísticas gerais
            df_stats = pd.DataFrame([
                ['Total de Escolas', stats['total_escolas']],
                ['Escolas Indígenas', stats['escolas_indigenas']],
                ['Escolas Quilombolas', stats['escolas_quilombolas']],
                ['Total de Veículos', stats['total_veiculos']],
                ['Veículos S-1', sum(v['s1']
                                     for v in veiculos_dados.values())],
                ['Veículos S-2', sum(v['s2']
                                     for v in veiculos_dados.values())],
                ['Veículos S-2 4X4', sum(v['s2_4x4']
                                         for v in veiculos_dados.values())],
                ['Diretorias com Veículos', stats['diretorias_com_veiculos']],
                ['Escolas Alta Prioridade', stats['escolas_alta_prioridade']],
                ['Distância Média (km)', round(stats['distancia_media'], 2)]
            ], columns=['Indicador', 'Valor'])

            df_stats.to_excel(
                writer, sheet_name='Estatisticas_Gerais', index=False)

        print(f"   ✅ Relatório Excel criado: {excel_filename}")

        # 4. Tentar gerar relatório PDF
        print("\n📄 Tentando gerar relatório PDF...")
        try:
            import subprocess
            import sys

            result = subprocess.run([sys.executable, "gerar_relatorio_pdf.py"],
                                    capture_output=True, text=True, encoding='utf-8',
                                    timeout=60)

            if result.returncode == 0:
                print("   ✅ Relatório PDF gerado com sucesso!")
            else:
                print(f"   ⚠️  Aviso ao gerar PDF: {result.stderr}")

        except Exception as e:
            print(f"   ⚠️  Não foi possível gerar PDF automaticamente: {e}")

        # 5. Resumo final
        print(f"\n📋 RESUMO DOS RELATÓRIOS GERADOS:")
        print("=" * 50)
        print(f"📊 Dados processados:")
        print(f"   • {stats['total_escolas']} escolas")
        print(f"   • {stats['total_veiculos']} veículos")
        print(f"   • {stats['diretorias_com_veiculos']} diretorias")
        print(
            f"   • {stats['escolas_alta_prioridade']} escolas de alta prioridade")

        print(f"\n📁 Arquivos gerados:")
        print(f"   ✅ {excel_filename}")

        # Listar outros relatórios existentes
        relatorios_pdf = [f for f in os.listdir('.') if f.startswith(
            'Relatorio_') and f.endswith('.pdf')]
        if relatorios_pdf:
            relatorio_mais_recente = max(relatorios_pdf, key=os.path.getctime)
            print(f"   📄 PDF mais recente: {relatorio_mais_recente}")

        print(f"\n✅ RELATÓRIOS ATUALIZADOS COM SUCESSO!")
        print(f"📅 Data/hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        return True

    except Exception as e:
        print(f"❌ Erro ao gerar relatórios: {e}")
        return False


if __name__ == "__main__":
    gerar_relatorios_automatico()
