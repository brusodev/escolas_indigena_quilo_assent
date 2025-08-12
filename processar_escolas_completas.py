#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROCESSADOR DE ESCOLAS CITEM - GERAÇÃO DE JSONs POR TIPO
=======================================================

Este script processa a base completa de escolas do CITEM e gera
arquivos JSON separados por tipo de escola (TIPOESC).

Dados: 5.582 escolas totais
Fonte: ENDERECO_ESCOLAS_062025 (1).csv
Output: JSONs organizados por tipo de escola

Autor: Sistema Dashboard Escolas
Data: 11/08/2025
"""

import pandas as pd
import json
import os
from pathlib import Path

# Mapeamento dos tipos de escola conforme metadados CITEM
TIPOS_ESCOLA = {
    3: "CEEJA",
    6: "CEL_JTO", 
    7: "HOSPITALAR",
    8: "REGULAR",
    9: "CENTRO_ATEND_SOCIOEDUC",
    10: "INDIGENA",
    15: "ESCOLA_PENITENCIARIA",
    31: "ASSENTAMENTO", 
    34: "CENTRO_ATEND_SOC_EDUC_ADOLESC",
    36: "QUILOMBOLA"
}

def processar_escolas_citem():
    """
    Processa o CSV completo e gera JSONs por tipo de escola
    """
    print("🏫 PROCESSADOR DE ESCOLAS CITEM - INICIANDO...")
    print("=" * 60)
    
    # Caminhos dos arquivos
    csv_path = "dados/ENDERECO_ESCOLAS_062025 (1).csv"
    output_dir = "dados/json/por_tipo"
    
    # Criar diretório de saída se não existir
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # Ler CSV com encoding correto - tentar diferentes encodings
        print(f"📊 Lendo arquivo: {csv_path}")
        
        # Lista de encodings para tentar
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                print(f"🔄 Tentando encoding: {encoding}")
                df = pd.read_csv(csv_path, sep=';', encoding=encoding)
                print(f"✅ Sucesso com encoding: {encoding}")
                break
            except UnicodeDecodeError:
                print(f"❌ Falhou com encoding: {encoding}")
                continue
        
        if df is None:
            raise Exception("Não foi possível ler o arquivo com nenhum encoding testado")
        
        print(f"✅ Total de registros lidos: {len(df):,}")
        print(f"📋 Colunas encontradas: {list(df.columns)}")
        
        # Verificar tipos de escola únicos
        tipos_unicos = df['TIPOESC'].unique()
        print(f"🏷️ Tipos de escola encontrados: {sorted(tipos_unicos)}")
        
        # Estatísticas por tipo
        print("\n📈 ESTATÍSTICAS POR TIPO DE ESCOLA:")
        print("-" * 40)
        
        estatisticas = {}
        
        for tipo_codigo in sorted(tipos_unicos):
            tipo_nome = TIPOS_ESCOLA.get(tipo_codigo, f"TIPO_{tipo_codigo}")
            quantidade = len(df[df['TIPOESC'] == tipo_codigo])
            
            print(f"{tipo_codigo:2d} - {tipo_nome:<30} : {quantidade:,} escolas")
            estatisticas[tipo_codigo] = {
                "nome": tipo_nome,
                "quantidade": quantidade
            }
        
        # Processar cada tipo de escola
        print("\n🔄 PROCESSANDO ARQUIVOS JSON POR TIPO...")
        print("-" * 50)
        
        total_processadas = 0
        
        for tipo_codigo in sorted(tipos_unicos):
            tipo_nome = TIPOS_ESCOLA.get(tipo_codigo, f"TIPO_{tipo_codigo}")
            
            # Filtrar escolas deste tipo
            escolas_tipo = df[df['TIPOESC'] == tipo_codigo].copy()
            
            # Converter para formato JSON padronizado
            escolas_json = []
            
            for _, escola in escolas_tipo.iterrows():
                # Função auxiliar para limpar strings
                def limpar_string(valor):
                    if pd.isna(valor):
                        return ""
                    return str(valor).strip()
                
                def limpar_numero(valor):
                    if pd.isna(valor):
                        return None
                    try:
                        return int(valor)
                    except:
                        return None
                
                def limpar_float(valor):
                    if pd.isna(valor):
                        return None
                    try:
                        # Tratar coordenadas com vírgula como separador decimal
                        valor_str = str(valor).strip().replace(',', '.')
                        return float(valor_str)
                    except:
                        return None
                
                escola_obj = {
                    "codigo": limpar_numero(escola['COD_ESC']),
                    "codigo_mec": limpar_string(escola['CODESCMEC']),
                    "nome": limpar_string(escola['NOMESC']),
                    "tipo_codigo": int(escola['TIPOESC']),
                    "tipo_nome": tipo_nome,
                    "endereco": {
                        "logradouro": limpar_string(escola['ENDESC']),
                        "numero": limpar_string(escola['NUMESC']),
                        "complemento": limpar_string(escola['COMPLEMENTO']),
                        "cep": limpar_string(escola['CEP']),
                        "bairro": limpar_string(escola['BAIESC']),
                        "zona": "Rural" if escola['ZONA'] == 2 else "Urbana"
                    },
                    "localizacao": {
                        "municipio": limpar_string(escola['MUN']),
                        "distrito": limpar_string(escola['DISTR']),
                        "codigo_ibge": limpar_numero(escola['CD_IBGE']),
                        "latitude": limpar_float(escola['DS_LATITUDE']),
                        "longitude": limpar_float(escola['DS_LONGITUDE'])
                    },
                    "administrativa": {
                        "dependencia": limpar_string(escola['NOMEDEP']),
                        "diretoria_ensino": limpar_string(escola['DE']),
                        "situacao": limpar_numero(escola['CODSIT']),
                        "vinculo": limpar_numero(escola['CODVINC'])
                    }
                }
                
                escolas_json.append(escola_obj)
            
            # Salvar arquivo JSON
            filename = f"escolas_{tipo_nome.lower()}.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(escolas_json, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {filename:<35} : {len(escolas_json):,} escolas")
            total_processadas += len(escolas_json)
        
        # Gerar arquivo de estatísticas gerais
        estatisticas_gerais = {
            "data_processamento": "2025-08-11",
            "fonte": "ENDERECO_ESCOLAS_062025 (1).csv",
            "total_escolas": int(len(df)),
            "total_processadas": total_processadas,
            "tipos_escola": {str(k): v for k, v in estatisticas.items()},
            "metadados": {
                "encoding": "UTF-8",
                "formato": "JSON",
                "estrutura": "padronizada"
            }
        }
        
        stats_path = os.path.join(output_dir, "estatisticas_tipos_escola.json")
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(estatisticas_gerais, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 Arquivo de estatísticas: estatisticas_tipos_escola.json")
        
        # Resumo final
        print("\n" + "=" * 60)
        print("🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print(f"📁 Diretório de saída: {output_dir}/")
        print(f"📊 Total de escolas processadas: {total_processadas:,}")
        print(f"📂 Arquivos JSON gerados: {len(tipos_unicos)} tipos")
        print(f"📈 Arquivo de estatísticas: estatisticas_tipos_escola.json")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO ao processar arquivo: {e}")
        return False

def gerar_relatorio_tipos():
    """
    Gera relatório detalhado dos tipos de escola
    """
    print("\n📋 RELATÓRIO DETALHADO DOS TIPOS DE ESCOLA")
    print("=" * 50)
    
    for codigo, nome in TIPOS_ESCOLA.items():
        print(f"{codigo:2d} = {nome}")
    
    print(f"\nTotal de tipos mapeados: {len(TIPOS_ESCOLA)}")

if __name__ == "__main__":
    print("🚀 INICIANDO PROCESSAMENTO DE ESCOLAS CITEM")
    print("Data:", "11/08/2025")
    print("Objetivo: Gerar JSONs por tipo de escola")
    print()
    
    # Gerar relatório de tipos
    gerar_relatorio_tipos()
    
    # Processar escolas
    sucesso = processar_escolas_citem()
    
    if sucesso:
        print("\n✅ Processamento finalizado com sucesso!")
        print("📂 Verifique o diretório 'dados/json/por_tipo/' para os arquivos gerados")
    else:
        print("\n❌ Erro durante o processamento")
