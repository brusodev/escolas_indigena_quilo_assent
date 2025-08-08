# -*- coding: utf-8 -*-
import pandas as pd
import json
import numpy as np


def revisar_planilha_veiculos():
    """Revisa a planilha de veículos e identifica problemas de dados"""
    print("🔍 REVISANDO PLANILHA DE VEÍCULOS...")
    print("=" * 60)

    try:
        # Carregar a planilha
        df = pd.read_excel("QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx")

        print(f"📊 Dados carregados: {len(df)} linhas")
        print(f"📋 Colunas: {list(df.columns)}")

        # Verificar dados ausentes ou problemáticos
        print("\n❌ PROBLEMAS IDENTIFICADOS:")
        print("=" * 40)

        # 1. Verificar valores nulos
        for col in df.columns:
            nulos = df[col].isnull().sum()
            if nulos > 0:
                print(f"⚠️  Coluna '{col}': {nulos} valores nulos")
                # Mostrar linhas com valores nulos
                linhas_nulas = df[df[col].isnull()]['DIRETORIA'].tolist()
                print(
                    f"   Diretorias afetadas: {linhas_nulas[:5]}{'...' if len(linhas_nulas) > 5 else ''}")

        # 2. Verificar valores não numéricos nas colunas de quantidade
        colunas_numericas = ['QUANTIDADE S-1',
                             'QUANTIDADE S-2', 'QUANTIDADE S-2 4X4']

        for col in colunas_numericas:
            if col in df.columns:
                # Tentar converter para numérico e identificar problemas
                problemas = []
                for idx, valor in enumerate(df[col]):
                    try:
                        if pd.isna(valor):
                            problemas.append(
                                f"Linha {idx+2}: '{df.iloc[idx]['DIRETORIA']}' = NaN")
                        else:
                            float(valor)  # Tenta converter
                    except (ValueError, TypeError):
                        problemas.append(
                            f"Linha {idx+2}: '{df.iloc[idx]['DIRETORIA']}' = '{valor}'")

                if problemas:
                    print(f"\n🚨 Problemas na coluna '{col}':")
                    # Mostrar só os primeiros 10
                    for problema in problemas[:10]:
                        print(f"   {problema}")
                    if len(problemas) > 10:
                        print(f"   ... e mais {len(problemas) - 10} problemas")

        # 3. Verificar espaços extras nos nomes das colunas
        print(f"\n📝 DETALHES DAS COLUNAS:")
        for i, col in enumerate(df.columns):
            print(f"   {i+1}. '{col}' (comprimento: {len(col)})")
            if col != col.strip():
                print(f"      ⚠️  Contém espaços extras!")

        # 4. Mostrar algumas linhas com problemas
        print(f"\n📋 PRIMEIRAS 10 LINHAS:")
        print(df.head(10).to_string())

        # 5. Verificar diretorias específicas mencionadas
        diretorias_problema = ['ITARARE', 'ITARARÉ']
        print(f"\n🔍 VERIFICANDO DIRETORIAS ESPECÍFICAS:")
        for diretoria in diretorias_problema:
            matches = df[df['DIRETORIA'].str.contains(
                diretoria, case=False, na=False)]
            if not matches.empty:
                print(f"\n📍 Diretoria '{diretoria}':")
                for idx, row in matches.iterrows():
                    print(f"   Linha {idx+2}: {row['DIRETORIA']}")
                    for col in colunas_numericas:
                        if col in df.columns:
                            valor = row[col]
                            print(
                                f"      {col}: {valor} (tipo: {type(valor)})")

        # 6. Estatísticas por coluna
        print(f"\n📊 ESTATÍSTICAS POR COLUNA:")
        for col in colunas_numericas:
            if col in df.columns:
                # Contar diferentes tipos de valores
                valores_validos = df[col].dropna()
                nulos = df[col].isnull().sum()
                zeros = (df[col] == 0).sum()
                positivos = (df[col] > 0).sum()

                print(f"\n   {col}:")
                print(f"      Valores válidos: {len(valores_validos)}")
                print(f"      Valores nulos: {nulos}")
                print(f"      Valores zero: {zeros}")
                print(f"      Valores positivos: {positivos}")

                if len(valores_validos) > 0:
                    print(f"      Mínimo: {valores_validos.min()}")
                    print(f"      Máximo: {valores_validos.max()}")
                    print(f"      Soma total: {valores_validos.sum()}")

        return df

    except Exception as e:
        print(f"❌ Erro ao revisar planilha: {e}")
        return None


