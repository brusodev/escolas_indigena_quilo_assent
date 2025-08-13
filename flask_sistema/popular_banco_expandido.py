# -*- coding: utf-8 -*-
"""
Script para Popular Banco de Dados Expandido com Informações Completas
"""

from app.models.models_expandidos import (
    db, Diretoria, Escola, Veiculo, Supervisor, Distancia, EstatisticasGerais
)
from app import create_app
import json
import sys
import os
from datetime import datetime, date

# Adicionar o diretório pai ao path para importar os modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def carregar_dados_json():
    """Carrega dados dos arquivos JSON expandidos"""

    # Caminhos dos arquivos
    base_path = 'data/json_expandido'

    dados = {}

    # Carregar diretorias completas
    try:
        with open(f'{base_path}/diretorias_completas.json', 'r', encoding='utf-8') as f:
            dados['diretorias'] = json.load(f)
        print(f"✅ Carregadas {len(dados['diretorias'])} diretorias completas")
    except FileNotFoundError:
        print("❌ Arquivo de diretorias completas não encontrado")
        return None

    # Carregar veículos detalhados
    try:
        with open(f'{base_path}/veiculos_detalhados.json', 'r', encoding='utf-8') as f:
            dados['veiculos'] = json.load(f)
        print(
            f"✅ Carregados dados de veículos para {len(dados['veiculos'])} diretorias")
    except FileNotFoundError:
        print("❌ Arquivo de veículos detalhados não encontrado")
        return None

    # Carregar relatório completo
    try:
        with open(f'{base_path}/relatorio_completo.json', 'r', encoding='utf-8') as f:
            dados['relatorio'] = json.load(f)
        print(f"✅ Carregado relatório completo")
    except FileNotFoundError:
        print("❌ Arquivo de relatório completo não encontrado")
        return None

    # Carregar dados de supervisão originais
    try:
        with open('../dados_supervisao_atualizados.json', 'r', encoding='utf-8') as f:
            dados['supervisao'] = json.load(f)
        print(
            f"✅ Carregados dados de supervisão para {len(dados['supervisao'])} regiões")
    except FileNotFoundError:
        print("❌ Arquivo de supervisão não encontrado")
        dados['supervisao'] = {}

    return dados


def popular_diretorias(dados):
    """Popula tabela de diretorias com dados completos"""
    print("\n📍 Populando diretorias...")

    count = 0
    for nome, info in dados['diretorias'].items():
        # Verificar se já existe
        diretoria_existente = Diretoria.query.filter_by(nome=nome).first()
        if diretoria_existente:
            continue

        # Criar nova diretoria
        diretoria = Diretoria(
            nome=nome,
            endereco=info.get('endereco', ''),
            cidade=info.get('cidade', ''),
            cep=info.get('cep', ''),
            latitude=info.get('coordenadas', {}).get('latitude'),
            longitude=info.get('coordenadas', {}).get('longitude'),
            codigo=info.get('codigo', ''),
            total_escolas=info['estatisticas']['total_escolas'],
            escolas_indigenas=info['estatisticas']['escolas_indigenas'],
            escolas_quilombolas=info['estatisticas']['escolas_quilombolas'],
            escolas_regulares=info['estatisticas']['escolas_regulares'],
            supervisor=info.get('supervisor', ''),
            regiao_supervisao=info.get('regiao_supervisao', ''),
            total_veiculos=len([v for v in dados['veiculos'].get(nome, {}).get(
                'veiculos_por_tipo', {}).values() if v.get('quantidade', 0) > 0])
        )

        db.session.add(diretoria)
        count += 1

    db.session.commit()
    print(f"✅ {count} diretorias adicionadas")
    return count


