# -*- coding: utf-8 -*-
"""
Rotas para Dashboard Principal
"""

from flask import Blueprint, render_template, jsonify
from app import db
from app.models import Escola, Diretoria, Veiculo, Supervisor
from sqlalchemy import func

bp_dashboard = Blueprint('dashboard', __name__)


@bp_dashboard.route('/')
def index():
    """Página principal do dashboard"""
    # Estatísticas básicas
    stats = {
        'total_escolas': Escola.query.count(),
        'total_diretorias': Diretoria.query.count(),
        'total_veiculos': Veiculo.query.count(),
        'total_supervisores': Supervisor.query.filter_by(ativo=True).count()
    }

    # Escolas por tipo
    escolas_por_tipo = db.session.query(
        Escola.tipo,
        func.count(Escola.id).label('total')
    ).group_by(Escola.tipo).all()

    stats['escolas_por_tipo'] = {tipo: total
                                 for tipo, total in escolas_por_tipo}

    return render_template('dashboard/index.html', stats=stats)


@bp_dashboard.route('/mapa')
def mapa():
    """Página do mapa interativo"""
    return render_template('dashboard/mapa.html')


@bp_dashboard.route('/dados/escolas')
def dados_escolas():
    """API para dados das escolas (JSON)"""
    escolas = Escola.query.all()
    return jsonify([escola.to_dict() for escola in escolas])


@bp_dashboard.route('/dados/diretorias')
def dados_diretorias():
    """API para dados das diretorias (JSON)"""
    diretorias = Diretoria.query.all()
    return jsonify([diretoria.to_dict() for diretoria in diretorias])


@bp_dashboard.route('/dados/veiculos')
def dados_veiculos():
    """API para dados dos veículos (JSON)"""
    veiculos = Veiculo.query.all()
    return jsonify([veiculo.to_dict() for veiculo in veiculos])


@bp_dashboard.route('/dados/estatisticas')
def estatisticas():
    """API para estatísticas gerais"""

    # Estatísticas básicas
    stats = {
        'total_escolas': Escola.query.count(),
        'total_diretorias': Diretoria.query.count(),
        'total_veiculos': Veiculo.query.count(),
        'total_supervisores': Supervisor.query.filter_by(ativo=True).count()
    }

    # Escolas por tipo
    escolas_por_tipo = db.session.query(
        Escola.tipo,
        func.count(Escola.id).label('total')
    ).group_by(Escola.tipo).all()

    stats['escolas_por_tipo'] = {tipo: total
                                 for tipo, total in escolas_por_tipo}

    # Veículos por tipo
    veiculos_por_tipo = db.session.query(
        Veiculo.tipo,
        func.count(Veiculo.id).label('total')
    ).group_by(Veiculo.tipo).all()

    stats['veiculos_por_tipo'] = {tipo: total
                                  for tipo, total in veiculos_por_tipo}

    # Diretorias com mais escolas
    diretorias_top = db.session.query(
        Diretoria.nome,
        func.count(Escola.id).label('total_escolas')
    ).join(Escola).group_by(Diretoria.nome).order_by(
        func.count(Escola.id).desc()
    ).limit(10).all()

    stats['diretorias_top'] = [
        {'nome': nome, 'total_escolas': total}
        for nome, total in diretorias_top
    ]

    return jsonify(stats)
