#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicação Flask - Configuração Principal
Sistema de Gestão de Escolas, Diretorias e Transporte
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar extensões
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)

    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',
                                              'dev-secret-key-change-in-production')

    # SQLite para desenvolvimento, PostgreSQL para produção
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'sqlite:///escolas_sistema.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Criar diretório data se não existir
    import pathlib
    data_dir = pathlib.Path(app.instance_path).parent / 'data'
    data_dir.mkdir(exist_ok=True)

    # Inicializar extensões com app
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
