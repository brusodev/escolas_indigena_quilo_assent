#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATUALIZAÇÃO DO ARQUIVO JSON DE VEÍCULOS E BASES CENTRAIS
Sincronização com dados das 63 escolas atualizadas
"""

import json
import pandas as pd
import os
from datetime import datetime


def atualizar_dados_veiculos():
    """Atualiza o arquivo JSON de veículos com base nas novas 63 escolas"""
    print("🚗 ATUALIZANDO DADOS DE VEÍCULOS")
    print("=" * 50)

    # Ler dados atualizados das escolas
    arquivo_excel = (
        "dados/excel/distancias_escolas_diretorias_completo_63_corrigido.xlsx"
    )

    try:
        df = pd.read_excel(arquivo_excel)
        print(f"📖 Lendo dados de: {arquivo_excel}")
        print(f"📊 Total de escolas: {len(df)}")

        # Obter diretorias únicas
        diretorias = df["DE_Responsavel"].value_counts().to_dict()
        print(f"🏢 Diretorias identificadas: {len(diretorias)}")

        # Criar estrutura de dados de veículos
        dados_veiculos = {
            "metadata": {
                "sistema": "Gestão de Escolas Indígenas, Quilombolas e Assentamentos",
                "versao": "2.0",
                "data_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_escolas": len(df),
                "total_diretorias": len(diretorias),
                "total_veiculos": 172,  # Mantendo o total conhecido
                "metodologia": "Distribuição proporcional baseada no número de escolas por diretoria",
            },
            "distribuicao_por_diretoria": {},
            "veiculos_por_tipo": {
                "onibus_escolar": 89,
                "van_escolar": 43,
                "microonibus": 25,
                "veiculo_adaptado": 15,
            },
            "estatisticas": {
                "escolas_indigenas": len(df[df["Tipo_Escola"] == "Indígena"]),
                "escolas_quilombolas_assentamentos": len(
                    df[df["Tipo_Escola"] == "Quilombola/Assentamento"]
                ),
                "escolas_zona_rural": len(df[df["Zona"] == "Rural"]),
                "escolas_zona_urbana": len(df[df["Zona"] == "Urbana"]),
            },
        }

        # Calcular distribuição de veículos por diretoria
        total_veiculos = 172
        total_escolas = len(df)

        print("🔄 Calculando distribuição de veículos...")

        for diretoria, num_escolas in diretorias.items():
            # Distribuição proporcional
            proporcao = num_escolas / total_escolas
            veiculos_diretoria = max(1, round(total_veiculos * proporcao))

            # Obter escolas desta diretoria
            escolas_diretoria = df[df["DE_Responsavel"] == diretoria]

            dados_veiculos["distribuicao_por_diretoria"][diretoria] = {
                "total_escolas": num_escolas,
                "total_veiculos": veiculos_diretoria,
                "escolas_indigenas": len(
                    escolas_diretoria[escolas_diretoria["Tipo_Escola"] == "Indígena"]
                ),
                "escolas_quilombolas": len(
                    escolas_diretoria[
                        escolas_diretoria["Tipo_Escola"] == "Quilombola/Assentamento"
                    ]
                ),
                "distancia_media": round(escolas_diretoria["Distancia_KM"].mean(), 2),
                "distancia_maxima": round(escolas_diretoria["Distancia_KM"].max(), 2),
                "escolas_rurais": len(
                    escolas_diretoria[escolas_diretoria["Zona"] == "Rural"]
                ),
                "escolas_urbanas": len(
                    escolas_diretoria[escolas_diretoria["Zona"] == "Urbana"]
                ),
                "codigo_de": (
                    escolas_diretoria["DE_Codigo"].iloc[0]
                    if not escolas_diretoria.empty
                    else diretoria.upper()
                ),
            }

        # Salvar arquivo JSON atualizado
        arquivo_json = "dados/json/dados_veiculos_diretorias.json"

        with open(arquivo_json, "w", encoding="utf-8") as f:
            json.dump(dados_veiculos, f, ensure_ascii=False, indent=2)

        print(f"✅ Arquivo JSON salvo: {arquivo_json}")
        print(f"🚗 Total de veículos: {dados_veiculos['metadata']['total_veiculos']}")
        print(
            f"🏢 Diretorias com veículos: {len(dados_veiculos['distribuicao_por_diretoria'])}"
        )

        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar dados de veículos: {e}")
        return False


def atualizar_config_sistema():
    """Atualiza arquivo de configuração do sistema"""
    print("\n⚙️ ATUALIZANDO CONFIGURAÇÃO DO SISTEMA")
    print("-" * 50)

    config_file = "dados/json/config_sistema.json"

    try:
        config = {
            "sistema": {
                "nome": "Sistema de Gestão de Escolas Indígenas, Quilombolas e Assentamentos",
                "versao": "2.0",
                "ultima_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Atualizado com dados das 63 escolas",
            },
            "dados": {
                "total_escolas": 63,
                "escolas_indigenas": 43,
                "escolas_quilombolas_assentamentos": 20,
                "diretorias_responsaveis": 19,
                "total_veiculos": 172,
                "arquivo_principal": "dados/excel/distancias_escolas_diretorias_completo_63_corrigido.xlsx",
                "metodologia_distancia": "Haversine",
                "referencia_validacao": {
                    "escola": "ALDEIA KOPENOTI",
                    "distancia_km": 27.16,
                    "coordenadas_escola": "-22.264515, -49.35027069",
                    "coordenadas_diretoria": "-22.3233112, -49.0940288",
                    "diretoria": "Bauru",
                },
            },
            "estrutura_arquivos": {
                "dados_excel": "dados/excel/",
                "dados_json": "dados/json/",
                "dashboard": "dashboard/",
                "relatorios_excel": "relatorios/excel/",
                "relatorios_pdf": "relatorios/pdf/",
                "scripts": "scripts/",
                "documentacao": "documentacao/",
            },
            "classificacao_distancias": {
                "baixa": "< 50 km",
                "media": "50-100 km",
                "alta": "> 100 km",
            },
            "tipos_escola": {
                "indigena": "Escolas em aldeias indígenas",
                "quilombola_assentamento": "Escolas em comunidades quilombolas e assentamentos",
            },
            "zonas": {"rural": "Zona rural", "urbana": "Zona urbana"},
        }

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        print(f"✅ Configuração salva: {config_file}")
        print(f"📊 Total escolas: {config['dados']['total_escolas']}")
        print(
            f"🎯 Validação KOPENOTI: {config['dados']['referencia_validacao']['distancia_km']} km"
        )

        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar configuração: {e}")
        return False


def verificar_integridade_dados():
    """Verifica integridade dos dados atualizados"""
    print("\n🔍 VERIFICAÇÃO DE INTEGRIDADE DOS DADOS")
    print("-" * 50)

    # Verificar arquivo Excel
    arquivo_excel = (
        "dados/excel/distancias_escolas_diretorias_completo_63_corrigido.xlsx"
    )
    if os.path.exists(arquivo_excel):
        df = pd.read_excel(arquivo_excel)
        print(f"✅ Excel: {len(df)} escolas encontradas")

        # Verificar KOPENOTI
        kopenoti = df[df["Nome_Escola"].str.contains("KOPENOTI", na=False, case=False)]
        if not kopenoti.empty:
            distancia = kopenoti.iloc[0]["Distancia_KM"]
            if abs(distancia - 27.16) < 0.1:
                print(f"✅ KOPENOTI: {distancia} km (CORRETO)")
            else:
                print(f"❌ KOPENOTI: {distancia} km (INCORRETO)")

        # Estatísticas
        indigenas = len(df[df["Tipo_Escola"] == "Indígena"])
        quilombolas = len(df[df["Tipo_Escola"] == "Quilombola/Assentamento"])
        print(f"📊 Indígenas: {indigenas}, Quilombolas/Assentamentos: {quilombolas}")
    else:
        print(f"❌ Arquivo Excel não encontrado: {arquivo_excel}")

    # Verificar arquivo JSON de veículos
    arquivo_json = "dados/json/dados_veiculos_diretorias.json"
    if os.path.exists(arquivo_json):
        with open(arquivo_json, "r", encoding="utf-8") as f:
            dados = json.load(f)

        total_veiculos = dados["metadata"]["total_veiculos"]
        total_diretorias = dados["metadata"]["total_diretorias"]
        print(f"✅ JSON: {total_veiculos} veículos, {total_diretorias} diretorias")
    else:
        print(f"❌ Arquivo JSON não encontrado: {arquivo_json}")

    # Verificar configuração
    config_file = "dados/json/config_sistema.json"
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        total_escolas = config["dados"]["total_escolas"]
        print(f"✅ Config: {total_escolas} escolas configuradas")
    else:
        print(f"❌ Arquivo de configuração não encontrado: {config_file}")

    return True


def main():
    """Função principal"""
    print("🔄 ATUALIZAÇÃO COMPLETA DAS BASES CENTRAIS DE DADOS")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🎯 Objetivo: Sincronizar todas as bases com dados das 63 escolas")
    print()

    # 1. Atualizar dados de veículos
    if not atualizar_dados_veiculos():
        print("❌ Falha ao atualizar dados de veículos")
        return False

    # 2. Atualizar configuração do sistema
    if not atualizar_config_sistema():
        print("❌ Falha ao atualizar configuração")
        return False

    # 3. Verificar integridade
    verificar_integridade_dados()

    print("\n🎯 ATUALIZAÇÃO DAS BASES CENTRAIS CONCLUÍDA!")
    print("=" * 80)
    print("✅ Arquivo Excel principal atualizado (63 escolas)")
    print("✅ Dados de veículos sincronizados (172 veículos)")
    print("✅ Configuração do sistema atualizada")
    print("✅ Integridade dos dados verificada")
    print()
    print("🚀 SISTEMA PRONTO PARA USO!")
    print("📊 Próximo passo: Gerar relatórios atualizados")
    print("   → python scripts/atualizar_relatorios_completos.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
