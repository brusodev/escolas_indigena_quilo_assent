#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para atualizar a base principal de dados de veículos
com os dados corretos validados.
"""

import json
import shutil
from datetime import datetime
import os


def criar_backup():
    """Cria backup do arquivo principal antes da atualização."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_original = "dados/json/dados_veiculos_atualizados.json"
    arquivo_backup = f"dados/json/backup_dados_veiculos_atualizados_{timestamp}.json"

    if os.path.exists(arquivo_original):
        shutil.copy2(arquivo_original, arquivo_backup)
        print(f"   📄 Backup criado: {arquivo_backup}")
        return True
    return False


def atualizar_base_principal():
    """Atualiza a base principal com os dados corretos."""

    print("🔄 ATUALIZANDO BASE PRINCIPAL DE VEÍCULOS")
    print("=" * 50)

    # Criar backup
    print("1️⃣ Criando backup da base atual...")
    backup_criado = criar_backup()

    if not backup_criado:
        print("   ⚠️  Arquivo principal não encontrado, criando novo...")

    # Carregar dados corretos
    print("\n2️⃣ Carregando dados corretos...")
    arquivo_correto = "dados/json/dados_veiculos_originais_corretos.json"

    try:
        with open(arquivo_correto, "r", encoding="utf-8") as f:
            dados_corretos = json.load(f)
        print(f"   ✅ Dados corretos carregados: {len(dados_corretos)} diretorias")
    except FileNotFoundError:
        print(f"   ❌ Arquivo {arquivo_correto} não encontrado!")
        return False

    # Atualizar arquivo principal
    print("\n3️⃣ Atualizando arquivo principal...")
    arquivo_principal = "dados/json/dados_veiculos_atualizados.json"

    try:
        with open(arquivo_principal, "w", encoding="utf-8") as f:
            json.dump(dados_corretos, f, indent=2, ensure_ascii=False)
        print(f"   ✅ Base principal atualizada: {arquivo_principal}")
    except Exception as e:
        print(f"   ❌ Erro ao atualizar base principal: {e}")
        return False

    # Verificação final
    print("\n4️⃣ Verificando atualização...")
    try:
        with open(arquivo_principal, "r", encoding="utf-8") as f:
            dados_verificacao = json.load(f)

        # Contar veículos nas diretorias relevantes
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

        total_veiculos_relevantes = 0
        total_s1 = 0
        total_s2 = 0
        total_s2_4x4 = 0

        for diretoria in diretorias_relevantes:
            if diretoria in dados_verificacao:
                dados_dir = dados_verificacao[diretoria]
                total_veiculos_relevantes += dados_dir.get("total", 0)
                total_s1 += dados_dir.get("s1", 0)
                total_s2 += dados_dir.get("s2", 0)
                total_s2_4x4 += dados_dir.get("s2_4x4", 0)

        print(f"   ✅ Diretorias relevantes: {len(diretorias_relevantes)}")
        print(
            f"   ✅ Total de veículos nas diretorias relevantes: {total_veiculos_relevantes}"
        )
        print(
            f"   ✅ Distribuição: S1={total_s1}, S2={total_s2}, S2_4x4={total_s2_4x4}"
        )

        # Verificar se os números estão corretos
        if (
            total_veiculos_relevantes == 39
            and total_s1 == 3
            and total_s2 == 25
            and total_s2_4x4 == 11
        ):
            print("\n   🎯 DADOS CORRETOS CONFIRMADOS!")
            print("   📊 Base principal atualizada com sucesso!")
        else:
            print("\n   ⚠️  ATENÇÃO: Números não conferem com os esperados")
            print(f"   Esperado: 39 veículos (3 S1 + 25 S2 + 11 S2_4x4)")
            print(
                f"   Encontrado: {total_veiculos_relevantes} veículos ({total_s1} S1 + {total_s2} S2 + {total_s2_4x4} S2_4x4)"
            )

    except Exception as e:
        print(f"   ❌ Erro na verificação: {e}")
        return False

    print("\n✅ ATUALIZAÇÃO DA BASE PRINCIPAL CONCLUÍDA!")
    return True


if __name__ == "__main__":
    sucesso = atualizar_base_principal()
    if sucesso:
        print("\n🔄 Agora todos os scripts do sistema usarão os dados corretos!")
        print("📈 Dashboard e relatórios serão consistentes com a base original.")
    else:
        print("\n❌ Falha na atualização. Verifique os logs acima.")
