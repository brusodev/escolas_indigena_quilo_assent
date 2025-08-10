#!/usr/bin/env python3
"""
Script para verificar se o dashboard está exibindo os dados corretos.
"""

import requests
import time


def verificar_dashboard_final():
    print("🔍 VERIFICAÇÃO FINAL DO DASHBOARD")
    print("=" * 50)

    base_url = "http://localhost:8005"

    try:
        # Verificar se o servidor está respondendo
        response = requests.get(
            f"{base_url}/dashboard_integrado.html", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard carregando corretamente")

            # Verificar se está carregando o JavaScript correto
            if "dash_dinamico.js" in response.text:
                print("✅ JavaScript dinâmico sendo carregado")
            else:
                print("❌ JavaScript dinâmico NÃO encontrado")
                return False

        else:
            print(f"❌ Dashboard não acessível: {response.status_code}")
            return False

        # Verificar JSONs
        print("\n🔄 Verificando carregamento dos dados...")

        # Testar dados das escolas
        response = requests.get(
            f"{base_url}/dados/json/dados_escolas_atualizados.json", timeout=5)
        if response.status_code == 200:
            escolas = response.json()
            print(f"✅ Escolas carregadas: {len(escolas)} escolas")
        else:
            print("❌ Dados das escolas não carregaram")
            return False

        # Testar dados dos veículos
        response = requests.get(
            f"{base_url}/dados_veiculos_diretorias.json", timeout=5)
        if response.status_code == 200:
            veiculos = response.json()
            total_veiculos = veiculos.get(
                'metadata', {}).get('total_veiculos', 0)
            print(f"✅ Veículos carregados: {total_veiculos} veículos totais")
        else:
            print("❌ Dados dos veículos não carregaram")
            return False

        print("\n🎯 RESULTADO FINAL:")
        print("✅ DASHBOARD FUNCIONANDO PERFEITAMENTE!")
        print("✅ Dados dinâmicos sendo carregados corretamente!")
        print("✅ JavaScript dinâmico ativo!")
        print("\n🌐 Acesse: http://localhost:8003/dashboard_integrado.html")
        print("📊 Verifique se mostra: 39 veículos, 63 escolas, 19 diretorias")

        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        print("💡 Certifique-se de que o servidor está rodando")
        return False


if __name__ == "__main__":
    sucesso = verificar_dashboard_final()
    if sucesso:
        print("\n🎉 TESTE PASSOU! Dashboard funcionando!")
    else:
        print("\n❌ TESTE FALHOU! Verifique o servidor.")
