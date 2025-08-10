#!/usr/bin/env python3
"""
Script para executar o dashboard como servidor web
Múltiplas opções de servidor disponíveis
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path


def servidor_python_simples(porta=8000):
    """Servidor HTTP simples do Python"""
    print(f"🚀 INICIANDO SERVIDOR PYTHON")
    print(f"📍 URL: http://localhost:{porta}")
    print(f"📁 Diretório: {os.getcwd()}")
    print(f"🌐 Dashboard: http://localhost:{porta}/dashboard_integrado.html")
    print("🛑 Para parar: Ctrl+C")
    print("-" * 50)

    try:
        with socketserver.TCPServer(("", porta), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"✅ Servidor rodando na porta {porta}")
            print(
                f"🔗 Acesse: http://localhost:{porta}/dashboard_integrado.html")

            # Abrir automaticamente no navegador
            webbrowser.open(
                f"http://localhost:{porta}/dashboard_integrado.html")

            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except OSError as e:
        if e.errno == 10048:  # Porta já em uso
            print(f"❌ Erro: Porta {porta} já está em uso")
            print(
                f"💡 Tente outra porta: python scripts/servidor.py {porta + 1}")
        else:
            print(f"❌ Erro ao iniciar servidor: {e}")


def servidor_com_cors(porta=8000):
    """Servidor HTTP com suporte a CORS"""

    class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods',
                             'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            super().end_headers()

    print(f"🚀 INICIANDO SERVIDOR COM CORS")
    print(f"📍 URL: http://localhost:{porta}")
    print(f"🌐 Dashboard: http://localhost:{porta}/dashboard_integrado.html")
    print("🛑 Para parar: Ctrl+C")
    print("-" * 50)

    try:
        with socketserver.TCPServer(("", porta), CORSRequestHandler) as httpd:
            print(f"✅ Servidor CORS rodando na porta {porta}")
            webbrowser.open(
                f"http://localhost:{porta}/dashboard_integrado.html")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")


def mostrar_opcoes():
    """Mostra todas as opções disponíveis"""
    print("🌐 OPÇÕES DE SERVIDOR PARA O DASHBOARD")
    print("=" * 50)
    print()
    print("1️⃣  PYTHON HTTP SIMPLES:")
    print("   python -m http.server 8000")
    print("   📍 http://localhost:8000/dashboard_integrado.html")
    print()
    print("2️⃣  PYTHON HTTP COM SCRIPT:")
    print("   python scripts/servidor.py")
    print("   📍 http://localhost:8000/dashboard_integrado.html")
    print()
    print("3️⃣  NODE.JS HTTP-SERVER (se instalado):")
    print("   npx http-server -p 8000 -c-1")
    print("   📍 http://localhost:8000/dashboard_integrado.html")
    print()
    print("4️⃣  PHP SERVIDOR (se instalado):")
    print("   php -S localhost:8000")
    print("   📍 http://localhost:8000/dashboard_integrado.html")
    print()
    print("5️⃣  LIVE SERVER (VS Code):")
    print("   Instalar extensão 'Live Server'")
    print("   Clicar com botão direito > 'Open with Live Server'")
    print()
    print("6️⃣  PYTHON COM CORS:")
    print("   python scripts/servidor.py --cors")
    print("   📍 http://localhost:8000/dashboard_integrado.html")
    print()
    print("🎯 RECOMENDADO: Opção 1 (mais simples) ou 5 (VS Code)")


def main():
    """Função principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            mostrar_opcoes()
            return
        elif sys.argv[1] == "--cors":
            porta = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
            servidor_com_cors(porta)
            return
        else:
            try:
                porta = int(sys.argv[1])
                servidor_python_simples(porta)
                return
            except ValueError:
                print("❌ Porta deve ser um número")
                return

    # Servidor padrão
    servidor_python_simples(8000)


if __name__ == "__main__":
    main()
