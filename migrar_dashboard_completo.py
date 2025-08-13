#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIGRAÇÃO DASHBOARD - INTEGRAÇÃO DAS 5.582 ESCOLAS
===============================================

Este script integra as 5.582 escolas do CITEM no dashboard existente,
mantendo compatibilidade com a estrutura atual.

Estratégia:
1. Detectar arquivos atuais do dashboard
2. Fazer backup dos dados existentes
3. Gerar novo arquivo compatível com 5.582 escolas
4. Atualizar estatísticas do dashboard
5. Criar seletores por tipo de escola

Autor: Sistema Dashboard Escolas
Data: 11/08/2025
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


def fazer_backup_dashboard():
    """Fazer backup dos arquivos atuais do dashboard"""
    print("💾 CRIANDO BACKUP DOS ARQUIVOS ATUAIS...")
    print("-" * 40)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_dashboard_{timestamp}"

    Path(backup_dir).mkdir(exist_ok=True)

    # Arquivos para backup
    arquivos_backup = [
        "dados/json/dados_escolas_atualizados.json",
        "dashboard_integrado.html",
        "static/js/modules/data-loader.js"
    ]

    for arquivo in arquivos_backup:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, backup_dir)
            print(f"✅ Backup: {arquivo}")

    print(f"📁 Backup criado em: {backup_dir}/")
    return backup_dir


def carregar_dados_citem():
    """Carregar dados das 5.582 escolas processadas"""
    print("\n📊 CARREGANDO DADOS CITEM...")
    print("-" * 30)

    # Carregar estatísticas
    with open('dados/json/por_tipo/estatisticas_tipos_escola.json', 'r', encoding='utf-8') as f:
        stats = json.load(f)

    # Carregar diretorias/unidades regionais
    with open('dados/mapeamento_unidades_regionais.json', 'r', encoding='utf-8') as f:
        unidades = json.load(f)

    # Carregar todos os tipos de escola
    tipos_arquivos = {
        'regular': 'dados/json/por_tipo/escolas_regular.json',
        'indigena': 'dados/json/por_tipo/escolas_indigena.json',
        'quilombola': 'dados/json/por_tipo/escolas_quilombola.json',
        'assentamento': 'dados/json/por_tipo/escolas_assentamento.json',
        'ceeja': 'dados/json/por_tipo/escolas_ceeja.json',
        'cel_jto': 'dados/json/por_tipo/escolas_cel_jto.json',
        'hospitalar': 'dados/json/por_tipo/escolas_hospitalar.json',
        'escola_penitenciaria': 'dados/json/por_tipo/escolas_escola_penitenciaria.json',
        'centro_atend_socioeduc': 'dados/json/por_tipo/escolas_centro_atend_socioeduc.json',
        'centro_atend_soc_educ_adolesc': 'dados/json/por_tipo/escolas_centro_atend_soc_educ_adolesc.json'
    }

    todas_escolas = []
    stats_tipos = {}

    for tipo, arquivo in tipos_arquivos.items():
        with open(arquivo, 'r', encoding='utf-8') as f:
            escolas = json.load(f)
            todas_escolas.extend(escolas)
            stats_tipos[tipo] = len(escolas)
            print(f"✅ {tipo.upper()}: {len(escolas)} escolas")

    print(f"\n📈 Total carregado: {len(todas_escolas)} escolas")

    return todas_escolas, stats_tipos, unidades


