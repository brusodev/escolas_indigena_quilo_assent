# -*- coding: utf-8 -*-
"""
Rotas para Escolas
"""

from flask import Blueprint, jsonify, request
from app import db
from app.models import Escola

bp_escolas = Blueprint('escolas', __name__)


@bp_escolas.route('/')
def index():
    """Lista todas as escolas"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    escolas = Escola.query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'escolas': [escola.to_dict() for escola in escolas.items],
        'total': escolas.total,
        'pages': escolas.pages,
        'current_page': page
    })


@bp_escolas.route('/<int:escola_id>')
def get_escola(escola_id):
    """Busca escola por ID"""
    escola = Escola.query.get_or_404(escola_id)
    return jsonify(escola.to_dict())


@bp_escolas.route('/tipo/<tipo>')
def por_tipo(tipo):
    """Busca escolas por tipo"""
    escolas = Escola.get_by_tipo(tipo)
    return jsonify([escola.to_dict() for escola in escolas])
