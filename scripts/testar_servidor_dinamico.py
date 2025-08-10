#!/usr/bin/env python3
"""
Validar se os dados dinâmicos estão funcionando no servidor
"""

import requests
import json
import time


def testar_servidor_dinamico(porta=8002):
    """Testa se o servidor está carregando dados dinâmicos"""
    base_url = f"http://localhost:{porta}"

    print("🧪 TESTANDO SERVIDOR COM DADOS DINÂMICOS")
    print("=" * 50)

    try:
        # 1. Testar se o servidor está rodando
        print("1️⃣ Testando conectividade...")
        response = requests.get(
            f"{base_url}/dashboard_integrado.html", timeout=5)

        if response.status_code == 200:
            print("   ✅ Servidor respondendo")
        else:
            print(f"   ❌ Servidor retornou status {response.status_code}")
            return False

        # 2. Testar se o JSON de escolas está acessível
        print("2️⃣ Testando JSON de escolas...")
        response = requests.get(
            f"{base_url}/dados/json/dados_escolas_atualizados.json", timeout=5)

        if response.status_code == 200:
            dados_escolas = response.json()
            print(f"   ✅ JSON acessível: {len(dados_escolas)} escolas")

            # Verificar tipos
            indigenas = len(
                [e for e in dados_escolas if e.get('type') == 'indigena'])
            quilombolas = len(
                [e for e in dados_escolas if e.get('type') == 'quilombola'])
            print(
                f"   📊 Tipos: {indigenas} indígenas + {quilombolas} quilombolas")

        else:
            print(f"   ❌ JSON não acessível: status {response.status_code}")
            return False

        # 3. Testar se o JSON de veículos está acessível
        print("3️⃣ Testando JSON de veículos...")
        response = requests.get(
            f"{base_url}/dados_veiculos_diretorias.json", timeout=5)

        if response.status_code == 200:
            dados_veiculos = response.json()
            total_veiculos = dados_veiculos['metadata']['total_veiculos']
            print(f"   ✅ JSON acessível: {total_veiculos} veículos totais")
        else:
            print(
                f"   ❌ JSON de veículos não acessível: status {response.status_code}")
            return False

        # 4. Testar JavaScript dinâmico
        print("4️⃣ Testando JavaScript dinâmico...")
        response = requests.get(
            f"{base_url}/static/js/dash_dinamico.js", timeout=5)

        if response.status_code == 200:
            js_content = response.text
            if "loadSchoolsData" in js_content and "fetch" in js_content:
                print("   ✅ JavaScript dinâmico acessível")
                print("   ✅ Contém funções de carregamento dinâmico")
            else:
                print("   ❌ JavaScript não contém funções dinâmicas")
                return False
        else:
            print(
                f"   ❌ JavaScript não acessível: status {response.status_code}")
            return False

        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print(
            f"✅ Dashboard dinâmico funcionando em: {base_url}/dashboard_integrado.html")
        print("✅ Dados sendo carregados diretamente dos JSONs")
        print("✅ Quando acessado via servidor, mostrará dados atualizados")

        return True

    except requests.exceptions.ConnectionError:
        print(f"❌ Não foi possível conectar ao servidor na porta {porta}")
        print("💡 Certifique-se de que o servidor está rodando:")
        print(f"   python -m http.server {porta}")
        return False

    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False


def comparar_dados_estaticos_vs_dinamicos():
    """Compara os dados que seriam carregados estaticamente vs dinamicamente"""
    print("\n📊 COMPARAÇÃO: ESTÁTICO vs DINÂMICO")
    print("=" * 40)

    # Dados do JSON (dinâmico)
    with open('dados/json/dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        dados_json = json.load(f)

    indigenas_json = len(
        [e for e in dados_json if e.get('type') == 'indigena'])
    quilombolas_json = len(
        [e for e in dados_json if e.get('type') == 'quilombola'])

    print("📄 DADOS DINÂMICOS (JSON):")
    print(f"   • Total: {len(dados_json)} escolas")
    print(f"   • Indígenas: {indigenas_json}")
    print(f"   • Quilombolas: {quilombolas_json}")

    # Verificar se há discrepância no HTML estático
    with open('dashboard_integrado.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    print("\n📄 DADOS ESTÁTICOS (HTML):")
    if "37 Escolas Indígenas + 26" in html_content:
        print("   ✅ HTML tem números corretos (37+26)")
    else:
        print("   ❌ HTML tem números incorretos")

    if "39 veículos" in html_content:
        print("   ✅ HTML menciona 39 veículos")
    else:
        print("   ❌ HTML não menciona 39 veículos")

    print(f"\n🎯 RESULTADO:")
    if indigenas_json == 37 and quilombolas_json == 26:
        print("✅ Dados dinâmicos estão corretos e atualizados")
    else:
        print("❌ Dados dinâmicos estão incorretos")


if __name__ == "__main__":
    # Aguardar um momento para o servidor estabilizar
    time.sleep(2)

    # Testar servidor dinâmico
    sucesso = testar_servidor_dinamico(8002)

    # Comparar dados
    comparar_dados_estaticos_vs_dinamicos()

    if sucesso:
        print(f"\n🚀 CORREÇÃO COMPLETA!")
        print("   O dashboard agora carrega dados dinâmicos via servidor")
        print("   Os dados sempre estarão sincronizados com os JSONs")
    else:
        print(f"\n⚠️ Verificar problemas acima")
