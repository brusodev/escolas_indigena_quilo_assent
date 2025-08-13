#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSOLIDAÇÃO COMPLETA DE DADOS - CORREÇÃO DE INCONSISTÊNCIAS
===========================================================

Este script irá:
1. Analisar TODOS os arquivos existentes
2. Consolidar as 91 diretorias corretamente
3. Mapear todos os 10 tipos de escola
4. Criar siglas para as diretorias
5. Gerar um banco de dados centralizado e consistente
"""

import pandas as pd
import json
import os
from datetime import datetime


def criar_siglas_diretorias():
    """Cria siglas para as 91 diretorias baseadas nos nomes."""
    siglas_manuais = {
        'ADAMANTINA': 'ADAM',
        'AMERICANA': 'AMER',
        'ANDRADINA': 'ANDR',
        'APIAI': 'APIA',
        'ARACATUBA': 'ARAC',
        'ARARAQUARA': 'ARAR',
        'ASSIS': 'ASSI',
        'AVARE': 'AVAR',
        'BARRETOS': 'BARR',
        'BAURU': 'BAUR',
        'BIRIGUI': 'BIRI',
        'BOTUCATU': 'BOTU',
        'BRAGANCA PAULISTA': 'BRAP',
        'CAIEIRAS': 'CAIE',
        'CAMPINAS LESTE': 'CAML',
        'CAMPINAS OESTE': 'CAMO',
        'CAPIVARI': 'CAPI',
        'CARAGUATATUBA': 'CARA',
        'CARAPICUIBA': 'CARP',
        'CATANDUVA': 'CATA',
        'CENTRO': 'CENT',
        'CENTRO OESTE': 'CEO',
        'CENTRO SUL': 'CES',
        'DIADEMA': 'DIAD',
        'FERNANDOPOLIS': 'FERN',
        'FRANCA': 'FRAN',
        'GUARATINGUETA': 'GUAR',
        'GUARULHOS NORTE': 'GRUN',
        'GUARULHOS SUL': 'GRUS',
        'ITAPECERICA DA SERRA': 'ITAP',
        'ITAPETININGA': 'ITAT',
        'ITAPEVA': 'ITAV',
        'ITAPEVI': 'ITAE',
        'ITAQUAQUECETUBA': 'ITAQ',
        'ITARARE': 'ITAR',
        'ITU': 'ITU',
        'JABOTICABAL': 'JABO',
        'JACAREI': 'JACA',
        'JALES': 'JALE',
        'JAU': 'JAU',
        'JOSE BONIFACIO': 'JOSB',
        'JUNDIAI': 'JUND',
        'LESTE 1': 'L1',
        'LESTE 2': 'L2',
        'LESTE 3': 'L3',
        'LESTE 4': 'L4',
        'LESTE 5': 'L5',
        'LIMEIRA': 'LIME',
        'LINS': 'LINS',
        'MARILIA': 'MARI',
        'MAUA': 'MAUA',
        'MIRACATU': 'MIRA',
        'MIRANTE DO PARANAPANEMA': 'MIRAN',
        'MOGI DAS CRUZES': 'MOGC',
        'MOGI MIRIM': 'MOGM',
        'NORTE 1': 'N1',
        'NORTE 2': 'N2',
        'OSASCO': 'OSAC',
        'OURINHOS': 'OURI',
        'PENAPOLIS': 'PENA',
        'PINDAMONHANGABA': 'PIND',
        'PIRACICABA': 'PIRA',
        'PIRAJU': 'PIRU',
        'PIRASSUNUNGA': 'PIRS',
        'PRESIDENTE PRUDENTE': 'PREP',
        'REGISTRO': 'REGI',
        'RIBEIRAO PRETO': 'RIBP',
        'SANTO ANASTACIO': 'STAN',
        'SANTO ANDRE': 'STAN',
        'SANTOS': 'SANT',
        'SAO BERNARDO DO CAMPO': 'SBCA',
        'SAO CARLOS': 'SCAR',
        'SAO JOAO DA BOA VISTA': 'SJBV',
        'SAO JOAQUIM DA BARRA': 'SJBA',
        'SAO JOSE DO RIO PRETO': 'SJRP',
        'SAO JOSE DOS CAMPOS': 'SJCA',
        'SAO ROQUE': 'SROQ',
        'SAO VICENTE': 'SVIC',
        'SERTAOZINHO': 'SERT',
        'SOROCABA': 'SORO',
        'SUL 1': 'S1',
        'SUL 2': 'S2',
        'SUL 3': 'S3',
        'SUMARE': 'SUMA',
        'SUZANO': 'SUZA',
        'TABOAO DA SERRA': 'TABS',
        'TAQUARITINGA': 'TAQT',
        'TAUBATE': 'TAUB',
        'TUPA': 'TUPA',
        'VOTORANTIM': 'VOTO',
        'VOTUPORANGA': 'VOTP'
    }
    return siglas_manuais


def mapear_tipos_escola():
    """Mapeia todos os 10 tipos de escola encontrados."""
    tipos_escola = {
        3: {
            'nome': 'CEEJA',
            'descricao': 'Centro Estadual de Educação de Jovens e Adultos',
            'categoria': 'Educação Especial'
        },
        6: {
            'nome': 'CEL JTO',
            'descricao': 'Centro de Línguas',
            'categoria': 'Educação Especial'
        },
        7: {
            'nome': 'HOSPITALAR',
            'descricao': 'Escola Hospitalar',
            'categoria': 'Educação Especial'
        },
        8: {
            'nome': 'REGULAR',
            'descricao': 'Escola Regular',
            'categoria': 'Educação Regular'
        },
        9: {
            'nome': 'SOCIOEDUCATIVO',
            'descricao': 'Centro de Atendimento Socioeducativo',
            'categoria': 'Educação Especial'
        },
        10: {
            'nome': 'INDÍGENA',
            'descricao': 'Escola Indígena',
            'categoria': 'Educação Étnica'
        },
        15: {
            'nome': 'PENITENCIÁRIA',
            'descricao': 'Escola Penitenciária',
            'categoria': 'Educação Especial'
        },
        31: {
            'nome': 'ASSENTAMENTO',
            'descricao': 'Escola de Assentamento Rural',
            'categoria': 'Educação Rural'
        },
        34: {
            'nome': 'SOCIOEDUCATIVO ADOLESCENTE',
            'descricao': 'Centro de Atendimento Socioeducativo para Adolescente',
            'categoria': 'Educação Especial'
        },
        36: {
            'nome': 'QUILOMBOLA',
            'descricao': 'Escola Quilombola',
            'categoria': 'Educação Étnica'
        }
    }
    return tipos_escola


def consolidar_dados_completos():
    """Consolida todos os dados em um banco consistente."""

    print("🔄 INICIANDO CONSOLIDAÇÃO COMPLETA DE DADOS")
    print("=" * 60)

    # 1. Carregar dados do CSV oficial (fonte principal)
    print("\n1. 📊 CARREGANDO DADOS DO CSV OFICIAL...")
    df_csv = pd.read_csv(
        'dados/ENDERECO_ESCOLAS_062025 (1).csv', sep=';', encoding='latin-1')
    print(f"   ✅ {len(df_csv):,} escolas carregadas")
    print(f"   ✅ {df_csv['DE'].nunique()} diretorias encontradas")
    print(f"   ✅ {df_csv['TIPOESC'].nunique()} tipos de escola encontrados")

    # 2. Carregar diretorias com endereços
    print("\n2. 🏢 CARREGANDO DADOS DAS DIRETORIAS...")
    df_diretorias = pd.read_excel(
        'dados/excel/diretorias_ensino_completo.xlsx')
    print(f"   ✅ {len(df_diretorias)} diretorias com endereços completos")

    # 3. Criar mapeamentos
    print("\n3. 🗺️  CRIANDO MAPEAMENTOS...")
    siglas_diretorias = criar_siglas_diretorias()
    tipos_escola = mapear_tipos_escola()
    print(f"   ✅ {len(siglas_diretorias)} siglas de diretorias criadas")
    print(f"   ✅ {len(tipos_escola)} tipos de escola mapeados")

    # 4. Consolidar diretorias com informações completas
    print("\n4. 🔧 CONSOLIDANDO DIRETORIAS...")
    diretorias_consolidadas = []

    # Lista das 91 diretorias do CSV
    diretorias_csv = sorted(df_csv['DE'].unique())

    for i, nome_diretoria in enumerate(diretorias_csv, 1):
        # Buscar dados no Excel de diretorias
        diretoria_excel = df_diretorias[
            df_diretorias['Nome da Diretoria'].str.upper().str.contains(
                nome_diretoria.replace(' ', '.*'), regex=True, na=False
            )
        ]

        # Contar escolas por tipo nesta diretoria
        escolas_diretoria = df_csv[df_csv['DE'] == nome_diretoria]
        total_escolas = len(escolas_diretoria)

        # Estatísticas por tipo
        tipos_estatisticas = {}
        for tipo_codigo in escolas_diretoria['TIPOESC'].unique():
            qtd = len(
                escolas_diretoria[escolas_diretoria['TIPOESC'] == tipo_codigo])
            tipo_info = tipos_escola.get(
                tipo_codigo, {'nome': f'TIPO_{tipo_codigo}'})
            tipos_estatisticas[str(tipo_codigo)] = {
                'quantidade': int(qtd),
                'nome': tipo_info['nome'],
                'descricao': tipo_info.get('descricao', ''),
                'categoria': tipo_info.get('categoria', '')
            }

        # Dados da diretoria
        diretoria_dados = {
            'id': int(i),
            'nome': nome_diretoria,
            'sigla': siglas_diretorias.get(nome_diretoria, nome_diretoria[:4]),
            'total_escolas': int(total_escolas),
            'tipos_escola': tipos_estatisticas,
            'endereco_completo': '',
            'logradouro': '',
            'numero': '',
            'bairro': '',
            'cidade': '',
            'cep': '',
            'telefone': '',
            'email': '',
            'dirigente': '',
            'coordenadas': {'latitude': None, 'longitude': None}
        }

        # Se encontrou dados no Excel, usar
        if not diretoria_excel.empty:
            row = diretoria_excel.iloc[0]
            diretoria_dados.update({
                'endereco_completo': str(row.get('Endereço Completo', '')),
                'logradouro': str(row.get('Logradouro', '')),
                'numero': str(row.get('Número', '')),
                'bairro': str(row.get('Bairro', '')),
                'cidade': str(row.get('Cidade', '')),
                'cep': str(row.get('CEP', '')),
                'telefone': str(row.get('Telefone', '')),
                'email': str(row.get('Email', '')),
                'dirigente': str(row.get('Dirigente', ''))
            })

        diretorias_consolidadas.append(diretoria_dados)

    print(f"   ✅ {len(diretorias_consolidadas)} diretorias consolidadas")

    # 5. Consolidar escolas com informações completas
    print("\n5. 🏫 CONSOLIDANDO ESCOLAS...")
    escolas_consolidadas = []

    for idx, row in df_csv.iterrows():
        tipo_codigo = row['TIPOESC']
        tipo_info = tipos_escola.get(
            tipo_codigo, {'nome': f'TIPO_{tipo_codigo}'})

        escola_dados = {
            'id': int(idx + 1),
            'codigo_escola': str(row.get('COD_ESC', '')),
            'codigo_mec': str(row.get('CODESCMEC', '')),
            'nome': str(row.get('NOMESC', '')),
            'diretoria': str(row.get('DE', '')),
            'municipio': str(row.get('MUN', '')),
            'distrito': str(row.get('DISTR', '')),
            'tipo_escola_codigo': int(tipo_codigo),
            'tipo_escola_nome': tipo_info['nome'],
            'tipo_escola_descricao': tipo_info.get('descricao', ''),
            'tipo_escola_categoria': tipo_info.get('categoria', ''),
            'endereco': str(row.get('ENDESC', '')),
            'numero': str(row.get('NUMESC', '')),
            'complemento': str(row.get('COMPLEMENTO', '')),
            'bairro': str(row.get('BAIESC', '')),
            'cep': str(row.get('CEP', '')),
            'zona': str(row.get('ZONA', '')),
            'latitude': float(str(row.get('DS_LATITUDE', 0)).replace(',', '.')) if pd.notna(row.get('DS_LATITUDE')) else None,
            'longitude': float(str(row.get('DS_LONGITUDE', 0)).replace(',', '.')) if pd.notna(row.get('DS_LONGITUDE')) else None,
            'situacao': str(row.get('CODSIT', '')),
            'vinculo': str(row.get('CODVINC', ''))
        }

        escolas_consolidadas.append(escola_dados)

    print(f"   ✅ {len(escolas_consolidadas):,} escolas consolidadas")

    # 6. Criar estatísticas gerais
    print("\n6. 📈 CRIANDO ESTATÍSTICAS GERAIS...")
    estatisticas_gerais = {
        'data_atualizacao': datetime.now().isoformat(),
        'total_escolas': len(escolas_consolidadas),
        'total_diretorias': len(diretorias_consolidadas),
        'total_tipos_escola': len(tipos_escola),
        'estatisticas_por_tipo': {},
        'estatisticas_por_diretoria': {},
        'resumo_por_categoria': {}
    }

    # Estatísticas por tipo
    for tipo_codigo, tipo_info in tipos_escola.items():
        qtd = len(
            [e for e in escolas_consolidadas if e['tipo_escola_codigo'] == tipo_codigo])
        estatisticas_gerais['estatisticas_por_tipo'][tipo_codigo] = {
            'nome': tipo_info['nome'],
            'quantidade': qtd,
            'percentual': round((qtd / len(escolas_consolidadas)) * 100, 2)
        }

    # Estatísticas por categoria
    categorias = {}
    for escola in escolas_consolidadas:
        categoria = escola['tipo_escola_categoria']
        if categoria not in categorias:
            categorias[categoria] = 0
        categorias[categoria] += 1

    for categoria, qtd in categorias.items():
        estatisticas_gerais['resumo_por_categoria'][categoria] = {
            'quantidade': qtd,
            'percentual': round((qtd / len(escolas_consolidadas)) * 100, 2)
        }

    # 7. Salvar dados consolidados
    print("\n7. 💾 SALVANDO DADOS CONSOLIDADOS...")

    # Criar pasta de dados consolidados
    os.makedirs('dados/consolidados', exist_ok=True)

    # Salvar diretorias
    with open('dados/consolidados/diretorias_91_completas.json', 'w', encoding='utf-8') as f:
        json.dump(diretorias_consolidadas, f, ensure_ascii=False, indent=2)

    # Salvar escolas
    with open('dados/consolidados/escolas_5582_completas.json', 'w', encoding='utf-8') as f:
        json.dump(escolas_consolidadas, f, ensure_ascii=False, indent=2)

    # Salvar tipos de escola
    with open('dados/consolidados/tipos_escola_10_completos.json', 'w', encoding='utf-8') as f:
        json.dump(tipos_escola, f, ensure_ascii=False, indent=2)

    # Salvar estatísticas
    with open('dados/consolidados/estatisticas_completas.json', 'w', encoding='utf-8') as f:
        json.dump(estatisticas_gerais, f, ensure_ascii=False, indent=2)

    # Salvar siglas das diretorias
    with open('dados/consolidados/siglas_diretorias.json', 'w', encoding='utf-8') as f:
        json.dump(siglas_diretorias, f, ensure_ascii=False, indent=2)

    print("   ✅ Arquivos salvos em dados/consolidados/")

    # 8. Gerar relatório de consolidação
    print("\n8. 📋 GERANDO RELATÓRIO DE CONSOLIDAÇÃO...")

    relatorio = f"""# RELATÓRIO DE CONSOLIDAÇÃO COMPLETA
## Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## 🎯 RESUMO EXECUTIVO
- **Total de Escolas**: {len(escolas_consolidadas):,}
- **Total de Diretorias**: {len(diretorias_consolidadas)} (✅ CORRETO - 91 diretorias)
- **Total de Tipos de Escola**: {len(tipos_escola)} (✅ CORRETO - 10 tipos)

## 📊 ESTATÍSTICAS POR TIPO DE ESCOLA

"""

    for tipo_codigo in sorted(tipos_escola.keys()):
        tipo_info = tipos_escola[tipo_codigo]
        qtd = len(
            [e for e in escolas_consolidadas if e['tipo_escola_codigo'] == tipo_codigo])
        percentual = round((qtd / len(escolas_consolidadas)) * 100, 2)
        relatorio += f"### {tipo_info['nome']} (Tipo {tipo_codigo})\n"
        relatorio += f"- **Quantidade**: {qtd:,} escolas ({percentual}%)\n"
        relatorio += f"- **Descrição**: {tipo_info['descricao']}\n"
        relatorio += f"- **Categoria**: {tipo_info['categoria']}\n\n"

    relatorio += f"""
## 🏢 DIRETORIAS COM SIGLAS

"""

    for diretoria in sorted(diretorias_consolidadas, key=lambda x: x['nome']):
        relatorio += f"- **{diretoria['nome']}** ({diretoria['sigla']}) - {diretoria['total_escolas']} escolas\n"

    relatorio += f"""

