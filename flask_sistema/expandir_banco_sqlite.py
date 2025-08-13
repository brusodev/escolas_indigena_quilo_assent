# -*- coding: utf-8 -*-
"""
Script Simplificado para Expandir Banco SQLite Existente
"""

import json
import sqlite3
import os
from datetime import date


def conectar_banco():
    """Conecta ao banco SQLite existente"""
    db_path = 'instance/escolas_sistema.db'
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return None

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_tabelas_expandidas(conn):
    """Cria tabelas expandidas no banco existente"""

    cursor = conn.cursor()

    # Tabela de estatísticas das diretorias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diretorias_estatisticas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        diretoria_nome TEXT NOT NULL,
        total_escolas INTEGER DEFAULT 0,
        escolas_indigenas INTEGER DEFAULT 0,
        escolas_quilombolas INTEGER DEFAULT 0,
        escolas_regulares INTEGER DEFAULT 0,
        total_veiculos INTEGER DEFAULT 0,
        veiculos_s1 INTEGER DEFAULT 0,
        veiculos_s2 INTEGER DEFAULT 0,
        veiculos_s2_4x4 INTEGER DEFAULT 0,
        supervisor TEXT,
        regiao_supervisao TEXT,
        cidade TEXT,
        endereco_completo TEXT,
        cep TEXT,
        codigo TEXT,
        capacidade_total_veiculos INTEGER DEFAULT 0,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Tabela de veículos detalhados
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS veiculos_detalhados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        diretoria_nome TEXT NOT NULL,
        tipo_veiculo TEXT NOT NULL,
        categoria TEXT,
        descricao TEXT,
        quantidade INTEGER DEFAULT 1,
        capacidade_estimada INTEGER DEFAULT 0,
        necessidade_especial BOOLEAN DEFAULT 0,
        ativo BOOLEAN DEFAULT 1,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Tabela de supervisores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS supervisores_completo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        regiao TEXT NOT NULL UNIQUE,
        diretorias_supervisionadas TEXT,
        quantidade_diretorias INTEGER DEFAULT 0,
        total_escolas INTEGER DEFAULT 0,
        total_veiculos INTEGER DEFAULT 0,
        email TEXT,
        telefone TEXT,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Tabela de estatísticas gerais
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estatisticas_sistema (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_referencia DATE NOT NULL,
        total_diretorias INTEGER DEFAULT 0,
        total_escolas INTEGER DEFAULT 0,
        total_veiculos INTEGER DEFAULT 0,
        total_supervisores INTEGER DEFAULT 0,
        escolas_indigenas INTEGER DEFAULT 0,
        escolas_quilombolas INTEGER DEFAULT 0,
        escolas_regulares INTEGER DEFAULT 0,
        veiculos_s1 INTEGER DEFAULT 0,
        veiculos_s2 INTEGER DEFAULT 0,
        veiculos_s2_4x4 INTEGER DEFAULT 0,
        capacidade_total_estimada INTEGER DEFAULT 0,
        diretoria_mais_escolas TEXT,
        quantidade_mais_escolas INTEGER DEFAULT 0,
        diretoria_menos_escolas TEXT,
        quantidade_menos_escolas INTEGER DEFAULT 0,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    print("✅ Tabelas expandidas criadas")


def popular_diretorias_estatisticas(conn, dados):
    """Popula estatísticas das diretorias"""

    cursor = conn.cursor()

    # Limpar dados anteriores
    cursor.execute("DELETE FROM diretorias_estatisticas")

    count = 0
    for nome, info in dados['diretorias'].items():
        # Dados de veículos
        veiculos_info = dados['veiculos'].get(nome, {})
        veiculos_por_tipo = veiculos_info.get('veiculos_por_tipo', {})

        cursor.execute('''
        INSERT INTO diretorias_estatisticas (
            diretoria_nome, total_escolas, escolas_indigenas, 
            escolas_quilombolas, escolas_regulares, total_veiculos,
            veiculos_s1, veiculos_s2, veiculos_s2_4x4,
            supervisor, regiao_supervisao, cidade, 
            endereco_completo, cep, codigo, capacidade_total_veiculos
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            nome,
            info['estatisticas']['total_escolas'],
            info['estatisticas']['escolas_indigenas'],
            info['estatisticas']['escolas_quilombolas'],
            info['estatisticas']['escolas_regulares'],
            veiculos_info.get('total_veiculos', 0),
            veiculos_por_tipo.get('S-1', {}).get('quantidade', 0),
            veiculos_por_tipo.get('S-2', {}).get('quantidade', 0),
            veiculos_por_tipo.get('S-2 4X4', {}).get('quantidade', 0),
            info.get('supervisor', ''),
            info.get('regiao_supervisao', ''),
            info.get('cidade', ''),
            info.get('endereco', ''),
            info.get('cep', ''),
            info.get('codigo', ''),
            veiculos_info.get('capacidade_total_estimada', 0)
        ))
        count += 1

    conn.commit()
    print(f"✅ {count} diretorias com estatísticas completas")


def popular_veiculos_detalhados(conn, dados):
    """Popula veículos detalhados"""

    cursor = conn.cursor()

    # Limpar dados anteriores
    cursor.execute("DELETE FROM veiculos_detalhados")

    count = 0
    for nome_diretoria, info_veiculos in dados['veiculos'].items():
        for tipo, info_tipo in info_veiculos.get('veiculos_por_tipo', {}).items():
            quantidade = info_tipo.get('quantidade', 0)

            if quantidade > 0:
                cursor.execute('''
                INSERT INTO veiculos_detalhados (
                    diretoria_nome, tipo_veiculo, categoria, descricao,
                    quantidade, capacidade_estimada, necessidade_especial
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    nome_diretoria,
                    tipo,
                    info_tipo.get('categoria', ''),
                    info_tipo.get('descricao', ''),
                    quantidade,
                    7 if tipo == 'S-1' else 15,  # Capacidade estimada
                    1 if '4X4' in tipo else 0    # Necessidade especial
                ))
                count += 1

    conn.commit()
    print(f"✅ {count} registros de veículos detalhados")


def popular_supervisores_completo(conn, dados):
    """Popula supervisores completos"""

    cursor = conn.cursor()

    # Limpar dados anteriores
    cursor.execute("DELETE FROM supervisores_completo")

    count = 0
    for regiao, info in dados['supervisao'].items():
        # Contar totais
        diretorias = info.get('diretorias', '').split('\n')
        diretorias = [d.strip() for d in diretorias if d.strip()]

        total_escolas = 0
        total_veiculos = 0

        for diretoria_nome in diretorias:
            if diretoria_nome in dados['diretorias']:
                total_escolas += dados['diretorias'][diretoria_nome]['estatisticas']['total_escolas']
            if diretoria_nome in dados['veiculos']:
                total_veiculos += dados['veiculos'][diretoria_nome]['total_veiculos']

        cursor.execute('''
        INSERT INTO supervisores_completo (
            nome, regiao, diretorias_supervisionadas,
            quantidade_diretorias, total_escolas, total_veiculos
        ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            info.get('supervisor', ''),
            regiao,
            info.get('diretorias', ''),
            len(diretorias),
            total_escolas,
            total_veiculos
        ))
        count += 1

    conn.commit()
    print(f"✅ {count} supervisores completos")


def popular_estatisticas_sistema(conn, dados):
    """Popula estatísticas do sistema"""

    cursor = conn.cursor()

    # Remover estatística do dia atual
    cursor.execute(
        "DELETE FROM estatisticas_sistema WHERE data_referencia = ?", (date.today(),))

    relatorio = dados['relatorio']

    # Encontrar extremos
    diretorias_escolas = relatorio.get('diretorias_com_mais_escolas', [])
    mais_escolas = diretorias_escolas[0] if diretorias_escolas else ('', 0)
    menos_escolas = diretorias_escolas[-1] if diretorias_escolas else ('', 0)

    cursor.execute('''
    INSERT INTO estatisticas_sistema (
        data_referencia, total_diretorias, total_escolas, total_veiculos,
        total_supervisores, escolas_indigenas, escolas_quilombolas,
        escolas_regulares, veiculos_s1, veiculos_s2, veiculos_s2_4x4,
        capacidade_total_estimada, diretoria_mais_escolas, quantidade_mais_escolas,
        diretoria_menos_escolas, quantidade_menos_escolas
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        date.today(),
        relatorio['resumo_geral']['total_diretorias'],
        relatorio['resumo_geral']['total_escolas'],
        relatorio['resumo_geral']['total_veiculos'],
        relatorio['resumo_geral']['total_regioes_supervisao'],
        relatorio['estatisticas_por_tipo']['escolas_indigenas'],
        relatorio['estatisticas_por_tipo']['escolas_quilombolas'],
        relatorio['estatisticas_por_tipo']['escolas_regulares'],
        relatorio['veiculos_por_tipo']['S-1'],
        relatorio['veiculos_por_tipo']['S-2'],
        relatorio['veiculos_por_tipo']['S-2_4X4'],
        (relatorio['veiculos_por_tipo']['S-1'] * 7 +
         relatorio['veiculos_por_tipo']['S-2'] * 15 +
         relatorio['veiculos_por_tipo']['S-2_4X4'] * 15),
        mais_escolas[0],
        mais_escolas[1],
        menos_escolas[0],
        menos_escolas[1]
    ))

    conn.commit()
    print(f"✅ Estatísticas do sistema atualizadas para {date.today()}")


def adicionar_colunas_tabelas_existentes(conn):
    """Adiciona colunas às tabelas existentes"""

    cursor = conn.cursor()

    # Lista de colunas para adicionar
    colunas_adicionar = [
        ("escolas", "codigo", "INTEGER"),
        ("escolas", "codigo_mec", "TEXT"),
        ("escolas", "zona", "TEXT"),
        ("escolas", "codigo_ibge", "INTEGER"),
        ("diretorias", "total_escolas", "INTEGER DEFAULT 0"),
        ("diretorias", "cidade", "TEXT"),
        ("diretorias", "cep", "TEXT"),
        ("diretorias", "codigo", "TEXT"),
        ("veiculos", "categoria", "TEXT"),
        ("veiculos", "capacidade_estimada", "INTEGER DEFAULT 0")
    ]

    for tabela, coluna, tipo in colunas_adicionar:
        try:
            cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo}")
            print(f"  ✅ Coluna {coluna} adicionada à tabela {tabela}")
        except sqlite3.OperationalError:
            # Coluna já existe
            pass

    conn.commit()


