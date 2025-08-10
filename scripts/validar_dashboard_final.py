#!/usr/bin/env python3
"""
Validação final do dashboard após correções
"""

import re


def validar_dashboard():
    """Valida se todas as correções foram aplicadas no dashboard"""
    print("🔍 VALIDANDO DASHBOARD APÓS CORREÇÕES")
    print("=" * 50)

    with open('dashboard_integrado.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    validacoes = []

    # 1. Verificar cartão de veículos
    if 'id="total-vehicles">39<' in html_content:
        validacoes.append("✅ Cartão de veículos: 39")
    else:
        validacoes.append("❌ Cartão de veículos ainda incorreto")

    # 2. Verificar comentário de fontes
    if "39 veículos nas diretorias relevantes" in html_content:
        validacoes.append("✅ Comentário de fontes: 39 veículos")
    else:
        validacoes.append("❌ Comentário de fontes ainda incorreto")

    # 3. Verificar legenda escolas indígenas
    if "Escola Indígena (37 escolas)" in html_content:
        validacoes.append("✅ Legenda indígenas: 37 escolas")
    else:
        validacoes.append("❌ Legenda indígenas ainda incorreta")

    # 4. Verificar legenda escolas quilombolas
    if "Escola Quilombola/Assentamento (26 escolas)" in html_content:
        validacoes.append("✅ Legenda quilombolas: 26 escolas")
    else:
        validacoes.append("❌ Legenda quilombolas ainda incorreta")

    # 5. Verificar legenda diretorias
    if "19 DEs com 39 veículos no total" in html_content:
        validacoes.append("✅ Legenda diretorias: 39 veículos")
    else:
        validacoes.append("❌ Legenda diretorias ainda incorreta")

    # 6. Verificar totais no comentário inicial
    if "37 Escolas Indígenas + 26 Escolas Quilombolas" in html_content:
        validacoes.append("✅ Comentário inicial: 37+26 escolas")
    else:
        validacoes.append("❌ Comentário inicial ainda incorreto")

    print("\n📊 RESULTADO DA VALIDAÇÃO:")
    for validacao in validacoes:
        print(f"  {validacao}")

    sucessos = sum(1 for v in validacoes if "✅" in v)
    total = len(validacoes)

    print(f"\n🎯 RESUMO: {sucessos}/{total} validações passaram")

    if sucessos == total:
        print("🎉 DASHBOARD COMPLETAMENTE CORRIGIDO!")
        return True
    else:
        print("⚠️ Ainda há itens para corrigir")
        return False


def validar_javascript():
    """Valida se o JavaScript está correto"""
    print("\n🔍 VALIDANDO JAVASCRIPT")
    print("=" * 30)

    with open('static/js/dash.js', 'r', encoding='utf-8') as f:
        js_content = f.read()

    validacoes_js = []

    # Verificar se totalvehicles = 39
    if "let totalvehicles = 39;" in js_content:
        validacoes_js.append("✅ JavaScript: totalvehicles = 39")
    else:
        validacoes_js.append("❌ JavaScript: totalvehicles incorreto")

    # Verificar se usa totalVehiclesRelevantes
    if "totalVehiclesRelevantes;" in js_content:
        validacoes_js.append("✅ JavaScript: usa cálculo dinâmico")
    else:
        validacoes_js.append("❌ JavaScript: não usa cálculo dinâmico")

    for validacao in validacoes_js:
        print(f"  {validacao}")

    return all("✅" in v for v in validacoes_js)


if __name__ == "__main__":
    html_ok = validar_dashboard()
    js_ok = validar_javascript()

    print(f"\n🏁 VALIDAÇÃO FINAL:")
    print(f"  📄 HTML: {'✅ OK' if html_ok else '❌ Pendente'}")
    print(f"  🔧 JavaScript: {'✅ OK' if js_ok else '❌ Pendente'}")

    if html_ok and js_ok:
        print("\n🎉 DASHBOARD TOTALMENTE SINCRONIZADO!")
        print("   • Cartões mostram 39 veículos")
        print("   • Legenda mostra 37+26+39")
        print("   • JavaScript calcula dinamicamente")
    else:
        print("\n⚠️ Verificar itens pendentes acima")
