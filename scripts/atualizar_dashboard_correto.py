#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para atualizar o dashboard com os dados corretos dos veículos.
"""

import json
import shutil
from datetime import datetime


def atualizar_dashboard():
    """Atualiza o dashboard com os dados corretos."""

    print("🔄 ATUALIZANDO DASHBOARD COM DADOS CORRETOS")
    print("=" * 50)

    # 1. Copiar arquivo de dados corretos para o dashboard
    print("1️⃣ Copiando dados corretos para o dashboard...")

    arquivo_origem = "dados/json/dados_veiculos_atualizados.json"
    arquivo_destino = "dashboard/dados_veiculos_diretorias.json"

    try:
        # Carregar dados corretos
        with open(arquivo_origem, "r", encoding="utf-8") as f:
            dados_corretos = json.load(f)

        # Contar totais
        diretorias_relevantes = [
            "ADAMANTINA",
            "AMERICANA",
            "ARAÇATUBA",
            "ARARAQUARA",
            "BAURU",
            "BOTUCATU",
            "BRAGANÇA PAULISTA",
            "CARAPICUÍBA",
            "DIADEMA",
            "FERNANDÓPOLIS",
            "GUARULHOS NORTE",
            "GUARULHOS SUL",
            "ITAPECERICA DA SERRA",
            "JALES",
            "JOSÉ BONIFÁCIO",
            "MARÍLIA",
            "OSASCO",
            "PRESIDENTE PRUDENTE",
            "TUPÃ",
        ]

        total_relevantes = 0
        total_s1 = 0
        total_s2 = 0
        total_s2_4x4 = 0
        total_geral = 0

        for diretoria, dados in dados_corretos.items():
            total_geral += dados.get("total", 0)
            if diretoria in diretorias_relevantes:
                total_relevantes += dados.get("total", 0)
                total_s1 += dados.get("s1", 0)
                total_s2 += dados.get("s2", 0)
                total_s2_4x4 += dados.get("s2_4x4", 0)

        # Criar estrutura para o dashboard
        dados_dashboard = {
            "metadata": {
                "total_veiculos": total_geral,
                "total_diretorias": len(dados_corretos),
                "diretorias_relevantes": len(diretorias_relevantes),
                "veiculos_relevantes": total_relevantes,
                "distribuicao_relevantes": {
                    "s1": total_s1,
                    "s2": total_s2,
                    "s2_4x4": total_s2_4x4,
                },
                "data_atualizacao": datetime.now().strftime("%d/%m/%Y - %H:%M"),
                "fonte": "dados_veiculos_originais_corretos.json",
            },
            "diretorias": dados_corretos,
        }

        # Salvar no dashboard
        with open(arquivo_destino, "w", encoding="utf-8") as f:
            json.dump(dados_dashboard, f, indent=2, ensure_ascii=False)

        print(f"   ✅ Arquivo criado: {arquivo_destino}")
        print(f"   📊 Total de veículos: {total_geral}")
        print(f"   📊 Veículos em diretorias relevantes: {total_relevantes}")
        print(
            f"   📊 Distribuição: S1={total_s1}, S2={total_s2}, S2_4x4={total_s2_4x4}"
        )

    except Exception as e:
        print(f"   ❌ Erro ao copiar dados: {e}")
        return False

    # 2. Atualizar metadados no HTML
    print("\n2️⃣ Atualizando metadados no dashboard HTML...")

    arquivo_html = "dashboard/dashboard_integrado.html"

    try:
        with open(arquivo_html, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Atualizar linha de veículos distribuídos
        conteudo = conteudo.replace(
            "- Veículos: dados_veiculos_diretorias.json (172 veículos distribuídos)",
            f"- Veículos: dados_veiculos_diretorias.json ({total_geral} veículos distribuídos)",
        )

        # Atualizar data de atualização
        data_atual = datetime.now().strftime("%d/%m/%Y - %H:%M")
        import re

        conteudo = re.sub(
            r"Data da última atualização: \d{2}/\d{2}/\d{4} - \d{2}:\d{2}",
            f"Data da última atualização: {data_atual}",
            conteudo,
        )

        # Atualizar total de veículos embebidos
        conteudo = conteudo.replace(
            '"total_veiculos": 172,', f'"total_veiculos": {total_geral},'
        )

        with open(arquivo_html, "w", encoding="utf-8") as f:
            f.write(conteudo)

        print(f"   ✅ Dashboard HTML atualizado")
        print(f"   📊 Nova data: {data_atual}")

    except Exception as e:
        print(f"   ❌ Erro ao atualizar HTML: {e}")
        return False

    # 3. Verificar integridade
    print("\n3️⃣ Verificando integridade...")

    try:
        with open(arquivo_destino, "r", encoding="utf-8") as f:
            dados_verificacao = json.load(f)

        meta = dados_verificacao["metadata"]
        print(f"   ✅ Total de veículos: {meta['total_veiculos']}")
        print(f"   ✅ Diretorias relevantes: {meta['diretorias_relevantes']}")
        print(f"   ✅ Veículos relevantes: {meta['veiculos_relevantes']}")
        print(f"   ✅ Data de atualização: {meta['data_atualizacao']}")

    except Exception as e:
        print(f"   ❌ Erro na verificação: {e}")
        return False

    print("\n✅ DASHBOARD ATUALIZADO COM SUCESSO!")
    print("🌐 Agora o dashboard usa os dados corretos dos veículos!")

    return True


if __name__ == "__main__":
    sucesso = atualizar_dashboard()
    if sucesso:
        print("\n🚀 Para ver o dashboard atualizado:")
        print("   📂 Abra: dashboard/dashboard_integrado.html")
        print("   🔄 Ou execute: python -m http.server 8000")
        print(
            "   🌐 E acesse: http://localhost:8000/dashboard/dashboard_integrado.html"
        )
    else:
        print("\n❌ Falha na atualização do dashboard.")
