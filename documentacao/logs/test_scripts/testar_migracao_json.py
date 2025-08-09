"""
Script para testar se o dashboard está usando corretamente o JSON
Criado em: 07/08/2025
Versão: 1.0
"""

import json
import os
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time


def verificar_arquivos():
    """Verifica se os arquivos necessários existem"""
    arquivos_necessarios = [
        'dados_veiculos_diretorias.json',
        'dashboard_integrado.html'
    ]

    print("🔍 Verificando arquivos necessários...")
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"  ✅ {arquivo}")
        else:
            print(f"  ❌ {arquivo} não encontrado!")
            return False
    return True


def validar_json():
    """Valida se o JSON está bem formado"""
    try:
        with open('dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)

        print("\n📊 Validação do JSON:")
        print(f"  ✅ JSON válido")
        print(f"  📁 Diretorias: {len(dados['diretorias'])}")
        print(f"  🚗 Total veículos: {dados['metadata']['total_veiculos']}")
        print(f"  📅 Data atualização: {dados['metadata']['data_atualizacao']}")
        return True
    except Exception as e:
        print(f"  ❌ Erro no JSON: {e}")
        return False


def testar_dashboard():
    """Testa o dashboard em um servidor local"""
    print("\n🚀 Iniciando servidor local para teste...")

    # Servidor HTTP simples
    class CORSRequestHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods',
                             'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            super().end_headers()

    def iniciar_servidor():
        with HTTPServer(('localhost', 8000), CORSRequestHandler) as server:
            print("  📡 Servidor rodando em http://localhost:8000")
            server.serve_forever()

    # Iniciar servidor em thread separada
    servidor_thread = threading.Thread(target=iniciar_servidor, daemon=True)
    servidor_thread.start()

    time.sleep(2)  # Aguardar servidor iniciar

    # Abrir dashboard no navegador
    url = "http://localhost:8000/dashboard_integrado.html"
    print(f"  🌐 Abrindo dashboard: {url}")
    print("\n✅ Dashboard aberto! Verifique:")
    print("  1. Se os dados de veículos carregaram (console do navegador)")
    print("  2. Se os gráficos estão funcionando")
    print("  3. Se as estatísticas estão corretas (172 veículos)")
    print("  4. Se o mapa está interativo")
    print("\n⚠️  Pressione Ctrl+C para parar o servidor")

    webbrowser.open(url)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")


def main():
    """Função principal de teste"""
    print("=== TESTE DE MIGRAÇÃO PARA JSON ===\n")

    if not verificar_arquivos():
        print("\n❌ Teste falhou: Arquivos necessários não encontrados")
        return

    if not validar_json():
        print("\n❌ Teste falhou: JSON inválido")
        return

    print("\n✅ Todos os arquivos validados com sucesso!")

    resposta = input("\n🤔 Deseja testar o dashboard no navegador? (s/n): ")
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        testar_dashboard()
    else:
        print("\n✅ Teste concluído. Dashboard pronto para uso!")


if __name__ == "__main__":
    main()
