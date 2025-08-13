#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testar carregamento de dados para dashboard
"""

import json
import requests
import time


def testar_dados_dashboard():
    """Testar se os dados estão acessíveis via HTTP"""
    print("🧪 TESTANDO CARREGAMENTO DE DADOS...")
    print("-" * 40)

    base_url = "http://localhost:8001"

    # Testar arquivo de escolas
    try:
        print("📊 Testando dados_escolas_atualizados.json...")
        response = requests.get(
            f"{base_url}/dados/json/dados_escolas_atualizados.json")
        if response.status_code == 200:
            escolas = response.json()
            print(f"✅ Escolas: {len(escolas):,} registros carregados")

            # Análise rápida
            diretorias = set(e['diretoria'] for e in escolas)
            tipos = {}
            for escola in escolas:
                tipo = escola.get('type', 'sem_tipo')
                tipos[tipo] = tipos.get(tipo, 0) + 1

            print(f"🏛️ Diretorias: {len(diretorias)}")
            print(f"📈 Tipos: {len(tipos)}")

        else:
            print(f"❌ Erro HTTP {response.status_code} ao carregar escolas")

    except Exception as e:
        print(f"❌ Erro ao carregar escolas: {e}")

    # Testar arquivo de veículos
    try:
        print("\n🚗 Testando dados_veiculos_diretorias.json...")
        response = requests.get(f"{base_url}/dados_veiculos_diretorias.json")
        if response.status_code == 200:
            veiculos = response.json()
            total_veiculos = veiculos.get(
                'metadata', {}).get('total_veiculos', 0)
            diretorias_veiculos = len(veiculos.get('diretorias', {}))
            print(
                f"✅ Veículos: {total_veiculos} total em {diretorias_veiculos} diretorias")
        else:
            print(f"❌ Erro HTTP {response.status_code} ao carregar veículos")

    except Exception as e:
        print(f"❌ Erro ao carregar veículos: {e}")

    # Testar dashboard
    try:
        print("\n🌐 Testando dashboard_corrigido.html...")
        response = requests.get(f"{base_url}/dashboard_corrigido.html")
        if response.status_code == 200:
            print(f"✅ Dashboard: {len(response.text):,} bytes carregados")
        else:
            print(f"❌ Erro HTTP {response.status_code} ao carregar dashboard")

    except Exception as e:
        print(f"❌ Erro ao carregar dashboard: {e}")


if __name__ == "__main__":
    # Aguardar um pouco para servidor estar pronto
    time.sleep(2)
    testar_dados_dashboard()
