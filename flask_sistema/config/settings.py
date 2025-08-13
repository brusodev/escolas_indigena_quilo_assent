# -*- coding: utf-8 -*-
"""
Configurações do Sistema Flask
"""

import os
from pathlib import Path


class Config:
    """Configuração base"""
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Diretório base do projeto
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    JSON_DIR = DATA_DIR / 'json'

    # Configurações da aplicação
    ITEMS_PER_PAGE = 50
    MAX_UPLOAD_SIZE = 16 * 1024 * 1024  # 16MB

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    # SQLite para desenvolvimento (fácil setup)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{Config.BASE_DIR}/data/escolas_sistema.db'


class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://sistema_escolas:senha123@localhost:5432/escolas_sistema'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Log para syslog em produção
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