def popular_escolas(dados):
    """Popula tabela de escolas com dados completos"""
    print("\n🏫 Populando escolas...")

    count = 0
    diretorias_map = {d.nome: d.id for d in Diretoria.query.all()}

    for nome_diretoria, info_diretoria in dados['diretorias'].items():
        diretoria_id = diretorias_map.get(nome_diretoria)
        if not diretoria_id:
            continue

        for escola_info in info_diretoria.get('escolas', []):
            # Verificar se já existe (por código MEC se disponível)
            codigo_mec = escola_info.get('codigo_mec')
            if codigo_mec:
                escola_existente = Escola.query.filter_by(
                    codigo_mec=codigo_mec).first()
                if escola_existente:
                    continue

            # Criar nova escola
            escola = Escola(
                nome=escola_info.get('nome', ''),
                codigo=escola_info.get('codigo'),
                codigo_mec=codigo_mec,
                tipo=escola_info.get('tipo', 'regular'),
                zona=escola_info.get('zona', ''),
                cidade=escola_info.get('cidade', ''),
                endereco=escola_info.get('endereco', ''),
                latitude=escola_info.get('latitude'),
                longitude=escola_info.get('longitude'),
                diretoria_id=diretoria_id,
                diretoria_nome=nome_diretoria,
                distancia_diretoria=escola_info.get('distancia', 0)
            )

            db.session.add(escola)
            count += 1

    db.session.commit()
    print(f"✅ {count} escolas adicionadas")
    return count


def popular_veiculos(dados):
    """Popula tabela de veículos com dados detalhados"""
    print("\n🚗 Populando veículos...")

    count = 0
    diretorias_map = {d.nome: d.id for d in Diretoria.query.all()}

    # Mapear tipos de veículos
    tipos_veiculo = {
        'S-1': {
            'categoria': 'pequeno',
            'descricao': 'Veículo pequeno (até 7 lugares)',
            'capacidade': 7,
            'especial': False
        },
        'S-2': {
            'categoria': 'medio_grande',
            'descricao': 'Veículo médio/grande (8+ lugares)',
            'capacidade': 15,
            'especial': False
        },
        'S-2 4X4': {
            'categoria': 'medio_grande_4x4',
            'descricao': 'Veículo médio/grande com tração 4x4',
            'capacidade': 15,
            'especial': True
        }
    }

    for nome_diretoria, info_veiculos in dados['veiculos'].items():
        diretoria_id = diretorias_map.get(nome_diretoria)
        if not diretoria_id:
            continue

        for tipo, info_tipo in info_veiculos.get('veiculos_por_tipo', {}).items():
            quantidade = info_tipo.get('quantidade', 0)

            # Criar um registro para cada veículo
            for i in range(quantidade):
                tipo_info = tipos_veiculo.get(tipo, {})

                veiculo = Veiculo(
                    diretoria_id=diretoria_id,
                    diretoria_nome=nome_diretoria,
                    tipo=tipo,
                    categoria=tipo_info.get('categoria', ''),
                    descricao=tipo_info.get('descricao', ''),
                    capacidade_estimada=tipo_info.get('capacidade', 0),
                    necessidade_especial=tipo_info.get('especial', False),
                    quantidade=1
                )

                db.session.add(veiculo)
                count += 1

    db.session.commit()
    print(f"✅ {count} veículos adicionados")
    return count


def popular_supervisores(dados):
    """Popula tabela de supervisores"""
    print("\n👥 Populando supervisores...")

    count = 0

    for regiao, info in dados['supervisao'].items():
        # Verificar se já existe
        supervisor_existente = Supervisor.query.filter_by(
            regiao=regiao).first()
        if supervisor_existente:
            continue

        # Contar diretorias
        diretorias = info.get('diretorias', '').split('\n')
        diretorias = [d.strip() for d in diretorias if d.strip()]

        # Calcular totais
        total_escolas = 0
        total_veiculos = 0

        for diretoria_nome in diretorias:
            if diretoria_nome in dados['diretorias']:
                total_escolas += dados['diretorias'][diretoria_nome]['estatisticas']['total_escolas']
            if diretoria_nome in dados['veiculos']:
                total_veiculos += dados['veiculos'][diretoria_nome]['total_veiculos']

        supervisor = Supervisor(
            nome=info.get('supervisor', ''),
            regiao=regiao,
            diretorias_supervisionadas=info.get('diretorias', ''),
            quantidade_diretorias=len(diretorias),
            total_escolas=total_escolas,
            total_veiculos=total_veiculos
        )

        db.session.add(supervisor)
        count += 1

    db.session.commit()
    print(f"✅ {count} supervisores adicionados")
    return count


