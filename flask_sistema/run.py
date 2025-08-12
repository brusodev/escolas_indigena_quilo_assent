#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ponto de entrada da aplicação Flask
Sistema de Gestão de Escolas, Diretorias e Transporte
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
