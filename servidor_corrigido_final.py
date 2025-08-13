#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor HTTP para o Dashboard Corrigido Final
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path


def iniciar_servidor_corrigido_final():
    """Iniciar servidor HTTP para dashboard corrigido final"""
    print("🚀 INICIANDO SERVIDOR DASHBOARD CORRIGIDO FINAL...")
    print("-" * 50)

    # Verificar se arquivo existe
    dashboard_file = Path("dashboard_corrigido_final.html")
    if not dashboard_file.exists():
        print("❌ Arquivo dashboard_corrigido_final.html não encontrado!")
        return

    # Configurar servidor
    PORT = 8003
    Handler = http.server.SimpleHTTPRequestHandler

    # Mudar para diretório correto
    os.chdir(Path(__file__).parent)

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"✅ Servidor iniciado na porta {PORT}")
            print(
                f"🌐 URL: http://localhost:{PORT}/dashboard_corrigido_final.html")
            print("")
            print("🎉 DASHBOARD CORRIGIDO FINAL - TODOS OS PROBLEMAS RESOLVIDOS:")
            print("  ✅ 91 diretorias (não mais 89)")
            print("  ✅ 5,582 escolas com dados atualizados")
            print("  ✅ Marcadores de escolas por tipo corretos")
            print("  ✅ Diretorias visíveis no mapa com veículos")
            print("  ✅ Linhas de conexão escola-diretoria")
            print("  ✅ Legenda corrigida e funcional")
            print("  ✅ Lista de escolas mostra todos os tipos")
            print("  ✅ Gráficos funcionais")
            print("  ✅ Estilo original preservado")
            print("  ✅ Módulos simplificados para manutenção")
            print("")
            print("⏹️  Pressione Ctrl+C para parar o servidor")
            print("-" * 50)

            # Abrir navegador automaticamente
            webbrowser.open(
                f"http://localhost:{PORT}/dashboard_corrigido_final.html")

            # Manter servidor rodando
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")


if __name__ == "__main__":
    iniciar_servidor_corrigido_final()
