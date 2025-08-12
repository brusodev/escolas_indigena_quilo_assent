#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SERVIDOR LOCAL PARA DASHBOARD CITEM
==================================

Servidor HTTP simples para executar o dashboard sem problemas de CORS.
Resolve todos os problemas de file:// protocol.

Como usar:
1. Execute: python servidor_dashboard.py
2. Abra: http://localhost:8000/dashboard_citem_completo.html
3. Dashboard funcionará perfeitamente!

Autor: Sistema Dashboard Escolas
Data: 11/08/2025
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time

def iniciar_servidor():
    """Iniciar servidor HTTP local"""
    PORT = 8000
    
    # Verificar se a porta está disponível
    try:
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print("🌐 SERVIDOR DASHBOARD CITEM INICIADO")
            print("=" * 40)
            print(f"📡 Servidor rodando em: http://localhost:{PORT}")
            print(f"🎯 Dashboard disponível em: http://localhost:{PORT}/dashboard_citem_completo.html")
            print("✨ Todos os problemas de CORS resolvidos!")
            print()
            print("🔧 COMANDOS:")
            print("   - Ctrl+C para parar o servidor")
            print("   - O navegador abrirá automaticamente")
            print()
            
            # Aguardar um pouco e abrir navegador automaticamente
            def abrir_navegador():
                time.sleep(2)
                url = f"http://localhost:{PORT}/dashboard_citem_completo.html"
                print(f"🌍 Abrindo navegador: {url}")
                webbrowser.open(url)
            
            # Abrir em thread separada
            threading.Thread(target=abrir_navegador, daemon=True).start()
            
            print("🚀 Servidor ativo! Dashboard carregando...")
            print("-" * 40)
            
            # Iniciar servidor
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Porta {PORT} já está em uso!")
            print("💡 SOLUÇÕES:")
            print(f"   1. Pare o processo que usa a porta {PORT}")
            print(f"   2. Ou abra manualmente: http://localhost:{PORT}/dashboard_citem_completo.html")
        else:
            print(f"❌ Erro ao iniciar servidor: {e}")

def verificar_arquivos():
    """Verificar se os arquivos necessários existem"""
    arquivos_necessarios = [
        "dashboard_citem_completo.html",
        "dados/json/dados_escolas_atualizados_completo.json",
        "static/js/modules/data-loader-citem-completo.js"
    ]
    
    print("🔍 VERIFICANDO ARQUIVOS...")
    print("-" * 25)
    
    todos_ok = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - FALTANDO")
            todos_ok = False
    
    return todos_ok

def main():
    """Função principal"""
    print("🎯 SERVIDOR DASHBOARD CITEM")
    print("=" * 30)
    print("Objetivo: Resolver problemas de CORS e servir dashboard")
    print()
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("dashboard_citem_completo.html"):
        print("❌ ERRO: Execute este script no diretório do dashboard!")
        print("💡 Navegue até a pasta do projeto antes de executar")
        return
    
    # Verificar arquivos
    if not verificar_arquivos():
        print("\n⚠️ ARQUIVOS FALTANDO!")
        print("Execute primeiro: python migrar_dashboard_completo.py")
        return
    
    print("\n✅ Todos os arquivos encontrados!")
    print("🚀 Iniciando servidor HTTP...")
    
    try:
        iniciar_servidor()
    except KeyboardInterrupt:
        print("\n\n👋 Servidor interrompido pelo usuário")
        print("✅ Dashboard encerrado com sucesso!")

if __name__ == "__main__":
    main()
