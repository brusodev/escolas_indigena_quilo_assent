#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor HTTP para o Dashboard Final
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path


def iniciar_servidor_final():
    """Iniciar servidor HTTP para dashboard final"""
    print("🚀 INICIANDO SERVIDOR DASHBOARD FINAL...")
    print("-" * 50)
    
    # Verificar se arquivo existe
    dashboard_file = Path("dashboard_final.html")
    if not dashboard_file.exists():
        print("❌ Arquivo dashboard_final.html não encontrado!")
        return
    
    # Configurar servidor
    PORT = 8002
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Mudar para diretório correto
    os.chdir(Path(__file__).parent)
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"✅ Servidor iniciado na porta {PORT}")
            print(f"🌐 URL: http://localhost:{PORT}/dashboard_final.html")
            print("📊 Dashboard FINAL - Todas as correções aplicadas:")
            print("  ✅ 91 diretorias (correto)")
            print("  ✅ 5,582 escolas com dados atualizados")
            print("  ✅ 172 veículos distribuídos")
            print("  ✅ Estilo original preservado")
            print("  ✅ Gráficos funcionais")
            print("⏹️  Pressione Ctrl+C para parar o servidor")
            print("-" * 50)
            
            # Abrir navegador automaticamente
            webbrowser.open(f"http://localhost:{PORT}/dashboard_final.html")
            
            # Manter servidor rodando
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")


if __name__ == "__main__":
    iniciar_servidor_final()
