#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise e Padronização das Bases de Dados
Preparação para migração Flask + SQLAlchemy + PostgreSQL
"""

import json
import pandas as pd
from pathlib import Path
import os


def analisar_bases_existentes():
    """Analisar todas as bases de dados existentes"""
    print("🔍 ANALISANDO BASES DE DADOS EXISTENTES...")
    print("=" * 60)
    
    bases_encontradas = {}
    
    # 1. Analisar JSONs principais
    json_files = [
        'dados/json/dados_escolas_atualizados.json',
        'dados_veiculos_diretorias.json',
        'dados_supervisao_atualizados.json',
        'estatisticas_atualizadas.json'
    ]
    
    for file_path in json_files:
        if os.path.exists(file_path):
            print(f"\n📄 Analisando: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                print(f"   📊 Registros: {len(data)}")
                if data:
                    print(f"   🔑 Campos: {list(data[0].keys())}")
                    bases_encontradas[file_path] = {
                        'tipo': 'lista',
                        'registros': len(data),
                        'campos': list(data[0].keys()),
                        'dados': data
                    }
            elif isinstance(data, dict):
                print(f"   📊 Tipo: Dicionário")
                print(f"   🔑 Chaves principais: {list(data.keys())}")
                bases_encontradas[file_path] = {
                    'tipo': 'dicionario',
                    'chaves': list(data.keys()),
                    'dados': data
                }
    
    # 2. Analisar Excel files
    excel_files = [
        'diretorias_com_coordenadas.xlsx',
        'diretorias_ensino_completo.xlsx',
        'QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx',
        'GEP.xlsx'
    ]
    
    for file_path in excel_files:
        if os.path.exists(file_path):
            print(f"\n📊 Analisando Excel: {file_path}")
            try:
                df = pd.read_excel(file_path)
                print(f"   📈 Linhas: {len(df)}")
                print(f"   📋 Colunas: {list(df.columns)}")
                bases_encontradas[file_path] = {
                    'tipo': 'excel',
                    'linhas': len(df),
                    'colunas': list(df.columns),
                    'dados': df
                }
            except Exception as e:
                print(f"   ❌ Erro ao ler: {e}")
    
    return bases_encontradas


def definir_entidades_principais():
    """Definir as entidades principais do sistema"""
    print("\n🏗️ DEFININDO ENTIDADES PRINCIPAIS...")
    print("=" * 60)
    
    entidades = {
        'escola': {
            'campos_principais': [
                'id', 'codigo_mec', 'nome', 'tipo', 'endereco',
                'cidade', 'uf', 'cep', 'latitude', 'longitude',
                'zona', 'situacao', 'diretoria_id'
            ],
            'relacionamentos': ['diretoria'],
            'descricao': 'Unidades escolares de todos os tipos'
        },
        'diretoria': {
            'campos_principais': [
                'id', 'nome', 'codigo', 'endereco', 'cidade',
                'latitude', 'longitude', 'telefone', 'email'
            ],
            'relacionamentos': ['escolas', 'veiculos', 'supervisores'],
            'descricao': 'Diretorias de Ensino responsáveis pelas escolas'
        },
        'veiculo': {
            'campos_principais': [
                'id', 'tipo', 'modelo', 'placa', 'ano',
                'capacidade', 'status', 'diretoria_id'
            ],
            'relacionamentos': ['diretoria'],
            'descricao': 'Veículos para transporte escolar'
        },
        'supervisor': {
            'campos_principais': [
                'id', 'nome', 'cargo', 'telefone', 'email',
                'diretoria_id', 'area_responsabilidade'
            ],
            'relacionamentos': ['diretoria'],
            'descricao': 'Supervisores do GEP responsáveis por diretorias'
        },
        'distancia': {
            'campos_principais': [
                'id', 'escola_id', 'diretoria_id', 'distancia_km',
                'metodo_calculo', 'data_calculo'
            ],
            'relacionamentos': ['escola', 'diretoria'],
            'descricao': 'Distâncias calculadas entre escolas e diretorias'
        }
    }
    
    for nome, dados in entidades.items():
        print(f"\n🔷 {nome.upper()}")
        print(f"   📝 {dados['descricao']}")
        print(f"   🔑 Campos: {', '.join(dados['campos_principais'][:5])}...")
        print(f"   🔗 Relaciona com: {', '.join(dados['relacionamentos'])}")
    
    return entidades


def padronizar_dados_escolas(bases_encontradas):
    """Padronizar dados de escolas"""
    print("\n🏫 PADRONIZANDO DADOS DE ESCOLAS...")
    print("-" * 40)
    
    # Usar base principal de escolas
    escolas_data = bases_encontradas.get('dados/json/dados_escolas_atualizados.json', {}).get('dados', [])
    
    if not escolas_data:
        print("❌ Dados de escolas não encontrados")
        return []
    
    escolas_padronizadas = []
    
    for i, escola in enumerate(escolas_data, 1):
        escola_padronizada = {
            'id': i,
            'codigo_mec': escola.get('codigo_mec', ''),
            'codigo': escola.get('codigo', ''),
            'nome': escola.get('name', '').strip(),
            'tipo': escola.get('type', 'regular'),
            'endereco': escola.get('endereco_escola', ''),
            'cidade': escola.get('city', '').strip(),
            'uf': 'SP',  # Todas são de São Paulo
            'zona': escola.get('zona', 'Urbana'),
            'situacao': escola.get('situacao', 1),
            'latitude': escola.get('lat'),
            'longitude': escola.get('lng'),
            'diretoria_nome': escola.get('diretoria', '').strip(),
            'distancia_diretoria': escola.get('distance', 0),
            'tipo_original': escola.get('tipo_original', ''),
            'codigo_ibge': escola.get('codigo_ibge'),
            'created_at': '2025-08-11',
            'updated_at': '2025-08-11'
        }
        escolas_padronizadas.append(escola_padronizada)
    
    print(f"✅ {len(escolas_padronizadas)} escolas padronizadas")
    return escolas_padronizadas


def padronizar_dados_diretorias(bases_encontradas):
    """Padronizar dados de diretorias"""
    print("\n🏛️ PADRONIZANDO DADOS DE DIRETORIAS...")
    print("-" * 40)
    
    # Extrair diretorias únicas das escolas
    escolas_data = bases_encontradas.get('dados/json/dados_escolas_atualizados.json', {}).get('dados', [])
    diretorias_nomes = sorted(set(escola.get('diretoria', '').strip() for escola in escolas_data if escola.get('diretoria')))
    
    # Dados de veículos por diretoria
    veiculos_data = bases_encontradas.get('dados_veiculos_diretorias.json', {}).get('dados', {})
    diretorias_veiculos = veiculos_data.get('diretorias', {}) if isinstance(veiculos_data, dict) else {}
    
    diretorias_padronizadas = []
    
    for i, nome in enumerate(diretorias_nomes, 1):
        # Buscar dados de veículos
        veiculos_info = diretorias_veiculos.get(nome, {})
        
        diretoria_padronizada = {
            'id': i,
            'nome': nome,
            'codigo': f"DE{i:03d}",
            'uf': 'SP',
            'regiao': 'Interior' if nome not in ['Centro', 'Centro Oeste', 'Centro Sul', 'Leste 1', 'Leste 2', 'Leste 3', 'Leste 4', 'Leste 5', 'Norte 1', 'Norte 2', 'Sul 1', 'Sul 2', 'Sul 3'] else 'Capital',
            'total_veiculos': veiculos_info.get('total', 0),
            'veiculos_s1': veiculos_info.get('s1', 0),
            'veiculos_s2': veiculos_info.get('s2', 0),
            'veiculos_s2_4x4': veiculos_info.get('s2_4x4', 0),
            'latitude': None,  # Será preenchido com coordenadas
            'longitude': None,
            'created_at': '2025-08-11',
            'updated_at': '2025-08-11'
        }
        diretorias_padronizadas.append(diretoria_padronizada)
    
    print(f"✅ {len(diretorias_padronizadas)} diretorias padronizadas")
    return diretorias_padronizadas


def padronizar_dados_veiculos(bases_encontradas):
    """Padronizar dados de veículos"""
    print("\n🚗 PADRONIZANDO DADOS DE VEÍCULOS...")
    print("-" * 40)
    
    veiculos_data = bases_encontradas.get('dados_veiculos_diretorias.json', {}).get('dados', {})
    diretorias_veiculos = veiculos_data.get('diretorias', {}) if isinstance(veiculos_data, dict) else {}
    
    veiculos_padronizados = []
    veiculo_id = 1
    
    for diretoria_nome, veiculos_info in diretorias_veiculos.items():
        # Criar registros para cada tipo de veículo
        tipos_veiculos = [
            ('S-1', veiculos_info.get('s1', 0), 'Veículo pequeno (até 7 lugares)'),
            ('S-2', veiculos_info.get('s2', 0), 'Veículo médio/grande (8+ lugares)'),
            ('S-2 4X4', veiculos_info.get('s2_4x4', 0), 'Veículo médio/grande com tração 4x4')
        ]
        
        for tipo, quantidade, descricao in tipos_veiculos:
            for i in range(quantidade):
                veiculo_padronizado = {
                    'id': veiculo_id,
                    'tipo': tipo,
                    'descricao': descricao,
                    'diretoria_nome': diretoria_nome,
                    'status': 'Ativo',
                    'capacidade': 7 if tipo == 'S-1' else 15,
                    'placa': f"VEI{veiculo_id:04d}",  # Placa fictícia
                    'ano': 2020,  # Ano padrão
                    'modelo': f"Modelo {tipo}",
                    'created_at': '2025-08-11',
                    'updated_at': '2025-08-11'
                }
                veiculos_padronizados.append(veiculo_padronizado)
                veiculo_id += 1
    
    print(f"✅ {len(veiculos_padronizados)} veículos padronizados")
    return veiculos_padronizados


def criar_base_centralizada(escolas, diretorias, veiculos):
    """Criar base de dados centralizada"""
    print("\n💾 CRIANDO BASE CENTRALIZADA...")
    print("-" * 40)
    
    # Criar diretório para bases padronizadas
    base_dir = Path('bases_padronizadas')
    base_dir.mkdir(exist_ok=True)
    
    # Salvar escolas
    with open(base_dir / 'escolas.json', 'w', encoding='utf-8') as f:
        json.dump(escolas, f, ensure_ascii=False, indent=2)
    print(f"✅ Escolas salvas: {len(escolas)} registros")
    
    # Salvar diretorias
    with open(base_dir / 'diretorias.json', 'w', encoding='utf-8') as f:
        json.dump(diretorias, f, ensure_ascii=False, indent=2)
    print(f"✅ Diretorias salvas: {len(diretorias)} registros")
    
    # Salvar veículos
    with open(base_dir / 'veiculos.json', 'w', encoding='utf-8') as f:
        json.dump(veiculos, f, ensure_ascii=False, indent=2)
    print(f"✅ Veículos salvos: {len(veiculos)} registros")
    
    # Criar metadados
    metadata = {
        'created_at': '2025-08-11T23:30:00',
        'description': 'Bases de dados padronizadas para migração Flask + SQLAlchemy',
        'version': '1.0',
        'entities': {
            'escolas': {
                'count': len(escolas),
                'description': 'Unidades escolares de todos os tipos'
            },
            'diretorias': {
                'count': len(diretorias),
                'description': 'Diretorias de Ensino'
            },
            'veiculos': {
                'count': len(veiculos),
                'description': 'Veículos para transporte escolar'
            }
        }
    }
    
    with open(base_dir / 'metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Metadados salvos")
    return base_dir


def main():
    """Função principal"""
    print("🚀 PADRONIZAÇÃO DE BASES DE DADOS")
    print("Preparando para migração Flask + SQLAlchemy + PostgreSQL")
    print("=" * 60)
    
    # 1. Analisar bases existentes
    bases = analisar_bases_existentes()
    
    # 2. Definir entidades
    entidades = definir_entidades_principais()
    
    # 3. Padronizar dados
    escolas = padronizar_dados_escolas(bases)
    diretorias = padronizar_dados_diretorias(bases)
    veiculos = padronizar_dados_veiculos(bases)
    
    # 4. Criar base centralizada
    base_dir = criar_base_centralizada(escolas, diretorias, veiculos)
    
    print(f"\n🎉 PADRONIZAÇÃO CONCLUÍDA!")
    print(f"📁 Bases salvas em: {base_dir}")
    print(f"📊 Total de registros:")
    print(f"   🏫 Escolas: {len(escolas)}")
    print(f"   🏛️ Diretorias: {len(diretorias)}")
    print(f"   🚗 Veículos: {len(veiculos)}")
    
    return base_dir


if __name__ == "__main__":
    main()