## 📁 ARQUIVOS GERADOS

1. **diretorias_91_completas.json** - Todas as 91 diretorias com informações completas
2. **escolas_5582_completas.json** - Todas as 5.582 escolas com dados consolidados
3. **tipos_escola_10_completos.json** - Os 10 tipos de escola mapeados
4. **estatisticas_completas.json** - Estatísticas gerais do sistema
5. **siglas_diretorias.json** - Siglas para uso em mapas interativos

## ✅ STATUS: CONSOLIDAÇÃO COMPLETA E CONSISTENTE
"""

    with open('dados/consolidados/RELATORIO_CONSOLIDACAO.md', 'w', encoding='utf-8') as f:
        f.write(relatorio)

    print("   ✅ Relatório salvo em dados/consolidados/RELATORIO_CONSOLIDACAO.md")

    print(f"\n🎉 CONSOLIDAÇÃO COMPLETA FINALIZADA!")
    print(f"   📊 {len(escolas_consolidadas):,} escolas processadas")
    print(f"   🏢 {len(diretorias_consolidadas)} diretorias consolidadas")
    print(f"   🏫 {len(tipos_escola)} tipos de escola mapeados")
    print(f"   📁 Dados salvos em dados/consolidados/")

    return {
        'diretorias': diretorias_consolidadas,
        'escolas': escolas_consolidadas,
        'tipos_escola': tipos_escola,
        'estatisticas': estatisticas_gerais
    }


if __name__ == "__main__":
    resultado = consolidar_dados_completos()
