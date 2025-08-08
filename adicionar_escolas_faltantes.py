#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adicionar as 4 escolas faltantes do dashboard ao arquivo Excel
"""

import pandas as pd
import re
import json


def extrair_dados_escolas_dashboard():
    """Extrai dados completos das escolas do dashboard"""
    print("🔍 EXTRAINDO DADOS COMPLETOS DO DASHBOARD")
    print("=" * 60)

    escolas_faltantes = [
        "BAIRRO BOMBAS DE CIMA",
        "BAIRRO DE BOMBAS",
        "FAZENDA DA CAIXA",
        "MARIA ANTONIA CHULES PRINCS",
    ]

    try:
        with open("dashboard_integrado.html", "r", encoding="utf-8") as f:
            content = f.read()

        # Buscar o array schoolsData
        match = re.search(r"const schoolsData = \[(.*?)\];", content, re.DOTALL)
        if not match:
            print("❌ Não encontrou schoolsData no dashboard")
            return []

        schools_text = match.group(1)

        # Dividir em objetos individuais
        school_objects = re.findall(r"\{[^}]+\}", schools_text)

        escolas_encontradas = []

        for obj in school_objects:
            # Extrair dados de cada escola
            name_match = re.search(r'"name":\s*"([^"]+)"', obj)
            type_match = re.search(r'"type":\s*"([^"]+)"', obj)
            city_match = re.search(r'"city":\s*"([^"]+)"', obj)
            diretoria_match = re.search(r'"diretoria":\s*"([^"]+)"', obj)
            distance_match = re.search(r'"distance":\s*([0-9.]+)', obj)
            lat_match = re.search(r'"lat":\s*(-?[0-9.]+)', obj)
            lng_match = re.search(r'"lng":\s*(-?[0-9.]+)', obj)

            if name_match:
                nome = name_match.group(1).strip()

                # Verificar se é uma das escolas faltantes
                if any(
                    faltante.upper() in nome.upper() for faltante in escolas_faltantes
                ):
                    escola_data = {
                        "Nome_Escola": nome,
                        "Tipo_Escola": type_match.group(1) if type_match else "",
                        "Cidade_Escola": city_match.group(1) if city_match else "",
                        "Endereco_Escola": "",  # Não disponível no dashboard
                        "DE_Responsavel": (
                            diretoria_match.group(1) if diretoria_match else ""
                        ),
                        "Zona": "",  # Não disponível no dashboard
                        "Latitude_Escola": (
                            float(lat_match.group(1)) if lat_match else 0
                        ),
                        "Longitude_Escola": (
                            float(lng_match.group(1)) if lng_match else 0
                        ),
                        "Nome_Diretoria": (
                            diretoria_match.group(1) if diretoria_match else ""
                        ),
                        "Cidade_Diretoria": "",  # Será preenchido depois
                        "Endereco_Diretoria": "",  # Será preenchido depois
                        "Latitude_Diretoria": 0,  # Será preenchido depois
                        "Longitude_Diretoria": 0,  # Será preenchido depois
                        "Distancia_KM": (
                            float(distance_match.group(1)) if distance_match else 0
                        ),
                    }
                    escolas_encontradas.append(escola_data)
                    print(
                        f"✅ Encontrada: {nome} ({escola_data['Cidade_Escola']}) - {escola_data['Distancia_KM']} km"
                    )

        print(
            f"\n📊 Total de escolas faltantes encontradas: {len(escolas_encontradas)}"
        )
        return escolas_encontradas

    except Exception as e:
        print(f"❌ Erro ao extrair dados: {e}")
        return []


def completar_dados_diretorias(escolas_data):
    """Completa dados das diretorias a partir do Excel existente"""
    print("\n🔍 COMPLETANDO DADOS DAS DIRETORIAS")
    print("=" * 60)

    try:
        df_excel = pd.read_excel("distancias_escolas_diretorias_corrigido.xlsx")

        # Criar mapeamento de diretorias
        diretorias_map = {}
        for _, row in df_excel.iterrows():
            nome_dir = row["Nome_Diretoria"]
            if nome_dir not in diretorias_map:
                diretorias_map[nome_dir] = {
                    "Cidade_Diretoria": row.get("Cidade_Diretoria", ""),
                    "Endereco_Diretoria": row.get("Endereco_Diretoria", ""),
                    "Latitude_Diretoria": row.get("Latitude_Diretoria", 0),
                    "Longitude_Diretoria": row.get("Longitude_Diretoria", 0),
                }

        # Completar dados das escolas
        for escola in escolas_data:
            nome_dir = escola["Nome_Diretoria"]
            if nome_dir in diretorias_map:
                escola.update(diretorias_map[nome_dir])
                print(f"✅ Completados dados da diretoria: {nome_dir}")
            else:
                print(f"⚠️  Diretoria não encontrada: {nome_dir}")

        return escolas_data

    except Exception as e:
        print(f"❌ Erro ao completar dados: {e}")
        return escolas_data


def adicionar_escolas_ao_excel(escolas_data):
    """Adiciona as escolas ao arquivo Excel"""
    print("\n📊 ADICIONANDO ESCOLAS AO EXCEL")
    print("=" * 60)

    try:
        # Carregar Excel existente
        df_excel = pd.read_excel("distancias_escolas_diretorias_corrigido.xlsx")
        print(f"📋 Excel atual: {len(df_excel)} escolas")

        # Converter escolas para DataFrame
        df_novas = pd.DataFrame(escolas_data)

        # Garantir que todas as colunas existam
        for col in df_excel.columns:
            if col not in df_novas.columns:
                df_novas[col] = ""

        # Reorganizar colunas na mesma ordem
        df_novas = df_novas[df_excel.columns]

        # Concatenar
        df_completo = pd.concat([df_excel, df_novas], ignore_index=True)

        print(f"📋 Excel atualizado: {len(df_completo)} escolas")
        print(f"➕ Adicionadas: {len(escolas_data)} escolas")

        # Salvar arquivo atualizado
        nome_arquivo = "distancias_escolas_diretorias_completo_63.xlsx"
        df_completo.to_excel(nome_arquivo, index=False)

        print(f"💾 Arquivo salvo: {nome_arquivo}")

        # Verificar KOPENOTI
        kopenoti = df_completo[
            df_completo["Nome_Escola"].str.contains("KOPENOTI", na=False, case=False)
        ]
        if not kopenoti.empty:
            distancia = kopenoti.iloc[0]["Distancia_KM"]
            print(f"🎯 Verificação KOPENOTI: {distancia:.2f} km")

        return df_completo

    except Exception as e:
        print(f"❌ Erro ao adicionar escolas: {e}")
        return None


def main():
    """Função principal"""
    print("🚀 ADICIONANDO ESCOLAS FALTANTES AO EXCEL")
    print("=" * 70)

    # Extrair dados das escolas faltantes
    escolas_data = extrair_dados_escolas_dashboard()

    if not escolas_data:
        print("❌ Nenhuma escola faltante encontrada")
        return

    if len(escolas_data) != 4:
        print(f"⚠️  Esperava 4 escolas, encontrou {len(escolas_data)}")

    # Completar dados das diretorias
    escolas_data = completar_dados_diretorias(escolas_data)

    # Adicionar ao Excel
    df_completo = adicionar_escolas_ao_excel(escolas_data)

    if df_completo is not None:
        print("\n🎯 RESUMO FINAL:")
        print("=" * 70)
        print(f"✅ Arquivo Excel atualizado com {len(df_completo)} escolas")
        print(f"✅ Dashboard e Excel agora sincronizados")
        print(f"✅ Próximo passo: Regenerar relatórios Excel e PDF")

        print(f"\n📋 ESCOLAS ADICIONADAS:")
        for i, escola in enumerate(escolas_data, 1):
            print(
                f"   {i}. {escola['Nome_Escola']} ({escola['Cidade_Escola']}) - {escola['Distancia_KM']} km"
            )


if __name__ == "__main__":
    main()