def normalizar_dados_veiculos(df):
    """Normaliza os dados da planilha de veículos"""
    print(f"\n🔧 NORMALIZANDO DADOS...")
    print("=" * 40)

    if df is None:
        print("❌ DataFrame não disponível para normalização")
        return None

    # Fazer uma cópia para não alterar o original
    df_normalizado = df.copy()

    # 1. Normalizar nomes das colunas (remover espaços extras)
    print("📝 Normalizando nomes das colunas...")
    colunas_antigas = list(df_normalizado.columns)
    df_normalizado.columns = [col.strip() for col in df_normalizado.columns]

    for i, (antiga, nova) in enumerate(zip(colunas_antigas, df_normalizado.columns)):
        if antiga != nova:
            print(f"   Coluna {i+1}: '{antiga}' → '{nova}'")

    # 2. Normalizar valores das colunas numéricas
    colunas_numericas = ['QUANTIDADE S-1',
                         'QUANTIDADE S-2', 'QUANTIDADE S-2 4X4']

    for col in colunas_numericas:
        if col in df_normalizado.columns:
            print(f"\n🔢 Normalizando coluna '{col}'...")

            # Substituir valores nulos por 0
            valores_nulos_antes = df_normalizado[col].isnull().sum()
            df_normalizado[col] = df_normalizado[col].fillna(0)

            # Converter para numérico, forçando erros para 0
            valores_problematicos = []
            for idx, valor in enumerate(df_normalizado[col]):
                try:
                    df_normalizado.loc[idx, col] = float(valor)
                except (ValueError, TypeError):
                    valores_problematicos.append(
                        f"{df_normalizado.iloc[idx]['DIRETORIA']}: '{valor}'")
                    df_normalizado.loc[idx, col] = 0

            # Garantir que são inteiros (não float)
            df_normalizado[col] = df_normalizado[col].astype(int)

            valores_nulos_depois = (df_normalizado[col] == 0).sum()

            print(f"   ✅ Valores nulos corrigidos: {valores_nulos_antes}")
            if valores_problematicos:
                print(
                    f"   ⚠️  Valores problemáticos corrigidos: {len(valores_problematicos)}")
                for problema in valores_problematicos[:5]:
                    print(f"      {problema}")
            print(
                f"   📊 Total de zeros após normalização: {valores_nulos_depois}")

    # 3. Verificar e normalizar nomes de diretorias
    print(f"\n📍 Normalizando nomes de diretorias...")

    # Remover espaços extras dos nomes
    df_normalizado['DIRETORIA'] = df_normalizado['DIRETORIA'].str.strip()

    # Verificar duplicatas ou inconsistências
    diretorias_unicas = df_normalizado['DIRETORIA'].nunique()
    diretorias_total = len(df_normalizado)

    print(f"   📊 Diretorias únicas: {diretorias_unicas}")
    print(f"   📊 Total de linhas: {diretorias_total}")

    if diretorias_unicas != diretorias_total:
        print("   ⚠️  Possíveis duplicatas detectadas!")
        duplicatas = df_normalizado['DIRETORIA'].value_counts()
        duplicatas = duplicatas[duplicatas > 1]
        if len(duplicatas) > 0:
            print("   🔍 Diretorias duplicadas:")
            for diretoria, count in duplicatas.items():
                print(f"      {diretoria}: {count} ocorrências")

    # 4. Salvar dados normalizados
    print(f"\n💾 Salvando dados normalizados...")

    arquivo_normalizado = "QUANTIDADE_VEICULOS_NORMALIZADO.xlsx"
    df_normalizado.to_excel(arquivo_normalizado, index=False)
    print(f"   ✅ Arquivo salvo: {arquivo_normalizado}")

    # 5. Criar JSON normalizado
    veiculos_normalizados = {}
    for _, row in df_normalizado.iterrows():
        diretoria = row["DIRETORIA"]
        s1 = int(row.get("QUANTIDADE S-1", 0))
        s2 = int(row.get("QUANTIDADE S-2", 0))
        s2_4x4 = int(row.get("QUANTIDADE S-2 4X4", 0))
        total = s1 + s2 + s2_4x4

        veiculos_normalizados[diretoria.upper()] = {
            "total": total,
            "s1": s1,
            "s2": s2,
            "s2_4x4": s2_4x4,
            "diretoria_original": diretoria,
        }

    with open("dados_veiculos_normalizados.json", "w", encoding="utf-8") as f:
        json.dump(veiculos_normalizados, f, ensure_ascii=False, indent=2)

    print(f"   ✅ JSON normalizado salvo: dados_veiculos_normalizados.json")

    # 6. Relatório de normalização
    print(f"\n📋 RELATÓRIO DE NORMALIZAÇÃO:")
    print("=" * 50)

    total_veiculos = sum(v["total"] for v in veiculos_normalizados.values())
    diretorias_com_veiculos = sum(
        1 for v in veiculos_normalizados.values() if v["total"] > 0)

    print(f"✅ {len(df_normalizado)} diretorias processadas")
    print(f"🚗 {total_veiculos} veículos totais")
    print(f"📍 {diretorias_com_veiculos} diretorias com veículos")
    print(
        f"⭕ {len(df_normalizado) - diretorias_com_veiculos} diretorias sem veículos")

    return df_normalizado


if __name__ == "__main__":
    df = revisar_planilha_veiculos()
    if df is not None:
        df_normalizado = normalizar_dados_veiculos(df)
        print(f"\n✅ REVISÃO E NORMALIZAÇÃO CONCLUÍDA!")
    else:
        print(f"\n❌ Não foi possível completar a revisão")
