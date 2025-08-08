#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para atualizar completamente a dashboard com os dados mais atuais da base central.
"""

import json
import shutil
import os
from datetime import datetime


def rastrear_dados_mais_atuais():
    """Rastreia e identifica os dados mais atuais."""

    print("🔍 RASTREANDO DADOS MAIS ATUAIS")
    print("=" * 50)

    # Arquivos candidatos na ordem de prioridade
    candidatos = [
        "dados/json/dados_veiculos_originais_corretos.json",  # Dados fornecidos pelo usuário
        "dados/json/dados_veiculos_atualizados.json",  # Base principal
        "dados/json/dados_veiculos_corrigidos.json",  # Dados corrigidos
        "dados/json/dados_veiculos_diretorias.json",  # Dados antigos
    ]

    for arquivo in candidatos:
        if os.path.exists(arquivo):
            print(f"✅ Encontrado: {arquivo}")

            # Verificar tamanho e data de modificação
            stat = os.stat(arquivo)
            tamanho = stat.st_size
            modificacao = datetime.fromtimestamp(stat.st_mtime)

            print(f"   📅 Modificado: {modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"   📊 Tamanho: {tamanho:,} bytes")

            # Verificar conteúdo
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)

                if isinstance(dados, dict):
                    if "diretorias" in dados:  # Estrutura do dashboard
                        dados_veiculos = dados["diretorias"]
                        print(f"   🏢 Diretorias: {len(dados_veiculos)}")
                        total_veiculos = sum(
                            d.get("total", 0) for d in dados_veiculos.values()
                        )
                        print(f"   🚗 Total veículos: {total_veiculos}")
                        if "metadata" in dados:
                            print(
                                f"   📋 Metadados: {dados['metadata'].get('fonte', 'N/A')}"
                            )
                    else:  # Estrutura simples
                        total_veiculos = sum(d.get("total", 0) for d in dados.values())
                        print(f"   🏢 Diretorias: {len(dados)}")
                        print(f"   🚗 Total veículos: {total_veiculos}")

            except Exception as e:
                print(f"   ❌ Erro ao ler: {e}")
        else:
            print(f"❌ Não encontrado: {arquivo}")

    return candidatos[
        0
    ]  # dados_veiculos_originais_corretos.json é a fonte mais confiável


def comparar_dados_dashboard():
    """Compara os dados atuais da dashboard com a base central."""

    print(f"\n🔍 COMPARANDO DADOS DA DASHBOARD")
    print("=" * 30)

    # Dados da dashboard (embebidos)
    dados_embebidos = {
        "ANDRADINA": {"s1": 1, "s2": 1, "s2_4x4": 0, "total": 2},
        "AVARE": {"s1": 0, "s2": 2, "s2_4x4": 0, "total": 2},
        "BAURU": {"s1": 0, "s2": 1, "s2_4x4": 1, "total": 2},
        "ITARARE": {"s1": 0, "s2": 2, "s2_4x4": 0, "total": 2},
        "TUPA": {"s1": 0, "s2": 1, "s2_4x4": 0, "total": 1},
        "SANTOS": {"s1": 0, "s2": 1, "s2_4x4": 0, "total": 1},
    }

    # Dados da base central
    try:
        with open(
            "dados/json/dados_veiculos_originais_corretos.json", "r", encoding="utf-8"
        ) as f:
            dados_centrais = json.load(f)

        print("📊 COMPARAÇÃO (amostra):")
        divergencias = 0

        for diretoria, dados_dash in dados_embebidos.items():
            dados_central = dados_centrais.get(diretoria, {})

            if dados_central:
                if dados_dash != dados_central:
                    divergencias += 1
                    print(f"   ⚠️  {diretoria}:")
                    print(
                        f"      Dashboard: Total={dados_dash.get('total', 0)} (S1={dados_dash.get('s1', 0)}, S2={dados_dash.get('s2', 0)}, S2_4x4={dados_dash.get('s2_4x4', 0)})"
                    )
                    print(
                        f"      Central:   Total={dados_central.get('total', 0)} (S1={dados_central.get('s1', 0)}, S2={dados_central.get('s2', 0)}, S2_4x4={dados_central.get('s2_4x4', 0)})"
                    )
                else:
                    print(f"   ✅ {diretoria}: Dados idênticos")
            else:
                print(f"   ❌ {diretoria}: Não encontrado na base central")

        print(f"\n📈 Resultado: {divergencias} divergências encontradas")
        return divergencias > 0

    except Exception as e:
        print(f"❌ Erro ao comparar: {e}")
        return True


def atualizar_dashboard_completa():
    """Atualiza completamente a dashboard com os dados mais atuais."""

    print(f"\n🔄 ATUALIZANDO DASHBOARD COMPLETAMENTE")
    print("=" * 40)

    # 1. Identificar arquivo fonte
    arquivo_fonte = rastrear_dados_mais_atuais()
    print(f"\n📁 Arquivo fonte selecionado: {arquivo_fonte}")

    # 2. Verificar se há divergências
    tem_divergencias = comparar_dados_dashboard()

    if not tem_divergencias:
        print(f"\n✅ Dashboard já está atualizada!")
        return True

    # 3. Carregar dados corretos
    try:
        with open(arquivo_fonte, "r", encoding="utf-8") as f:
            dados_corretos = json.load(f)
        print(f"✅ Dados corretos carregados: {len(dados_corretos)} diretorias")
    except Exception as e:
        print(f"❌ Erro ao carregar dados corretos: {e}")
        return False

    # 4. Criar backup da dashboard atual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"dashboard/dashboard_integrado_backup_{timestamp}.html"
    shutil.copy2("dashboard/dashboard_integrado.html", backup_file)
    print(f"💾 Backup criado: {backup_file}")

    # 5. Extrair diretorias relevantes (que têm escolas)
    try:
        with open(
            "dados/json/dados_escolas_atualizados.json", "r", encoding="utf-8"
        ) as f:
            escolas = json.load(f)

        diretorias_relevantes = list(set(escola["diretoria"] for escola in escolas))
        print(f"🏫 Diretorias com escolas: {len(diretorias_relevantes)}")

        # Mapear nomes
        mapeamento = {
            "Andradina": "ADAMANTINA",
            "Apiai": "BOTUCATU",
            "Avare": "BOTUCATU",
            "Bauru": "BAURU",
            "Caraguatatuba": "CARAPICUÍBA",
            "Itapeva": "BOTUCATU",
            "Itarare": "ITARARÉ",
            "Lins": "ARARAQUARA",
            "Miracatu": "ITAPECERICA DA SERRA",
            "Mirante do Paranapanema": "PRESIDENTE PRUDENTE",
            "Norte 1": "GUARULHOS NORTE",
            "Penapolis": "ARAÇATUBA",
            "Registro": "ITAPECERICA DA SERRA",
            "Santo Anastacio": "PRESIDENTE PRUDENTE",
            "Santos": "SANTOS",
            "Sao Bernardo do Campo": "DIADEMA",
            "Sul 3": "GUARULHOS SUL",
            "SÃO VICENTE": "SANTOS",
            "Tupa": "TUPÃ",
        }

    except Exception as e:
        print(f"❌ Erro ao carregar escolas: {e}")
        return False

    # 6. Atualizar arquivo JSON da dashboard
    try:
        # Calcular totais
        total_veiculos = sum(d.get("total", 0) for d in dados_corretos.values())

        # Calcular veículos em diretorias relevantes
        veiculos_relevantes = 0
        s1_relevantes = 0
        s2_relevantes = 0
        s2_4x4_relevantes = 0

        for diretoria_escola in diretorias_relevantes:
            diretoria_veiculo = mapeamento.get(
                diretoria_escola, diretoria_escola.upper()
            )
            if diretoria_veiculo in dados_corretos:
                dados = dados_corretos[diretoria_veiculo]
                veiculos_relevantes += dados.get("total", 0)
                s1_relevantes += dados.get("s1", 0)
                s2_relevantes += dados.get("s2", 0)
                s2_4x4_relevantes += dados.get("s2_4x4", 0)

        # Estrutura atualizada para o dashboard
        dados_dashboard_atualizados = {
            "metadata": {
                "total_veiculos": total_veiculos,
                "total_diretorias": len(dados_corretos),
                "diretorias_relevantes": len(diretorias_relevantes),
                "veiculos_relevantes": veiculos_relevantes,
                "distribuicao_relevantes": {
                    "s1": s1_relevantes,
                    "s2": s2_relevantes,
                    "s2_4x4": s2_4x4_relevantes,
                },
                "data_atualizacao": datetime.now().strftime("%d/%m/%Y - %H:%M"),
                "fonte": arquivo_fonte.split("/")[-1],
            },
            "diretorias": dados_corretos,
        }

        # Salvar arquivo JSON atualizado
        with open(
            "dashboard/dados_veiculos_diretorias.json", "w", encoding="utf-8"
        ) as f:
            json.dump(dados_dashboard_atualizados, f, indent=2, ensure_ascii=False)

        print(f"✅ JSON da dashboard atualizado")
        print(f"   📊 Total de veículos: {total_veiculos}")
        print(f"   📊 Veículos relevantes: {veiculos_relevantes}")

    except Exception as e:
        print(f"❌ Erro ao atualizar JSON: {e}")
        return False

    # 7. Atualizar dados embebidos no HTML
    try:
        with open("dashboard/dashboard_integrado.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        # Extrair apenas as diretorias com escolas para os dados embebidos
        dados_embebidos_atualizados = {}
        for diretoria_escola in diretorias_relevantes:
            diretoria_veiculo = mapeamento.get(
                diretoria_escola, diretoria_escola.upper()
            )
            if diretoria_veiculo in dados_corretos:
                # Usar o nome como aparece nas escolas para consistência
                chave = diretoria_veiculo
                dados_embebidos_atualizados[chave] = dados_corretos[diretoria_veiculo]

        # Construir string dos dados embebidos
        dados_str = "        vehicleData = {\n"
        for diretoria, dados in dados_embebidos_atualizados.items():
            dados_str += f'          "{diretoria}": {{"s1": {dados.get("s1", 0)}, "s2": {dados.get("s2", 0)}, "s2_4x4": {dados.get("s2_4x4", 0)}, "total": {dados.get("total", 0)}}},\n'
        dados_str = dados_str.rstrip(",\n") + "\n        };"

        # Atualizar metadados embebidos
        html_content = html_content.replace(
            '"total_veiculos": 245,', f'"total_veiculos": {total_veiculos},'
        )

        # Atualizar header com novos totais
        html_content = html_content.replace(
            "- Veículos: dados_veiculos_diretorias.json (245 veículos distribuídos)",
            f"- Veículos: dados_veiculos_diretorias.json ({total_veiculos} veículos distribuídos)",
        )

        # Atualizar data
        data_atual = datetime.now().strftime("%d/%m/%Y - %H:%M")
        import re

        html_content = re.sub(
            r"Data da última atualização: \d{2}/\d{2}/\d{4} - \d{2}:\d{2}",
            f"Data da última atualização: {data_atual}",
            html_content,
        )

        # Atualizar dados embebidos
        padrao_dados = r"vehicleData = \{[^}]*\};"
        html_content = re.sub(padrao_dados, dados_str, html_content, flags=re.DOTALL)

        # Salvar HTML atualizado
        with open("dashboard/dashboard_integrado.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ HTML da dashboard atualizado")
        print(f"   📊 Dados embebidos: {len(dados_embebidos_atualizados)} diretorias")
        print(f"   📅 Data atualizada: {data_atual}")

    except Exception as e:
        print(f"❌ Erro ao atualizar HTML: {e}")
        return False

    print(f"\n🎉 DASHBOARD COMPLETAMENTE ATUALIZADA!")
    print(f"📁 Fonte dos dados: {arquivo_fonte}")
    print(f"💾 Backup salvo em: {backup_file}")
    print(f"🌐 Dashboard: dashboard/dashboard_integrado.html")

    return True


if __name__ == "__main__":
    sucesso = atualizar_dashboard_completa()
    if sucesso:
        print(f"\n✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"🔄 A dashboard agora usa os dados mais atuais da base central.")
    else:
        print(f"\n❌ FALHA NA ATUALIZAÇÃO!")
        print(f"🔍 Verifique os logs acima para detalhes do erro.")
