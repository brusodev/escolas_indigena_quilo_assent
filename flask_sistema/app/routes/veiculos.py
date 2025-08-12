# -*- coding: utf-8 -*-
"""
Rotas para Veículos
"""

from flask import Blueprint, jsonify
from app.models import Veiculo

bp_veiculos = Blueprint('veiculos', __name__)


@bp_veiculos.route('/')
def index():
    """Lista todos os veículos"""
    veiculos = Veiculo.query.all()
    return jsonify([veiculo.to_dict() for veiculo in veiculos])


@bp_veiculos.route('/<int:veiculo_id>')
def get_veiculo(veiculo_id):
    """Busca veículo por ID"""
    veiculo = Veiculo.query.get_or_404(veiculo_id)
    return jsonify(veiculo.to_dict())


@bp_veiculos.route('/tipo/<tipo>')
def por_tipo(tipo):
    """Busca veículos por tipo"""
    veiculos = Veiculo.get_by_tipo(tipo)
    return jsonify([veiculo.to_dict() for veiculo in veiculos])
