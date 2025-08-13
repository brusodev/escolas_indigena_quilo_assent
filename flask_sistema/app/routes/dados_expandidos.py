# -*- coding: utf-8 -*-
"""
Rotas para Dados Expandidos - API Completa
"""

from flask import Blueprint, jsonify, request, render_template
import sqlite3
import os

dados_expandidos_bp = Blueprint('dados_expandidos', __name__)


def get_db_connection():
    """Conecta ao banco SQLite"""
    db_path = os.path.join('instance', 'escolas_sistema.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@dados_expandidos_bp.route('/completo')
def dashboard_completo():
    """Página do dashboard completo"""
    return render_template('dashboard/completo.html')


@dados_expandidos_bp.route('/api/diretorias/completas')
def diretorias_completas():
    """Retorna dados completos das diretorias com estatísticas"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM diretorias_estatisticas 
        ORDER BY total_escolas DESC
        ''')

        diretorias = []
        for row in cursor.fetchall():
            diretorias.append({
                'id': row['id'],
                'nome': row['diretoria_nome'],
                'total_escolas': row['total_escolas'],
                'escolas_indigenas': row['escolas_indigenas'],
                'escolas_quilombolas': row['escolas_quilombolas'],
                'escolas_regulares': row['escolas_regulares'],
                'total_veiculos': row['total_veiculos'],
                'veiculos_s1': row['veiculos_s1'],
                'veiculos_s2': row['veiculos_s2'],
                'veiculos_s2_4x4': row['veiculos_s2_4x4'],
                'supervisor': row['supervisor'],
                'regiao_supervisao': row['regiao_supervisao'],
                'cidade': row['cidade'],
                'endereco_completo': row['endereco_completo'],
                'cep': row['cep'],
                'codigo': row['codigo'],
                'capacidade_total_veiculos': row['capacidade_total_veiculos']
            })

        conn.close()

        return jsonify({
            'status': 'success',
            'total': len(diretorias),
            'diretorias': diretorias
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@dados_expandidos_bp.route('/api/diretorias/<nome>/detalhes')
def diretoria_detalhes(nome):
    """Retorna detalhes completos de uma diretoria específica"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Dados da diretoria
        cursor.execute('''
        SELECT * FROM diretorias_estatisticas 
        WHERE diretoria_nome = ?
        ''', (nome,))

        diretoria = cursor.fetchone()
        if not diretoria:
            return jsonify({'status': 'error', 'message': 'Diretoria não encontrada'}), 404

        # Veículos da diretoria
        cursor.execute('''
        SELECT * FROM veiculos_detalhados 
        WHERE diretoria_nome = ?
        ''', (nome,))

        veiculos = []
        for row in cursor.fetchall():
            veiculos.append({
                'tipo': row['tipo_veiculo'],
                'categoria': row['categoria'],
                'descricao': row['descricao'],
                'quantidade': row['quantidade'],
                'capacidade_estimada': row['capacidade_estimada'],
                'necessidade_especial': bool(row['necessidade_especial'])
            })

        # Escolas da diretoria
        cursor.execute('''
        SELECT nome, tipo, cidade, latitude, longitude, endereco
        FROM escolas 
        WHERE diretoria = ?
        ORDER BY tipo, nome
        ''', (nome,))

        escolas = []
        for row in cursor.fetchall():
            escolas.append({
                'nome': row['nome'],
                'tipo': row['tipo'],
                'cidade': row['cidade'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'endereco': row['endereco']
            })

        conn.close()

        return jsonify({
            'status': 'success',
            'diretoria': {
                'nome': diretoria['diretoria_nome'],
                'total_escolas': diretoria['total_escolas'],
                'escolas_indigenas': diretoria['escolas_indigenas'],
                'escolas_quilombolas': diretoria['escolas_quilombolas'],
                'escolas_regulares': diretoria['escolas_regulares'],
                'supervisor': diretoria['supervisor'],
                'regiao_supervisao': diretoria['regiao_supervisao'],
                'endereco_completo': diretoria['endereco_completo'],
                'total_veiculos': diretoria['total_veiculos'],
                'capacidade_total_veiculos': diretoria['capacidade_total_veiculos'],
                'veiculos': veiculos,
                'escolas': escolas
            }
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@dados_expandidos_bp.route('/api/veiculos/detalhados')
def veiculos_detalhados():
    """Retorna informações detalhadas dos veículos por diretoria"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT diretoria_nome, tipo_veiculo, categoria, descricao,
               SUM(quantidade) as total_quantidade,
               capacidade_estimada, necessidade_especial
        FROM veiculos_detalhados 
        GROUP BY diretoria_nome, tipo_veiculo
        ORDER BY diretoria_nome, tipo_veiculo
        ''')

        veiculos = {}
        for row in cursor.fetchall():
            diretoria = row['diretoria_nome']
            if diretoria not in veiculos:
                veiculos[diretoria] = {
                    'nome': diretoria,
                    'veiculos': [],
                    'total_veiculos': 0,
                    'capacidade_total': 0
                }

            veiculo_info = {
                'tipo': row['tipo_veiculo'],
                'categoria': row['categoria'],
                'descricao': row['descricao'],
                'quantidade': row['total_quantidade'],
                'capacidade_estimada': row['capacidade_estimada'],
                'necessidade_especial': bool(row['necessidade_especial']),
                'capacidade_total': row['total_quantidade'] * row['capacidade_estimada']
            }

            veiculos[diretoria]['veiculos'].append(veiculo_info)
            veiculos[diretoria]['total_veiculos'] += row['total_quantidade']
            veiculos[diretoria]['capacidade_total'] += veiculo_info['capacidade_total']

        conn.close()

        return jsonify({
            'status': 'success',
            'total_diretorias': len(veiculos),
            'veiculos_por_diretoria': list(veiculos.values())
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@dados_expandidos_bp.route('/api/supervisores/completos')
def supervisores_completos():
    """Retorna informações completas dos supervisores"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM supervisores_completo 
        ORDER BY total_escolas DESC
        ''')

        supervisores = []
        for row in cursor.fetchall():
            # Processar diretorias supervisionadas
            diretorias_lista = []
            if row['diretorias_supervisionadas']:
                diretorias_lista = [
                    d.strip() for d in row['diretorias_supervisionadas'].split('\n') if d.strip()]

            supervisores.append({
                'nome': row['nome'],
                'regiao': row['regiao'],
                'diretorias_supervisionadas': diretorias_lista,
                'quantidade_diretorias': row['quantidade_diretorias'],
                'total_escolas': row['total_escolas'],
                'total_veiculos': row['total_veiculos'],
                'email': row['email'],
                'telefone': row['telefone']
            })

        conn.close()

        return jsonify({
            'status': 'success',
            'total': len(supervisores),
            'supervisores': supervisores
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@dados_expandidos_bp.route('/api/estatisticas/sistema')
def estatisticas_sistema():
    """Retorna estatísticas completas do sistema"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Estatísticas mais recentes
        cursor.execute('''
        SELECT * FROM estatisticas_sistema 
        ORDER BY data_referencia DESC 
        LIMIT 1
        ''')

        stats = cursor.fetchone()
        if not stats:
            return jsonify({'status': 'error', 'message': 'Estatísticas não encontradas'}), 404

        # Top 10 diretorias por número de escolas
        cursor.execute('''
        SELECT diretoria_nome, total_escolas, total_veiculos,
               escolas_indigenas, escolas_quilombolas, escolas_regulares
        FROM diretorias_estatisticas 
        ORDER BY total_escolas DESC 
        LIMIT 10
        ''')

        top_diretorias = []
        for row in cursor.fetchall():
            top_diretorias.append({
                'nome': row['diretoria_nome'],
                'total_escolas': row['total_escolas'],
                'total_veiculos': row['total_veiculos'],
                'escolas_indigenas': row['escolas_indigenas'],
                'escolas_quilombolas': row['escolas_quilombolas'],
                'escolas_regulares': row['escolas_regulares']
            })

        # Distribuição de veículos por tipo
        cursor.execute('''
        SELECT tipo_veiculo, SUM(quantidade) as total
        FROM veiculos_detalhados 
        GROUP BY tipo_veiculo
        ''')

        distribuicao_veiculos = {}
        for row in cursor.fetchall():
            distribuicao_veiculos[row['tipo_veiculo']] = row['total']

        conn.close()

        return jsonify({
            'status': 'success',
            'data_referencia': stats['data_referencia'],
            'totais_gerais': {
                'diretorias': stats['total_diretorias'],
                'escolas': stats['total_escolas'],
                'veiculos': stats['total_veiculos'],
                'supervisores': stats['total_supervisores'],
                'capacidade_total_estimada': stats['capacidade_total_estimada']
            },
            'distribuicao_escolas': {
                'indigenas': stats['escolas_indigenas'],
                'quilombolas': stats['escolas_quilombolas'],
                'regulares': stats['escolas_regulares']
            },
            'distribuicao_veiculos': distribuicao_veiculos,
            'extremos': {
                'diretoria_mais_escolas': {
                    'nome': stats['diretoria_mais_escolas'],
                    'quantidade': stats['quantidade_mais_escolas']
                },
                'diretoria_menos_escolas': {
                    'nome': stats['diretoria_menos_escolas'],
                    'quantidade': stats['quantidade_menos_escolas']
                }
            },
            'top_diretorias': top_diretorias
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@dados_expandidos_bp.route('/api/relatorio/completo')
def relatorio_completo():
    """Retorna relatório completo do sistema"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Resumo geral
        cursor.execute('SELECT COUNT(*) as total FROM diretorias_estatisticas')
        total_diretorias = cursor.fetchone()['total']

        cursor.execute(
            'SELECT SUM(total_escolas) as total FROM diretorias_estatisticas')
        total_escolas = cursor.fetchone()['total']

        cursor.execute(
            'SELECT SUM(quantidade) as total FROM veiculos_detalhados')
        total_veiculos = cursor.fetchone()['total']

        cursor.execute('SELECT COUNT(*) as total FROM supervisores_completo')
        total_supervisores = cursor.fetchone()['total']

        # Escolas por tipo
        cursor.execute('''
        SELECT SUM(escolas_indigenas) as indigenas,
               SUM(escolas_quilombolas) as quilombolas,
               SUM(escolas_regulares) as regulares
        FROM diretorias_estatisticas
        ''')
        tipos_escolas = cursor.fetchone()

        # Distribuição geográfica
        cursor.execute('''
        SELECT regiao_supervisao, COUNT(*) as diretorias,
               SUM(total_escolas) as escolas, SUM(total_veiculos) as veiculos
        FROM diretorias_estatisticas 
        WHERE regiao_supervisao IS NOT NULL AND regiao_supervisao != ''
        GROUP BY regiao_supervisao
        ORDER BY escolas DESC
        ''')

        distribuicao_geografica = []
        for row in cursor.fetchall():
            distribuicao_geografica.append({
                'regiao': row['regiao_supervisao'],
                'diretorias': row['diretorias'],
                'escolas': row['escolas'],
                'veiculos': row['veiculos']
            })

        conn.close()

        return jsonify({
            'status': 'success',
            'resumo_executivo': {
                'total_diretorias': total_diretorias,
                'total_escolas': total_escolas or 0,
                'total_veiculos': total_veiculos or 0,
                'total_supervisores': total_supervisores,
                'media_escolas_por_diretoria': round((total_escolas or 0) / max(total_diretorias, 1), 2),
                'media_veiculos_por_diretoria': round((total_veiculos or 0) / max(total_diretorias, 1), 2)
            },
            'distribuicao_tipos_escolas': {
                'indigenas': tipos_escolas['indigenas'] or 0,
                'quilombolas': tipos_escolas['quilombolas'] or 0,
                'regulares': tipos_escolas['regulares'] or 0
            },
            'distribuicao_geografica': distribuicao_geografica
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