def main():
    """Função principal"""
    print("🔄 EXPANDINDO BANCO DE DADOS SQLite EXISTENTE")
    print("=" * 50)

    # Conectar ao banco
    conn = conectar_banco()
    if not conn:
        return

    # Carregar dados JSON
    print("\n📥 Carregando dados expandidos...")

    dados = {}

    try:
        with open('data/json_expandido/diretorias_completas.json', 'r', encoding='utf-8') as f:
            dados['diretorias'] = json.load(f)

        with open('data/json_expandido/veiculos_detalhados.json', 'r', encoding='utf-8') as f:
            dados['veiculos'] = json.load(f)

        with open('data/json_expandido/relatorio_completo.json', 'r', encoding='utf-8') as f:
            dados['relatorio'] = json.load(f)

        with open('../dados_supervisao_atualizados.json', 'r', encoding='utf-8') as f:
            dados['supervisao'] = json.load(f)

        print(
            f"✅ Dados carregados: {len(dados['diretorias'])} diretorias, {len(dados['veiculos'])} veículos, {len(dados['supervisao'])} supervisores")

    except FileNotFoundError as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return

    # Expandir banco
    print("\n🔧 Criando tabelas expandidas...")
    criar_tabelas_expandidas(conn)

    print("\n📝 Adicionando colunas às tabelas existentes...")
    adicionar_colunas_tabelas_existentes(conn)

    print("\n📊 Populando dados expandidos...")
    popular_diretorias_estatisticas(conn, dados)
    popular_veiculos_detalhados(conn, dados)
    popular_supervisores_completo(conn, dados)
    popular_estatisticas_sistema(conn, dados)

    # Verificar resultados
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM diretorias_estatisticas")
    total_dir_stats = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM veiculos_detalhados")
    total_veic_det = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM supervisores_completo")
    total_sup = cursor.fetchone()[0]

    conn.close()

    print(f"\n✅ BANCO DE DADOS EXPANDIDO COM SUCESSO!")
    print(f"   📍 {total_dir_stats} diretorias com estatísticas completas")
    print(f"   🚗 {total_veic_det} registros de veículos detalhados")
    print(f"   👥 {total_sup} supervisores completos")
    print(f"   📊 Estatísticas do sistema atualizadas")
    print(f"\n🎯 O banco agora possui informações completas e detalhadas!")


if __name__ == "__main__":
    main()
