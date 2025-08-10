#!/usr/bin/env python3
"""
Verificar se dados hardcoded no JS estão atualizados
"""

import json

# Carregar dados JSON
with open('dados/json/dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

print("🔍 DIAGNÓSTICO: DADOS DESATUALIZADOS NO SERVIDOR")
print("=" * 55)

print(f"\n📊 DADOS NO JSON (corretos):")
print(f"   • Total: {len(json_data)} escolas")

indigenas_json = len([e for e in json_data if e['type'] == 'indigena'])
quilombolas_json = len([e for e in json_data if e['type'] == 'quilombola'])

print(f"   • Indígenas: {indigenas_json}")
print(f"   • Quilombolas: {quilombolas_json}")

print(f"\n❌ PROBLEMA IDENTIFICADO:")
print(f"   O JavaScript tem dados HARDCODED em vez de carregar do JSON!")

# Verificar se o JS carrega do JSON
with open('static/js/dash.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

if 'const schoolsData = [' in js_content:
    print(f"   ❌ JavaScript usa dados estáticos (hardcoded)")
    print(f"   ❌ Não carrega dados/json/dados_escolas_atualizados.json")
else:
    print(f"   ✅ JavaScript carrega dados dinamicamente")

print(f"\n🔧 SOLUÇÃO NECESSÁRIA:")
print(f"   1. Modificar JavaScript para carregar JSON")
print(f"   2. Remover dados hardcoded")
print(f"   3. Usar fetch() para dados_escolas_atualizados.json")

print(f"\n📁 ARQUIVO A CORRIGIR:")
print(f"   static/js/dash.js - linha ~135 (const schoolsData)")

print(f"\n🎯 RESULTADO ESPERADO:")
print(f"   Dashboard mostrará dados corretos quando acessado via servidor")
