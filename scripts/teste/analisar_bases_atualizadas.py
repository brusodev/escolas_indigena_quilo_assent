"""
RELATÓRIO DAS BASES DE DADOS MAIS ATUALIZADAS
Data da análise: 09/08/2025
Sistema: Gestão de Escolas Indígenas, Quilombolas e Assentamentos
"""

import json
import os
from datetime import datetime

def analisar_bases_dados():
    """Analisa todas as bases de dados e identifica as mais atualizadas"""
    
    print("🗃️  RELATÓRIO DAS BASES DE DADOS MAIS ATUALIZADAS")
    print("=" * 60)
    print()
    
    # Bases principais identificadas
    bases_principais = {
        "ESCOLAS": [
            "dados\\json\\dados_escolas_atualizados.json",
            "dados_escolas_atualizados.json",
            "dados_escolas_corrigidos.json"
        ],
        "VEÍCULOS": [
            "dados_veiculos_diretorias.json",
            "dados\\json\\dados_veiculos_diretorias.json", 
            "dados\\json\\dados_veiculos_originais_corretos.json",
            "dados\\json\\dados_veiculos_normalizados.json",
            "dados\\json\\dados_veiculos_atualizados.json"
        ],
        "SUPERVISÃO": [
            "dados\\json\\dados_supervisao_atualizados.json",
            "dados_supervisao_atualizados.json"
        ],
        "ESTATÍSTICAS": [
            "estatisticas_atualizadas.json",
            "dados\\json\\estatisticas_atualizadas.json"
        ],
        "EXCEL_RELATÓRIOS": [
            "relatorios\\excel\\Relatorio_Completo_Escolas_Diretorias.xlsx",
            "dados\\excel\\distancias_escolas_diretorias_completo_63_ATUALIZADO_20250808_103722.xlsx",
            "relatorios\\excel\\Relatorio_Veiculos_por_Diretoria_20250808_130326.xlsx"
        ]
    }
    
    print("📊 ANÁLISE POR CATEGORIA:")
    print()
    
    for categoria, arquivos in bases_principais.items():
        print(f"🔸 {categoria}")
        print("-" * 40)
        
        arquivos_existentes = []
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                stat = os.stat(arquivo)
                tamanho = stat.st_size
                data_mod = datetime.fromtimestamp(stat.st_mtime)
                
                # Verificar conteúdo se for JSON
                conteudo_info = ""
                if arquivo.endswith('.json') and tamanho > 0:
                    try:
                        with open(arquivo, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                conteudo_info = f"({len(data)} registros)"
                            elif isinstance(data, dict):
                                if 'metadata' in data:
                                    meta = data['metadata']
                                    if 'total_escolas' in meta:
                                        conteudo_info = f"({meta.get('total_escolas', 0)} escolas)"
                                    elif 'total_diretorias' in meta:
                                        conteudo_info = f"({meta.get('total_diretorias', 0)} diretorias)"
                                elif 'diretorias' in data:
                                    conteudo_info = f"({len(data['diretorias'])} diretorias)"
                                else:
                                    conteudo_info = f"({len(data)} itens)"
                    except:
                        conteudo_info = "(erro ao ler)"
                elif tamanho == 0:
                    conteudo_info = "(ARQUIVO VAZIO)"
                
                arquivos_existentes.append({
                    'arquivo': arquivo,
                    'tamanho': tamanho,
                    'data': data_mod,
                    'conteudo': conteudo_info
                })
        
        # Ordenar por data mais recente
        arquivos_existentes.sort(key=lambda x: x['data'], reverse=True)
        
        if arquivos_existentes:
            for i, info in enumerate(arquivos_existentes):
                status = "🟢 MAIS ATUAL" if i == 0 else "🟡 BACKUP"
                if info['tamanho'] == 0:
                    status = "🔴 VAZIO"
                
                print(f"  {status} {info['arquivo']}")
                print(f"      📅 {info['data'].strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"      📏 {info['tamanho']:,} bytes {info['conteudo']}")
                print()
        else:
            print("  ❌ Nenhum arquivo encontrado")
            print()
    
    print("=" * 60)
    print("🎯 RECOMENDAÇÕES - BASES PRINCIPAIS PARA USAR:")
    print()
    
    # Verificar e recomendar as melhores bases
    recomendacoes = []
    
    # Escolas
    if os.path.exists("dados\\json\\dados_escolas_atualizados.json"):
        with open("dados\\json\\dados_escolas_atualizados.json", 'r', encoding='utf-8') as f:
            escolas = json.load(f)
        recomendacoes.append(f"✅ ESCOLAS: dados\\json\\dados_escolas_atualizados.json ({len(escolas)} escolas)")
    
    # Veículos - verificar qual tem dados válidos
    veiculos_file = None
    if os.path.exists("dados\\json\\dados_veiculos_originais_corretos.json"):
        stat = os.stat("dados\\json\\dados_veiculos_originais_corretos.json")
        if stat.st_size > 0:
            veiculos_file = "dados\\json\\dados_veiculos_originais_corretos.json"
    
    if veiculos_file:
        with open(veiculos_file, 'r', encoding='utf-8') as f:
            veiculos = json.load(f)
        if 'diretorias' in veiculos:
            total_dirs = len(veiculos['diretorias'])
            total_veic = veiculos.get('metadata', {}).get('total_veiculos', 'N/A')
            recomendacoes.append(f"✅ VEÍCULOS: {veiculos_file} ({total_dirs} diretorias, {total_veic} veículos)")
    
    # Relatórios Excel
    excel_files = [
        "relatorios\\excel\\Relatorio_Completo_Escolas_Diretorias.xlsx",
        "dados\\excel\\distancias_escolas_diretorias_completo_63_ATUALIZADO_20250808_103722.xlsx"
    ]
    
    for excel_file in excel_files:
        if os.path.exists(excel_file):
            stat = os.stat(excel_file)
            data_mod = datetime.fromtimestamp(stat.st_mtime)
            recomendacoes.append(f"✅ EXCEL: {excel_file} ({data_mod.strftime('%d/%m/%Y %H:%M')})")
            break
    
    for rec in recomendacoes:
        print(rec)
    
    print()
    print("🚨 PROBLEMAS IDENTIFICADOS:")
    
    # Verificar arquivo principal vazio
    if os.path.exists("dados_veiculos_diretorias.json"):
        stat = os.stat("dados_veiculos_diretorias.json")
        if stat.st_size == 0:
            print("❌ dados_veiculos_diretorias.json está VAZIO - usar backup em dados\\json\\")
    
    print()
    print("💡 SUGESTÃO DE AÇÃO:")
    print("1. Restaurar dados_veiculos_diretorias.json do backup válido")
    print("2. Usar dados\\json\\dados_escolas_atualizados.json para escolas")
    print("3. Validar integridade antes de usar em produção")

if __name__ == "__main__":
    analisar_bases_dados()
