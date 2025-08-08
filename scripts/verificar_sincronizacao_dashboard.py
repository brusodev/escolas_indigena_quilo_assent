#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar se o dashboard está usando os dados da fonte principal.
"""

import json
import os


def verificar_sincronizacao_dashboard():
    """Verifica se o dashboard está sincronizado com a fonte principal."""

    print("🔍 VERIFICANDO SINCRONIZAÇÃO DO DASHBOARD")
    print("=" * 50)

    # Verificar existência dos arquivos
    arquivo_dashboard = "dashboard/dados_veiculos_diretorias.json"
    arquivo_principal = "dados/json/dados_veiculos_atualizados.json"

    print("📂 VERIFICANDO ARQUIVOS:")
    existe_dashboard = os.path.exists(arquivo_dashboard)
    existe_principal = os.path.exists(arquivo_principal)

    print(f"   {'✅' if existe_dashboard else '❌'} Dashboard: {arquivo_dashboard}")
    print(f"   {'✅' if existe_principal else '❌'} Principal: {arquivo_principal}")

    if not existe_dashboard or not existe_principal:
        print("\n❌ Arquivos necessários não encontrados!")
        return False

    # Carregar dados
    try:
        with open(arquivo_dashboard, "r", encoding="utf-8") as f:
            dados_dashboard = json.load(f)

        with open(arquivo_principal, "r", encoding="utf-8") as f:
            dados_principal = json.load(f)

        print("\n📊 DADOS CARREGADOS COM SUCESSO")

    except Exception as e:
        print(f"\n❌ Erro ao carregar dados: {e}")
        return False

    # Comparar estruturas
    diretorias_dashboard = dados_dashboard.get("diretorias", {})
    diretorias_principal = dados_principal

    print(f"\n🔢 COMPARAÇÃO DE TOTAIS:")
    total_dashboard = sum(d.get("total", 0) for d in diretorias_dashboard.values())
    total_principal = sum(d.get("total", 0) for d in diretorias_principal.values())

    print(f"   Dashboard: {total_dashboard} veículos")
    print(f"   Principal: {total_principal} veículos")
    print(f"   Sincronizado: {'✅' if total_dashboard == total_principal else '❌'}")

    # Verificar metadados do dashboard
    meta = dados_dashboard.get("metadata", {})
    print(f"\n📋 METADADOS DO DASHBOARD:")
    print(f"   Total de veículos: {meta.get('total_veiculos', 'N/A')}")
    print(f"   Diretorias relevantes: {meta.get('diretorias_relevantes', 'N/A')}")
    print(f"   Veículos relevantes: {meta.get('veiculos_relevantes', 'N/A')}")
    print(f"   Data atualização: {meta.get('data_atualizacao', 'N/A')}")
    print(f"   Fonte: {meta.get('fonte', 'N/A')}")

    # Verificar diretorias específicas
    diretorias_teste = ["BAURU", "SANTOS", "TUPÃ", "ADAMANTINA"]
    print(f"\n🔍 VERIFICAÇÃO DE DIRETORIAS ESPECÍFICAS:")

    todas_sincronizadas = True
    for diretoria in diretorias_teste:
        if diretoria in diretorias_dashboard and diretoria in diretorias_principal:
            dash_data = diretorias_dashboard[diretoria]
            prin_data = diretorias_principal[diretoria]

            sincronizada = (
                dash_data.get("total", 0) == prin_data.get("total", 0)
                and dash_data.get("s1", 0) == prin_data.get("s1", 0)
                and dash_data.get("s2", 0) == prin_data.get("s2", 0)
                and dash_data.get("s2_4x4", 0) == prin_data.get("s2_4x4", 0)
            )

            status = "✅" if sincronizada else "❌"
            print(f"   {status} {diretoria}:")
            print(
                f"       Dashboard: {dash_data.get('total', 0)} ({dash_data.get('s1', 0)}S1+{dash_data.get('s2', 0)}S2+{dash_data.get('s2_4x4', 0)}S2_4x4)"
            )
            print(
                f"       Principal: {prin_data.get('total', 0)} ({prin_data.get('s1', 0)}S1+{prin_data.get('s2', 0)}S2+{prin_data.get('s2_4x4', 0)}S2_4x4)"
            )

            if not sincronizada:
                todas_sincronizadas = False
        else:
            print(f"   ⚠️  {diretoria}: Não encontrada em um dos arquivos")
            todas_sincronizadas = False

    # Verificar se os dados completos são idênticos
    print(f"\n🔄 VERIFICAÇÃO COMPLETA:")
    dados_identicos = diretorias_dashboard == diretorias_principal
    print(f"   Dados idênticos: {'✅' if dados_identicos else '❌'}")

    if dados_identicos:
        print("\n✅ DASHBOARD COMPLETAMENTE SINCRONIZADO!")
        print(
            "🎯 O dashboard está usando exatamente os mesmos dados da fonte principal."
        )
    else:
        print("\n⚠️  DASHBOARD PODE ESTAR DESATUALIZADO")
        print("🔄 Recomendação: Execute o script de atualização do dashboard.")

    # Verificar fonte dos dados no HTML
    print(f"\n📁 VERIFICAÇÃO DA FONTE NO HTML:")
    try:
        with open("dashboard/dashboard_integrado.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        if "dados_veiculos_diretorias.json" in html_content:
            print("   ✅ HTML configurado para carregar dados_veiculos_diretorias.json")
        else:
            print("   ❌ HTML não está configurado para carregar o arquivo correto")
    except Exception as e:
        print(f"   ❌ Erro ao verificar HTML: {e}")

    return dados_identicos and todas_sincronizadas


if __name__ == "__main__":
    resultado = verificar_sincronizacao_dashboard()

    if resultado:
        print("\n🎉 CONCLUSÃO: Dashboard está usando os dados da fonte principal!")
    else:
        print("\n⚠️  CONCLUSÃO: Dashboard precisa ser atualizado.")
        print("💡 Execute: python scripts/atualizar_dashboard_correto.py")