def converter_para_formato_dashboard(escolas_citem, unidades_regionais):
    """Converter dados CITEM para formato compatível com dashboard"""
    print("\n🔄 CONVERTENDO PARA FORMATO DO DASHBOARD...")
    print("-" * 45)

    # Mapeamento de tipos para compatibilidade
    tipo_mapping = {
        'INDIGENA': 'indigena',
        'QUILOMBOLA': 'quilombola',
        'ASSENTAMENTO': 'assentamento',
        'REGULAR': 'regular',
        'CEEJA': 'ceeja',
        'CEL_JTO': 'cel_jto',
        'HOSPITALAR': 'hospitalar',
        'ESCOLA_PENITENCIARIA': 'penitenciaria',
        'CENTRO_ATEND_SOCIOEDUC': 'socioeduc',
        'CENTRO_ATEND_SOC_EDUC_ADOLESC': 'socioeduc_adolesc'
    }

    escolas_dashboard = []
    diretorias_encontradas = set()

    for escola in escolas_citem:
        # Converter tipo
        tipo_original = escola['tipo_nome']
        tipo_dashboard = tipo_mapping.get(tipo_original, 'outros')

        # Normalizar nome da diretoria
        diretoria_original = escola['administrativa']['diretoria_ensino']
        diretoria_normalizada = normalizar_diretoria(
            diretoria_original, unidades_regionais)
        diretorias_encontradas.add(diretoria_normalizada)

        # Converter para formato dashboard
        escola_dashboard = {
            "name": escola['nome'],
            "type": tipo_dashboard,
            "city": escola['localizacao']['municipio'],
            "diretoria": diretoria_normalizada,
            "distance": 0,  # Será calculado posteriormente se necessário
            "lat": escola['localizacao']['latitude'],
            "lng": escola['localizacao']['longitude'],
            "de_lat": None,  # Coordenadas da diretoria (se disponível)
            "de_lng": None,
            "endereco_escola": f"{escola['endereco']['logradouro']}, {escola['endereco']['numero']}, {escola['endereco']['bairro']}, CEP: {escola['endereco']['cep']}",
            "endereco_diretoria": "",
            "codigo": escola['codigo'],
            "codigo_mec": escola['codigo_mec'],
            "tipo_original": tipo_original,
            "zona": escola['endereco']['zona'],
            "codigo_ibge": escola['localizacao']['codigo_ibge'],
            "situacao": escola['administrativa']['situacao']
        }

        escolas_dashboard.append(escola_dashboard)

    print(f"✅ {len(escolas_dashboard)} escolas convertidas")
    print(f"📍 {len(diretorias_encontradas)} diretorias encontradas")

    return escolas_dashboard, diretorias_encontradas


def normalizar_diretoria(diretoria_original, unidades_regionais):
    """Normalizar nome da diretoria usando mapeamento de unidades regionais"""
    if not diretoria_original:
        return "NÃO INFORMADO"

    diretoria_upper = diretoria_original.upper().strip()

    # Procurar no mapeamento de unidades regionais
    for key, unidade in unidades_regionais['unidades_regionais'].items():
        if key in diretoria_upper or diretoria_upper in key:
            return key.title()

    # Se não encontrar, tentar normalização simples
    return diretoria_upper.title()


def gerar_arquivo_dashboard_atualizado(escolas_dashboard, stats_tipos):
    """Gerar novo arquivo dados_escolas_atualizados.json com todas as escolas"""
    print("\n💾 GERANDO ARQUIVO ATUALIZADO DO DASHBOARD...")
    print("-" * 45)

    output_file = "dados/json/dados_escolas_atualizados_completo.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(escolas_dashboard, f, ensure_ascii=False, indent=2)

    print(f"✅ Arquivo gerado: {output_file}")
    print(f"📊 Total de escolas: {len(escolas_dashboard)}")

    # Gerar arquivo de configuração com tipos
    config_dashboard = {
        "metadata": {
            "data_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "versao": "2.0 - CITEM Completo",
            "total_escolas": len(escolas_dashboard),
            "fonte": "CITEM - Base Completa 5.582 escolas"
        },
        "tipos_escola": stats_tipos,
        "configuracao": {
            "mapa_inicial": {
                "centro_lat": -23.5,
                "centro_lng": -46.6,
                "zoom": 7
            },
            "filtros_disponiveis": list(stats_tipos.keys()),
            "cores_tipos": {
                "indigena": "#8B4513",
                "quilombola": "#800080",
                "assentamento": "#228B22",
                "regular": "#4169E1",
                "ceeja": "#FF6347",
                "cel_jto": "#FF8C00",
                "hospitalar": "#DC143C",
                "penitenciaria": "#2F4F4F",
                "socioeduc": "#9932CC",
                "socioeduc_adolesc": "#8A2BE2"
            }
        }
    }

    config_file = "dados/json/config_dashboard_completo.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_dashboard, f, ensure_ascii=False, indent=2)

    print(f"✅ Configuração gerada: {config_file}")

    return output_file, config_file


