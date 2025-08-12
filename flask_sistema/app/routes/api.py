# -*- coding: utf-8 -*-
"""
API REST para dados
"""

from flask import Blueprint, jsonify
from app.models import Escola, Diretoria, Veiculo, Supervisor

bp_api = Blueprint('api', __name__)


@bp_api.route('/escolas')
def api_escolas():
    """API: Lista todas as escolas"""
    escolas = Escola.query.all()
    return jsonify([escola.to_dict() for escola in escolas])


@bp_api.route('/diretorias')
def api_diretorias():
    """API: Lista todas as diretorias"""
    diretorias = Diretoria.query.all()
    return jsonify([diretoria.to_dict() for diretoria in diretorias])


@bp_api.route('/veiculos')
def api_veiculos():
    """API: Lista todos os veículos"""
    veiculos = Veiculo.query.all()
    return jsonify([veiculo.to_dict() for veiculo in veiculos])


@bp_api.route('/supervisores')
def api_supervisores():
    """API: Lista todos os supervisores"""
    supervisores = Supervisor.query.filter_by(ativo=True).all()
    return jsonify([supervisor.to_dict() for supervisor in supervisores])
