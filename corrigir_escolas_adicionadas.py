#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrigir dados das 4 escolas adicionadas com informações originais
"""

import pandas as pd


def corrigir_dados_escolas_adicionadas():
    """Corrige os dados das 4 escolas com informações originais"""
    print("🔧 CORRIGINDO DADOS DAS ESCOLAS ADICIONADAS")
    print("=" * 60)

    try:
        # Carregar arquivo atual
        df = pd.read_excel("distancias_escolas_diretorias_completo_63.xlsx")
        print(f"📋 Arquivo atual: {len(df)} escolas")

        # Dados originais das escolas
        correções = {
            "BAIRRO DE BOMBAS": {
                "Endereco_Escola": "BAIRRO BOMBAS DE BAIXO SN",
                "Zona": 2,
                "Latitude_Escola": -24.60935974,
                "Longitude_Escola": -48.65967178,
                "DE_Responsavel": "Apiai",
                "Nome_Diretoria": "Apiai",
            },
            "BAIRRO BOMBAS DE CIMA": {
                "Endereco_Escola": "BAIRRO BOMBAS DE CIMA SN",
                "Zona": 2,
                "Latitude_Escola": -24.60933304,
                "Longitude_Escola": -48.65969086,
                "DE_Responsavel": "Apiai",
                "Nome_Diretoria": "Apiai",
            },
            "FAZENDA DA CAIXA": {
                "Endereco_Escola": "CASA DA FARINHA S/N",
                "Zona": 2,
                "Latitude_Escola": -23.34110069,
                "Longitude_Escola": -44.83760834,
                "DE_Responsavel": "Caraguatatuba",
                "Nome_Diretoria": "Caraguatatuba",
            },
            "MARIA ANTONIA CHULES PRINCS": {
                "Endereco_Escola": "BENEDITO PASCOAL DE FRANCA KM 37 KM 111",
                "Zona": 2,
                "Latitude_Escola": -24.60128975,
                "Longitude_Escola": -48.40626144,
                "DE_Responsavel": "Registro",
                "Nome_Diretoria": "Registro",
            },
        }

        # Aplicar correções
        escolas_corrigidas = 0
        for nome_escola, dados in correções.items():
            # Encontrar a escola
            mask = df["Nome_Escola"].str.contains(nome_escola, na=False, case=False)
            indices = df[mask].index

            if len(indices) > 0:
                idx = indices[0]
                print(f"✅ Corrigindo: {nome_escola}")

                # Aplicar dados
                for campo, valor in dados.items():
                    df.at[idx, campo] = valor
                    print(f"   {campo}: {valor}")

                escolas_corrigidas += 1
            else:
                print(f"❌ Escola não encontrada: {nome_escola}")

        print(f"\n📊 Total de escolas corrigidas: {escolas_corrigidas}")

        # Completar dados de diretorias para Apiai (que não existia antes)
        print("\n🔍 COMPLETANDO DADOS DA DIRETORIA APIAI")

        # Dados da diretoria Apiai (estimados com base na localização)
        dados_apiai = {
            "Cidade_Diretoria": "APIAI",
            "Endereco_Diretoria": "APIAI - SP",
            "Latitude_Diretoria": -24.51111,  # Coordenadas aproximadas de Apiai
            "Longitude_Diretoria": -48.84222,
        }

        # Aplicar dados da diretoria Apiai para as duas escolas
        mask_apiai = df["Nome_Diretoria"] == "Apiai"
        for campo, valor in dados_apiai.items():
            df.loc[mask_apiai, campo] = valor

        escolas_apiai = df[mask_apiai]
        print(f"   ✅ Completados dados para {len(escolas_apiai)} escolas em Apiai")

        # Verificar valores NaN na coluna Zona
        zona_nan = df["Zona"].isna().sum()
        if zona_nan > 0:
            print(f"\n⚠️  Corrigindo {zona_nan} valores NaN na coluna Zona")
            df["Zona"] = df["Zona"].fillna(2)  # Preencher com 2 (rural)

        # Salvar arquivo corrigido
        nome_arquivo = "distancias_escolas_diretorias_completo_63_corrigido.xlsx"
        df.to_excel(nome_arquivo, index=False)
        print(f"\n💾 Arquivo salvo: {nome_arquivo}")

        # Verificações finais
        print(f"\n🎯 VERIFICAÇÕES FINAIS:")
        print(f"   📊 Total de escolas: {len(df)}")
        print(f"   🔍 Valores NaN em Zona: {df['Zona'].isna().sum()}")
        print(f"   🏢 Diretorias únicas: {df['Nome_Diretoria'].nunique()}")

        # Verificar KOPENOTI
        kopenoti = df[df["Nome_Escola"].str.contains("KOPENOTI", na=False, case=False)]
        if not kopenoti.empty:
            distancia = kopenoti.iloc[0]["Distancia_KM"]
            print(f"   🎯 KOPENOTI: {distancia:.2f} km")

        print(f"\n✅ CORREÇÃO CONCLUÍDA COM SUCESSO!")
        return df

    except Exception as e:
        print(f"❌ Erro ao corrigir dados: {e}")
        return None


def atualizar_scripts_para_arquivo_corrigido():
    """Atualiza os scripts para usar o arquivo corrigido"""
    print("\n🔄 ATUALIZANDO SCRIPTS PARA ARQUIVO CORRIGIDO")
    print("=" * 60)

    arquivos_para_atualizar = [
        "gerar_relatorio_excel.py",
        "gerar_relatorio_pdf.py",
        "atualizar_relatorios_completos.py",
    ]

    arquivo_antigo = "distancias_escolas_diretorias_completo_63.xlsx"
    arquivo_novo = "distancias_escolas_diretorias_completo_63_corrigido.xlsx"

    for arquivo in arquivos_para_atualizar:
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                content = f.read()

            if arquivo_antigo in content:
                content = content.replace(arquivo_antigo, arquivo_novo)

                with open(arquivo, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"   ✅ Atualizado: {arquivo}")
            else:
                print(f"   ⚠️  Não encontrado em: {arquivo}")

        except Exception as e:
            print(f"   ❌ Erro em {arquivo}: {e}")


def main():
    """Função principal"""
    print("🚀 CORREÇÃO DE DADOS DAS ESCOLAS ADICIONADAS")
    print("=" * 70)

    # Corrigir dados
    df = corrigir_dados_escolas_adicionadas()

    if df is not None:
        # Atualizar scripts
        atualizar_scripts_para_arquivo_corrigido()

        print(f"\n🎯 PRÓXIMOS PASSOS:")
        print(f"   1. ✅ Dados das 4 escolas corrigidos com informações originais")
        print(f"   2. ✅ Scripts atualizados para o novo arquivo")
        print(f"   3. 🔄 Execute: python atualizar_relatorios_completos.py")
        print(f"   4. 🎯 Verifique se todos os relatórios agora têm 63 escolas")


if __name__ == "__main__":
    main()
