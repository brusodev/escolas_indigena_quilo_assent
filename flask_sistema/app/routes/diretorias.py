# -*- coding: utf-8 -*-
"""
Rotas para Diretorias
"""

from flask import Blueprint, jsonify, request
from app.models import Diretoria

bp_diretorias = Blueprint('diretorias', __name__)


@bp_diretorias.route('/')
def index():
    """Lista todas as diretorias"""
    diretorias = Diretoria.query.all()
    return jsonify([diretoria.to_dict() for diretoria in diretorias])


@bp_diretorias.route('/<int:diretoria_id>')
def get_diretoria(diretoria_id):
    """Busca diretoria por ID"""
    diretoria = Diretoria.query.get_or_404(diretoria_id)
    return jsonify(diretoria.to_dict())


@bp_diretorias.route('/<int:diretoria_id>/escolas')
def escolas_da_diretoria(diretoria_id):
    """Lista escolas de uma diretoria"""
    diretoria = Diretoria.query.get_or_404(diretoria_id)
    escolas = diretoria.escolas.all()
    return jsonify([escola.to_dict() for escola in escolas])