def atualizar_data_loader(stats_tipos):
    """Atualizar módulo data-loader.js para incluir novos tipos"""
    print("\n🔄 ATUALIZANDO MÓDULO DATA-LOADER...")
    print("-" * 35)

    # Ler arquivo atual
    data_loader_path = "static/js/modules/data-loader.js"

    with open(data_loader_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Atualizar caminho do arquivo de dados
    content_updated = content.replace(
        'fetch("dados/json/dados_escolas_atualizados.json")',
        'fetch("dados/json/dados_escolas_atualizados_completo.json")'
    )

    # Adicionar comentário sobre atualização
    header_comment = """// ===================================================
// MÓDULO: CARREGAMENTO DE DADOS - VERSÃO CITEM COMPLETA
// ===================================================
// ATUALIZADO: 11/08/2025 - Integração das 5.582 escolas
// FONTE: Base completa CITEM com todos os tipos de escola
// TIPOS DISPONÍVEIS: """ + ", ".join(stats_tipos.keys()) + """
// ===================================================

"""

    # Substituir header
    content_updated = content_updated.replace(
        "// ===================================================\n// MÓDULO: CARREGAMENTO DE DADOS\n// ===================================================",
        header_comment.strip()
    )

    # Salvar arquivo atualizado
    new_data_loader = "static/js/modules/data-loader-citem-completo.js"
    with open(new_data_loader, 'w', encoding='utf-8') as f:
        f.write(content_updated)

    print(f"✅ Módulo atualizado: {new_data_loader}")

    return new_data_loader


def main():
    """Função principal de migração"""
    print("🚀 MIGRAÇÃO DASHBOARD - INTEGRAÇÃO CITEM COMPLETA")
    print("=" * 55)
    print("Objetivo: Integrar 5.582 escolas no dashboard existente")
    print("Data:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print()

    try:
        # 1. Fazer backup
        backup_dir = fazer_backup_dashboard()

        # 2. Carregar dados CITEM
        escolas_citem, stats_tipos, unidades = carregar_dados_citem()

        # 3. Converter para formato dashboard
        escolas_dashboard, diretorias = converter_para_formato_dashboard(
            escolas_citem, unidades)

        # 4. Gerar arquivos atualizados
        arquivo_dados, arquivo_config = gerar_arquivo_dashboard_atualizado(
            escolas_dashboard, stats_tipos)

        # 5. Atualizar módulo JavaScript
        novo_data_loader = atualizar_data_loader(stats_tipos)

        # Resumo final
        print("\n" + "=" * 55)
        print("🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 55)
        print(f"📦 Backup criado: {backup_dir}/")
        print(f"📊 Escolas integradas: {len(escolas_dashboard)}")
        print(f"🏛️ Diretorias mapeadas: {len(diretorias)}")
        print(f"🎨 Tipos de escola: {len(stats_tipos)}")
        print()
        print("📁 ARQUIVOS GERADOS:")
        print(f"   📄 {arquivo_dados}")
        print(f"   ⚙️ {arquivo_config}")
        print(f"   🔧 {novo_data_loader}")
        print()
        print("🔄 PRÓXIMOS PASSOS:")
        print("   1. Testar o dashboard com os novos dados")
        print("   2. Atualizar dashboard_integrado.html se necessário")
        print("   3. Implementar filtros por tipo de escola")
        print("   4. Ajustar estatísticas na interface")

    except Exception as e:
        print(f"\n❌ ERRO NA MIGRAÇÃO: {str(e)}")
        print("💡 Verifique os arquivos de origem e tente novamente")


if __name__ == "__main__":
    main()
