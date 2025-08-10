#!/usr/bin/env python3
"""
Script para testar se o carregamento dinâmico está funcionando via curl/requests.
"""

import requests
import time
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import os


def test_dynamic_loading():
    print("🧪 TESTE DE CARREGAMENTO DINÂMICO")
    print("=" * 50)

    # Iniciar servidor em thread separada
    os.chdir(os.path.dirname(os.path.dirname(__file__)))

    class CORSHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods',
                             'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            super().end_headers()

        def log_message(self, format, *args):
            print(f"📥 {format % args}")

    def start_server():
        httpd = HTTPServer(('localhost', 8001), CORSHandler)
        print("🚀 Servidor de teste iniciado na porta 8001")
        httpd.serve_forever()

    # Iniciar servidor em thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(2)

    base_url = "http://localhost:8001"

    try:
        # Testar se os arquivos estão sendo servidos
        print("\n🔍 Testando arquivos...")

        # Testar HTML
        response = requests.get(f"{base_url}/dashboard_integrado.html")
        if response.status_code == 200:
            print("✅ dashboard_integrado.html: OK")
            if "dash_dinamico.js" in response.text:
                print("✅ HTML carrega dash_dinamico.js")
            else:
                print("❌ HTML não carrega dash_dinamico.js")
        else:
            print(f"❌ dashboard_integrado.html: {response.status_code}")

        # Testar JavaScript dinâmico
        response = requests.get(f"{base_url}/static/js/dash_dinamico.js")
        if response.status_code == 200:
            print("✅ dash_dinamico.js: OK")
            if "loadSchoolsData" in response.text:
                print("✅ Contém função de carregamento dinâmico")
            else:
                print("❌ Não contém funções dinâmicas")
        else:
            print(f"❌ dash_dinamico.js: {response.status_code}")

        # Testar JSONs
        response = requests.get(
            f"{base_url}/dados/json/dados_escolas_atualizados.json")
        if response.status_code == 200:
            print("✅ dados_escolas_atualizados.json: OK")
        else:
            print(f"❌ dados_escolas_atualizados.json: {response.status_code}")

        response = requests.get(f"{base_url}/dados_veiculos_diretorias.json")
        if response.status_code == 200:
            print("✅ dados_veiculos_diretorias.json: OK")
        else:
            print(f"❌ dados_veiculos_diretorias.json: {response.status_code}")

        print(f"\n🌐 Abrindo dashboard em: {base_url}/dashboard_integrado.html")
        webbrowser.open(f"{base_url}/dashboard_integrado.html")

        print("\n✅ TESTE CONCLUÍDO!")
        print("🔗 Verifique o navegador para validar os dados dinâmicos")

    except Exception as e:
        print(f"❌ Erro no teste: {e}")


if __name__ == "__main__":
    test_dynamic_loading()
