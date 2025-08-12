# -*- coding: utf-8 -*-
"""
Script para expandir e complementar o banco de dados com todas as informações disponíveis
Reunindo dados de escolas, diretorias, veículos, supervisores e distâncias
"""

import json
import pandas as pd
import os
from datetime import datetime

def carregar_dados_completos():
    """Carrega todos os dados disponíveis para análise e complementação"""
    dados = {
        'escolas': [],
        'diretorias': {},
        'veiculos': {},
        'supervisao': {},
        'diretorias_coordenadas': {}
    }
    
    # Carregar escolas atualizadas completas
    try:
        with open('dados/json/dados_escolas_atualizados_completo.json', 'r', encoding='utf-8') as f:
            dados['escolas'] = json.load(f)
        print(f"✅ Carregadas {len(dados['escolas'])} escolas")
    except FileNotFoundError:
        with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
            dados['escolas'] = json.load(f)
        print(f"✅ Carregadas {len(dados['escolas'])} escolas (arquivo alternativo)")
    
    # Carregar dados de veículos por diretoria
    try:
        with open('dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
            dados['veiculos'] = json.load(f)
        print(f"✅ Carregados dados de veículos para {len(dados['veiculos']['diretorias'])} diretorias")
    except FileNotFoundError:
        print("⚠️ Arquivo de veículos não encontrado")
    
    # Carregar dados de supervisão
    try:
        with open('dados_supervisao_atualizados.json', 'r', encoding='utf-8') as f:
            dados['supervisao'] = json.load(f)
        print(f"✅ Carregados dados de supervisão para {len(dados['supervisao'])} unidades")
    except FileNotFoundError:
        print("⚠️ Arquivo de supervisão não encontrado")
    
    # Carregar dados de coordenadas das diretorias
    try:
        df_diretorias = pd.read_excel('dados/excel/diretorias_com_coordenadas.xlsx')
        for _, row in df_diretorias.iterrows():
            nome = row.get('nome', row.get('diretoria', ''))
            if nome:
                dados['diretorias_coordenadas'][nome] = {
                    'nome': nome,
                    'endereco': row.get('endereco', ''),
                    'cidade': row.get('cidade', ''),
                    'latitude': row.get('latitude', None),
                    'longitude': row.get('longitude', None),
                    'cep': row.get('cep', ''),
                    'codigo': row.get('codigo', '')
                }
        print(f"✅ Carregadas coordenadas de {len(dados['diretorias_coordenadas'])} diretorias")
    except Exception as e:
        print(f"⚠️ Erro ao carregar coordenadas das diretorias: {e}")
    
    return dados

def criar_diretorias_completas(dados):
    """Cria dados completos das diretorias com todas as informações"""
    diretorias_completas = {}
    
    # Processar todas as escolas para agrupar por diretoria
    escolas_por_diretoria = {}
    for escola in dados['escolas']:
        diretoria = escola.get('diretoria', '')
        if diretoria:
            if diretoria not in escolas_por_diretoria:
                escolas_por_diretoria[diretoria] = []
            escolas_por_diretoria[diretoria].append(escola)
    
    # Criar dados completos para cada diretoria
    for diretoria_nome, escolas in escolas_por_diretoria.items():
        # Dados básicos
        diretoria_info = {
            'nome': diretoria_nome,
            'escolas_vinculadas': len(escolas),
            'escolas': [],
            'coordenadas': None,
            'endereco': '',
            'veiculos': {},
            'supervisor': '',
            'regiao_supervisao': '',
            'estatisticas': {
                'total_escolas': len(escolas),
                'escolas_indigenas': 0,
                'escolas_quilombolas': 0,
                'escolas_regulares': 0,
                'escolas_por_cidade': {}
            }
        }
        
        # Processar escolas
        for escola in escolas:
            escola_info = {
                'nome': escola.get('name', ''),
                'tipo': escola.get('type', ''),
                'cidade': escola.get('city', ''),
                'distancia': escola.get('distance', 0),
                'latitude': escola.get('lat'),
                'longitude': escola.get('lng'),
                'endereco': escola.get('endereco_escola', ''),
                'codigo': escola.get('codigo'),
                'codigo_mec': escola.get('codigo_mec'),
                'zona': escola.get('zona', '')
            }
            diretoria_info['escolas'].append(escola_info)
            
            # Atualizar estatísticas
            tipo = escola.get('type', 'regular')
            if tipo == 'indigena':
                diretoria_info['estatisticas']['escolas_indigenas'] += 1
            elif tipo == 'quilombola':
                diretoria_info['estatisticas']['escolas_quilombolas'] += 1
            else:
                diretoria_info['estatisticas']['escolas_regulares'] += 1
            
            # Contar por cidade
            cidade = escola.get('city', 'Não informado')
            if cidade not in diretoria_info['estatisticas']['escolas_por_cidade']:
                diretoria_info['estatisticas']['escolas_por_cidade'][cidade] = 0
            diretoria_info['estatisticas']['escolas_por_cidade'][cidade] += 1
        
        # Adicionar coordenadas se disponível
        if diretoria_nome in dados['diretorias_coordenadas']:
            coord = dados['diretorias_coordenadas'][diretoria_nome]
            diretoria_info['coordenadas'] = {
                'latitude': coord['latitude'],
                'longitude': coord['longitude']
            }
            diretoria_info['endereco'] = coord['endereco']
            diretoria_info['cidade'] = coord['cidade']
            diretoria_info['cep'] = coord['cep']
            diretoria_info['codigo'] = coord['codigo']
        
        # Adicionar dados de veículos
        if diretoria_nome in dados['veiculos'].get('diretorias', {}):
            veiculo_info = dados['veiculos']['diretorias'][diretoria_nome]
            diretoria_info['veiculos'] = {
                'total': veiculo_info.get('total', 0),
                's1_pequeno': veiculo_info.get('s1', 0),
                's2_medio_grande': veiculo_info.get('s2', 0),
                's2_4x4': veiculo_info.get('s2_4x4', 0),
                'detalhamento': {
                    'S-1': 'Veículo pequeno (até 7 lugares)',
                    'S-2': 'Veículo médio/grande (8+ lugares)',
                    'S-2 4X4': 'Veículo médio/grande com tração 4x4'
                }
            }
        
        # Adicionar supervisor e região
        for regiao, info_sup in dados['supervisao'].items():
            diretorias_regiao = info_sup.get('diretorias', '').upper()
            if diretoria_nome.upper() in diretorias_regiao:
                diretoria_info['supervisor'] = info_sup.get('supervisor', '')
                diretoria_info['regiao_supervisao'] = regiao
                break
        
        diretorias_completas[diretoria_nome] = diretoria_info
    
    return diretorias_completas

def criar_veiculos_detalhados(dados):
    """Cria dados detalhados dos veículos por diretoria"""
    if 'veiculos' not in dados or 'diretorias' not in dados['veiculos']:
        return {}
    
    veiculos_detalhados = {}
    
    for diretoria, info in dados['veiculos']['diretorias'].items():
        veiculos_detalhados[diretoria] = {
            'diretoria': diretoria,
            'total_veiculos': info.get('total', 0),
            'veiculos_por_tipo': {
                'S-1': {
                    'quantidade': info.get('s1', 0),
                    'descricao': 'Veículo pequeno (até 7 lugares)',
                    'categoria': 'pequeno'
                },
                'S-2': {
                    'quantidade': info.get('s2', 0),
                    'descricao': 'Veículo médio/grande (8+ lugares)',
                    'categoria': 'medio_grande'
                },
                'S-2 4X4': {
                    'quantidade': info.get('s2_4x4', 0),
                    'descricao': 'Veículo médio/grande com tração 4x4',
                    'categoria': 'medio_grande_4x4'
                }
            },
            'necessidade_especial': info.get('s2_4x4', 0) > 0,  # Tem tração 4x4
            'capacidade_total_estimada': (
                info.get('s1', 0) * 7 +  # S-1 até 7 lugares
                info.get('s2', 0) * 15 +  # S-2 estimado 15 lugares
                info.get('s2_4x4', 0) * 15  # S-2 4x4 estimado 15 lugares
            )
        }
    
    return veiculos_detalhados

def gerar_relatorio_completo(dados, diretorias_completas, veiculos_detalhados):
    """Gera relatório completo das informações"""
    relatorio = {
        'timestamp': datetime.now().isoformat(),
        'resumo_geral': {
            'total_escolas': len(dados['escolas']),
            'total_diretorias': len(diretorias_completas),
            'total_regioes_supervisao': len(dados['supervisao']),
            'total_veiculos': sum(v['total_veiculos'] for v in veiculos_detalhados.values())
        },
        'estatisticas_por_tipo': {
            'escolas_indigenas': len([e for e in dados['escolas'] if e.get('type') == 'indigena']),
            'escolas_quilombolas': len([e for e in dados['escolas'] if e.get('type') == 'quilombola']),
            'escolas_regulares': len([e for e in dados['escolas'] if e.get('type') == 'regular'])
        },
        'veiculos_por_tipo': {
            'S-1': sum(v['veiculos_por_tipo']['S-1']['quantidade'] for v in veiculos_detalhados.values()),
            'S-2': sum(v['veiculos_por_tipo']['S-2']['quantidade'] for v in veiculos_detalhados.values()),
            'S-2_4X4': sum(v['veiculos_por_tipo']['S-2 4X4']['quantidade'] for v in veiculos_detalhados.values())
        },
        'diretorias_com_mais_escolas': sorted(
            [(nome, info['estatisticas']['total_escolas']) for nome, info in diretorias_completas.items()],
            key=lambda x: x[1], reverse=True
        )[:10],
        'diretorias_com_mais_veiculos': sorted(
            [(nome, info['total_veiculos']) for nome, info in veiculos_detalhados.items()],
            key=lambda x: x[1], reverse=True
        )[:10]
    }
    
    return relatorio

def salvar_dados_expandidos(diretorias_completas, veiculos_detalhados, relatorio):
    """Salva os dados expandidos em arquivos JSON"""
    
    # Criar diretório se não existir
    os.makedirs('flask_sistema/data/json_expandido', exist_ok=True)
    
    # Salvar diretorias completas
    with open('flask_sistema/data/json_expandido/diretorias_completas.json', 'w', encoding='utf-8') as f:
        json.dump(diretorias_completas, f, ensure_ascii=False, indent=2)
    
    # Salvar veículos detalhados
    with open('flask_sistema/data/json_expandido/veiculos_detalhados.json', 'w', encoding='utf-8') as f:
        json.dump(veiculos_detalhados, f, ensure_ascii=False, indent=2)
    
    # Salvar relatório
    with open('flask_sistema/data/json_expandido/relatorio_completo.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 DADOS EXPANDIDOS SALVOS:")
    print(f"✅ Diretorias completas: {len(diretorias_completas)} registros")
    print(f"✅ Veículos detalhados: {len(veiculos_detalhados)} registros")
    print(f"✅ Relatório gerado com estatísticas completas")

def atualizar_modelos_flask():
    """Cria script para atualizar modelos Flask com novos campos"""
    script_atualizacao = '''# -*- coding: utf-8 -*-
"""
Script para atualizar modelos Flask com campos expandidos
"""

# Campos adicionais para o modelo Diretoria:
campos_diretoria = """
    # Informações geográficas
    cidade = db.Column(db.String(100))
    cep = db.Column(db.String(10))
    codigo = db.Column(db.String(20))
    
    # Estatísticas
    total_escolas = db.Column(db.Integer, default=0)
    escolas_indigenas = db.Column(db.Integer, default=0)
    escolas_quilombolas = db.Column(db.Integer, default=0)
    escolas_regulares = db.Column(db.Integer, default=0)
    
    # Supervisão
    supervisor = db.Column(db.String(200))
    regiao_supervisao = db.Column(db.String(100))
"""

# Campos adicionais para o modelo Veiculo:
campos_veiculo = """
    # Detalhamento do veículo
    categoria = db.Column(db.String(50))  # pequeno, medio_grande, medio_grande_4x4
    descricao_completa = db.Column(db.Text)
    capacidade_estimada = db.Column(db.Integer)
    necessidade_especial = db.Column(db.Boolean, default=False)
"""

# Campos adicionais para o modelo Escola:
campos_escola = """
    # Códigos identificadores
    codigo = db.Column(db.Integer)
    codigo_mec = db.Column(db.String(20))
    codigo_ibge = db.Column(db.Integer)
    
    # Informações administrativas
    zona = db.Column(db.String(20))  # Urbana, Rural
    situacao = db.Column(db.Integer)  # 1=Ativa, etc
    
    # Campos extras para relatórios
    tipo_original = db.Column(db.String(50))
"""

print("📋 Campos sugeridos para expansão dos modelos:")
print("\\n1. DIRETORIA:")
print(campos_diretoria)
print("\\n2. VEICULO:")
print(campos_veiculo)
print("\\n3. ESCOLA:")
print(campos_escola)
'''
    
    with open('flask_sistema/expandir_modelos_sugestoes.py', 'w', encoding='utf-8') as f:
        f.write(script_atualizacao)
    
    print("\n📝 Script de sugestões para expansão dos modelos criado em:")
    print("   flask_sistema/expandir_modelos_sugestoes.py")

def main():
    """Função principal"""
    print("🔄 EXPANDINDO BANCO DE DADOS COM INFORMAÇÕES COMPLETAS")
    print("=" * 60)
    
    # Carregar todos os dados
    dados = carregar_dados_completos()
    
    # Criar diretorias completas
    print("\n📋 Processando diretorias completas...")
    diretorias_completas = criar_diretorias_completas(dados)
    
    # Criar veículos detalhados
    print("\n🚗 Processando veículos detalhados...")
    veiculos_detalhados = criar_veiculos_detalhados(dados)
    
    # Gerar relatório
    print("\n📊 Gerando relatório completo...")
    relatorio = gerar_relatorio_completo(dados, diretorias_completas, veiculos_detalhados)
    
    # Salvar dados
    print("\n💾 Salvando dados expandidos...")
    salvar_dados_expandidos(diretorias_completas, veiculos_detalhados, relatorio)
    
    # Criar sugestões para modelos
    print("\n🔧 Criando sugestões para expansão dos modelos...")
    atualizar_modelos_flask()
    
    print(f"\n✅ EXPANSÃO COMPLETA! Resumo:")
    print(f"   📍 {relatorio['resumo_geral']['total_diretorias']} diretorias com dados completos")
    print(f"   🏫 {relatorio['resumo_geral']['total_escolas']} escolas processadas")
    print(f"   🚗 {relatorio['resumo_geral']['total_veiculos']} veículos catalogados")
    print(f"   👥 {relatorio['resumo_geral']['total_regioes_supervisao']} regiões de supervisão")

if __name__ == "__main__":
    main()
