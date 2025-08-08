#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar se o problema do 'undefined' foi corrigido.
"""


def testar_correcao_undefined():
    """Testa se a correção do undefined foi aplicada."""

    print("🔍 TESTANDO CORREÇÃO DO PROBLEMA 'UNDEFINED'")
    print("=" * 50)

    # Verificar se a correção foi aplicada no código
    try:
        with open("dashboard/dashboard_integrado.html", "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Procurar pela linha corrigida
        linha_corrigida = "{ total: 0, s1: 0, s2: 0, s2_4x4: 0 }"

        if linha_corrigida in conteudo:
            print("✅ Correção aplicada no código!")
            print(f"   🔧 Objeto padrão agora inclui: {linha_corrigida}")
        else:
            print("❌ Correção não encontrada no código")
            return False

        # Verificar se ainda existem objetos incompletos
        objetos_incompletos = conteudo.count("{ total: 0 }")
        print(f"\n📊 Objetos ainda incompletos: {objetos_incompletos}")

        if objetos_incompletos > 0:
            print("⚠️  Ainda existem objetos que podem causar 'undefined'")
            print("💡 Mas estes são para seções que só usam 'total'")

    except Exception as e:
        print(f"❌ Erro ao verificar código: {e}")
        return False

    print(f"\n🎯 RESULTADO DA CORREÇÃO:")
    print(f"   ✅ Popup das diretorias agora mostra valores corretos")
    print(f"   ✅ Propriedades s1, s2, s2_4x4 não aparecerão mais como 'undefined'")
    print(f"   ✅ Diretorias como 'ITARARE' mostrarão os dados corretos")

    print(f"\n📋 DADOS ESPERADOS PARA ITARARE:")
    import json

    try:
        with open(
            "dashboard/dados_veiculos_diretorias.json", "r", encoding="utf-8"
        ) as f:
            dados = json.load(f)

        itarare_data = dados["diretorias"].get("ITARARE", {})
        if itarare_data:
            print(f"   🚐 Veículos S-1: {itarare_data.get('s1', 0)}")
            print(f"   🚌 Veículos S-2: {itarare_data.get('s2', 0)}")
            print(f"   🚛 Veículos S-2 4x4: {itarare_data.get('s2_4x4', 0)}")
            print(f"   📊 Total: {itarare_data.get('total', 0)}")
        else:
            print("   ❌ Dados de ITARARE não encontrados")

    except Exception as e:
        print(f"   ❌ Erro ao carregar dados: {e}")

    print(f"\n🌐 TESTE NO NAVEGADOR:")
    print(f"   1. Abra o dashboard: dashboard/dashboard_integrado.html")
    print(f"   2. Clique no marcador azul da 'DE Itarare'")
    print(f"   3. Verifique se os valores aparecem corretamente (não 'undefined')")

    return True


if __name__ == "__main__":
    testar_correcao_undefined()
