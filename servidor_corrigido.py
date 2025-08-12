#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor HTTP para o Dashboard Corrigido
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path


def iniciar_servidor_corrigido():
    """Iniciar servidor HTTP para dashboard corrigido"""
    print("🚀 INICIANDO SERVIDOR DASHBOARD CORRIGIDO...")
    print("-" * 50)
    
    # Verificar se arquivo existe
    dashboard_file = Path("dashboard_corrigido.html")
    if not dashboard_file.exists():
        print("❌ Arquivo dashboard_corrigido.html não encontrado!")
        return
    
    # Configurar servidor
    PORT = 8001
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Mudar para diretório correto
    os.chdir(Path(__file__).parent)
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"✅ Servidor iniciado na porta {PORT}")
            print(f"🌐 URL do Dashboard: http://localhost:{PORT}/dashboard_corrigido.html")
            print("📊 Dashboard com 91 diretorias e dados completos")
            print("⏹️  Pressione Ctrl+C para parar o servidor")
            print("-" * 50)
            
            # Abrir navegador automaticamente
            webbrowser.open(f"http://localhost:{PORT}/dashboard_corrigido.html")
            
            # Manter servidor rodando
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")


if __name__ == "__main__":
    iniciar_servidor_corrigido()
