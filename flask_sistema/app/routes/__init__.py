# -*- coding: utf-8 -*-
"""
Registro de Blueprints - Sistema Flask
"""


def register_blueprints(app):
    """Registra todos os blueprints da aplicação"""

    # Importar blueprints
    from .escolas import bp_escolas
    from .diretorias import bp_diretorias
    from .veiculos import bp_veiculos
    from .api import bp_api
    from .dashboard import bp_dashboard
    from .dados_expandidos import dados_expandidos_bp
    from .teste_91_diretorias import bp_91_diretorias

    # Registrar blueprints
    app.register_blueprint(bp_escolas, url_prefix='/escolas')
    app.register_blueprint(bp_diretorias, url_prefix='/diretorias')
    app.register_blueprint(bp_veiculos, url_prefix='/veiculos')
    app.register_blueprint(bp_api, url_prefix='/api')
    app.register_blueprint(bp_dashboard, url_prefix='/')
    app.register_blueprint(dados_expandidos_bp, url_prefix='/')
    app.register_blueprint(bp_91_diretorias, url_prefix='/')

    # Rota de health check
    @app.route('/health')
    def health():
        return {'status': 'ok', 'message': 'Sistema funcionando'}
