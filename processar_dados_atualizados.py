#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para processar dados atualizados das três planilhas principais
e gerar arquivos JSON para o dashboard HTML
"""

import pandas as pd
import json
import numpy as np
from datetime import datetime


def processar_dados_atualizados():
    """Processa todos os dados atualizados das planilhas"""

    print("🔄 PROCESSANDO DADOS ATUALIZADOS...")
    print("=" * 60)

    # 1. Carregar dados de distâncias
    print("📊 1. Carregando dados de distâncias...")
    try:
        dist_df = pd.read_excel("distancias_escolas_diretorias.xlsx")
        print(f"   ✅ {len(dist_df)} registros de distâncias carregados")
        print(f"   📋 Colunas: {list(dist_df.columns)}")

        # Verificar se há coordenadas atualizadas
        if (
            "Latitude_Escola" in dist_df.columns
            and "Longitude_Escola" in dist_df.columns
        ):
            coordenadas_validas = dist_df.dropna(
                subset=["Latitude_Escola", "Longitude_Escola"]
            )
            print(f"   📍 {len(coordenadas_validas)} escolas com coordenadas válidas")
    except Exception as e:
        print(f"   ❌ Erro ao carregar distâncias: {e}")
        return False

    # 2. Carregar dados de veículos atualizados
    print("\n🚗 2. Carregando dados de veículos...")
    try:
        veic_df = pd.read_excel("QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx")
        print(f"   ✅ {len(veic_df)} diretorias com dados de veículos")

        # Calcular totais de veículos
        veiculos_por_diretoria = {}
        total_veiculos = 0

        for _, row in veic_df.iterrows():
            diretoria = row["DIRETORIA"]
            s1 = row.get("QUANTIDADE S-1", 0) or 0
            s2 = row.get("QUANTIDADE S-2", 0) or 0
            s2_4x4 = row.get("QUANTIDADE S-2 4X4", 0) or 0
            total = s1 + s2 + s2_4x4

            veiculos_por_diretoria[diretoria.upper()] = {
                "total": int(total),
                "s1": int(s1),
                "s2": int(s2),
                "s2_4x4": int(s2_4x4),
                "diretoria_original": diretoria,
            }
            total_veiculos += total

            print(
                f"   🚙 {diretoria}: {int(total)} veículos (S1:{int(s1)}, S2:{int(s2)}, S2-4x4:{int(s2_4x4)})"
            )

        print(f"   📊 Total geral: {int(total_veiculos)} veículos")

    except Exception as e:
        print(f"   ❌ Erro ao carregar veículos: {e}")
        return False

    # 3. Carregar dados do GEP (Supervisão)
    print("\n👥 3. Carregando dados do GEP...")
    try:
        gep_df = pd.read_excel("GEP.xlsx")
        print(f"   ✅ {len(gep_df)} registros de supervisão carregados")
        print(f"   📋 Colunas: {list(gep_df.columns)}")

        # Processar dados de supervisão
        supervisao_dados = {}
        for _, row in gep_df.iterrows():
            regiao = row.get("REGIÃO", "N/A")
            supervisor = row.get("SUPERVISOR GEP", "N/A")
            diretorias = row.get("DIRETORIA DE ENSINO SOB SUPERVISÃO", "N/A")

            supervisao_dados[regiao] = {
                "supervisor": supervisor,
                "diretorias": diretorias,
                "quantidade_des": row.get("QUANTIDADE DE DEs", 0),
            }

            print(f"   👤 {regiao}: {supervisor}")
            print(f"      📍 Diretorias: {diretorias}")

    except Exception as e:
        print(f"   ❌ Erro ao carregar GEP: {e}")
        supervisao_dados = {}

    # 4. Processar dados das escolas para JavaScript
    print("\n🏫 4. Processando dados das escolas...")
    escolas_para_js = []
    estatisticas = {
        "total_escolas": len(dist_df),
        "escolas_indigenas": 0,
        "escolas_quilombolas": 0,
        "total_veiculos": int(total_veiculos),
        "diretorias_com_veiculos": sum(
            1 for v in veiculos_por_diretoria.values() if v["total"] > 0
        ),
        "escolas_alta_prioridade": 0,
        "distancia_media": 0,
    }

    distancias_total = 0

    for _, escola in dist_df.iterrows():
        # Determinar tipo de escola
        nome_escola = str(escola.get("Nome_Escola", "")).upper()
        if any(
            palavra in nome_escola
            for palavra in [
                "ALDEIA",
                "INDIGENA",
                "INDIA",
                "GUARANI",
                "TEKOA",
                "KRUKUTU",
            ]
        ):
            tipo = "indigena"
            estatisticas["escolas_indigenas"] += 1
        else:
            tipo = "quilombola"
            estatisticas["escolas_quilombolas"] += 1

        # Dados da escola
        distancia = escola.get("Distancia_KM", 0)
        if pd.isna(distancia):
            distancia = 0
        else:
            distancias_total += distancia

        diretoria = escola.get("Nome_Diretoria", "")
        cidade = escola.get("Cidade_Escola", "")
        lat_escola = escola.get("Latitude_Escola", 0)
        lng_escola = escola.get("Longitude_Escola", 0)
        lat_diretoria = escola.get("Latitude_Diretoria", 0)
        lng_diretoria = escola.get("Longitude_Diretoria", 0)

        # Verificar prioridade (>50km sem veículos)
        veiculos_diretoria = veiculos_por_diretoria.get(diretoria.upper(), {"total": 0})
        if distancia > 50 and veiculos_diretoria["total"] == 0:
            estatisticas["escolas_alta_prioridade"] += 1

        escola_dados = {
            "name": escola.get("Nome_Escola", ""),
            "type": tipo,
            "city": cidade,
            "diretoria": diretoria,
            "distance": round(distancia, 2),
            "lat": lat_escola if not pd.isna(lat_escola) else 0,
            "lng": lng_escola if not pd.isna(lng_escola) else 0,
            "de_lat": lat_diretoria if not pd.isna(lat_diretoria) else 0,
            "de_lng": lng_diretoria if not pd.isna(lng_diretoria) else 0,
            "endereco_escola": escola.get("Endereco_Escola", ""),
            "endereco_diretoria": escola.get("Endereco_Diretoria", ""),
        }

        escolas_para_js.append(escola_dados)

    # Calcular distância média
    if len(dist_df) > 0:
        estatisticas["distancia_media"] = round(distancias_total / len(dist_df), 1)

    print(f"   📊 Estatísticas:")
    print(f"      🏫 Total de escolas: {estatisticas['total_escolas']}")
    print(f"      🔴 Indígenas: {estatisticas['escolas_indigenas']}")
    print(f"      🟢 Quilombolas/Assentamentos: {estatisticas['escolas_quilombolas']}")
    print(f"      🚗 Total de veículos: {estatisticas['total_veiculos']}")
    print(
        f"      📍 Diretorias com veículos: {estatisticas['diretorias_com_veiculos']}"
    )
    print(
        f"      ⚠️  Escolas alta prioridade: {estatisticas['escolas_alta_prioridade']}"
    )
    print(f"      📏 Distância média: {estatisticas['distancia_media']} km")

    # 5. Salvar dados para JavaScript
    print("\n💾 5. Salvando dados para dashboard...")

    # Dados de veículos para JS
    with open("dados_veiculos_atualizados.json", "w", encoding="utf-8") as f:
        json.dump(veiculos_por_diretoria, f, ensure_ascii=False, indent=2)

    # Dados de escolas para JS
    with open("dados_escolas_atualizados.json", "w", encoding="utf-8") as f:
        json.dump(escolas_para_js, f, ensure_ascii=False, indent=2)

    # Dados de supervisão para JS
    with open("dados_supervisao_atualizados.json", "w", encoding="utf-8") as f:
        json.dump(supervisao_dados, f, ensure_ascii=False, indent=2)

    # Estatísticas para JS
    with open("estatisticas_atualizadas.json", "w", encoding="utf-8") as f:
        json.dump(estatisticas, f, ensure_ascii=False, indent=2)

    print("   ✅ Arquivos JSON criados:")
    print("      📄 dados_veiculos_atualizados.json")
    print("      📄 dados_escolas_atualizados.json")
    print("      📄 dados_supervisao_atualizados.json")
    print("      📄 estatisticas_atualizadas.json")

    # 6. Gerar resumo das mudanças
    print("\n📋 6. RESUMO DAS ATUALIZAÇÕES:")
    print("=" * 40)

    # Identificar diretorias com veículos
    diretorias_com_frota = [
        d["diretoria_original"]
        for d in veiculos_por_diretoria.values()
        if d["total"] > 0
    ]
    diretorias_sem_frota = [
        d["diretoria_original"]
        for d in veiculos_por_diretoria.values()
        if d["total"] == 0
    ]

    print(f"🚗 DIRETORIAS COM VEÍCULOS ({len(diretorias_com_frota)}):")
    for diretoria in sorted(diretorias_com_frota):
        dados = veiculos_por_diretoria[diretoria.upper()]
        print(f"   ✅ {diretoria}: {dados['total']} veículos")

    print(f"\n❌ DIRETORIAS SEM VEÍCULOS ({len(diretorias_sem_frota)}):")
    for diretoria in sorted(diretorias_sem_frota):
        print(f"   ⭕ {diretoria}")

    print(f"\n👥 SUPERVISÃO GEP:")
    for regiao, dados in supervisao_dados.items():
        print(f"   🌍 {regiao}: {dados['supervisor']}")

    print(f"\n⚠️  ESCOLAS DE ALTA PRIORIDADE:")
    print(
        f"   📊 {estatisticas['escolas_alta_prioridade']} escolas >50km sem veículos na diretoria"
    )

    print("\n✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print(f"📅 Data/hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    return True


if __name__ == "__main__":
    success = processar_dados_atualizados()
    if success:
        print("\n🎯 Próximos passos:")
        print("   1. Atualizar dashboard HTML com novos dados")
        print("   2. Corrigir cores das diretorias no mapa")
        print("   3. Integrar dados de supervisão GEP")
        print("   4. Regenerar relatórios")
    else:
        print("\n❌ Erro no processamento. Verifique os arquivos de dados.")