def popular_estatisticas(dados):
    """Popula tabela de estatísticas gerais"""
    print("\n📊 Populando estatísticas gerais...")

    relatorio = dados['relatorio']

    # Remover estatística do dia atual se existir
    EstatisticasGerais.query.filter_by(data_referencia=date.today()).delete()

    # Encontrar diretoria com mais e menos escolas
    diretorias_escolas = relatorio.get('diretorias_com_mais_escolas', [])
    mais_escolas = diretorias_escolas[0] if diretorias_escolas else ('', 0)
    menos_escolas = diretorias_escolas[-1] if diretorias_escolas else ('', 0)

    estatistica = EstatisticasGerais(
        data_referencia=date.today(),
        total_diretorias=relatorio['resumo_geral']['total_diretorias'],
        total_escolas=relatorio['resumo_geral']['total_escolas'],
        total_veiculos=relatorio['resumo_geral']['total_veiculos'],
        total_supervisores=relatorio['resumo_geral']['total_regioes_supervisao'],
        escolas_indigenas=relatorio['estatisticas_por_tipo']['escolas_indigenas'],
        escolas_quilombolas=relatorio['estatisticas_por_tipo']['escolas_quilombolas'],
        escolas_regulares=relatorio['estatisticas_por_tipo']['escolas_regulares'],
        veiculos_s1=relatorio['veiculos_por_tipo']['S-1'],
        veiculos_s2=relatorio['veiculos_por_tipo']['S-2'],
        veiculos_s2_4x4=relatorio['veiculos_por_tipo']['S-2_4X4'],
        capacidade_total_veiculos=(
            relatorio['veiculos_por_tipo']['S-1'] * 7 +
            relatorio['veiculos_por_tipo']['S-2'] * 15 +
            relatorio['veiculos_por_tipo']['S-2_4X4'] * 15
        ),
        diretoria_mais_escolas=mais_escolas[0],
        quantidade_maior=mais_escolas[1],
        diretoria_menos_escolas=menos_escolas[0],
        quantidade_menor=menos_escolas[1]
    )

    db.session.add(estatistica)
    db.session.commit()
    print(f"✅ Estatísticas do dia {date.today()} adicionadas")


def criar_tabelas_expandidas(app):
    """Cria todas as tabelas expandidas"""
    print("\n🔧 Criando tabelas expandidas...")

    from app.models.models_expandidos import db as db_expandido

    # Inicializar o db expandido com a app
    db_expandido.init_app(app)

    with app.app_context():
        # Criar todas as tabelas (sem remover as existentes)
        db_expandido.create_all()

    print("✅ Tabelas expandidas criadas")


def main():
    """Função principal"""
    print("🔄 POPULANDO BANCO DE DADOS EXPANDIDO")
    print("=" * 50)

    # Criar aplicação Flask
    app = create_app()

    with app.app_context():
        # Carregar dados
        print("📥 Carregando dados...")
        dados = carregar_dados_json()
        if not dados:
            print("❌ Falha ao carregar dados")
            return

        # Criar tabelas
        criar_tabelas_expandidas(app)

        # Popular dados
        total_diretorias = popular_diretorias(dados)
        total_escolas = popular_escolas(dados)
        total_veiculos = popular_veiculos(dados)
        total_supervisores = popular_supervisores(dados)
        popular_estatisticas(dados)

        print(f"\n✅ BANCO DE DADOS EXPANDIDO POPULADO COM SUCESSO!")
        print(f"   📍 {total_diretorias} diretorias")
        print(f"   🏫 {total_escolas} escolas")
        print(f"   🚗 {total_veiculos} veículos")
        print(f"   👥 {total_supervisores} supervisores")
        print(f"   📊 Estatísticas atualizadas")


if __name__ == "__main__":
    main()
