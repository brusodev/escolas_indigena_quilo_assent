#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificação dos dados para dashboard
"""

import json


def verificar_estrutura_dados():
    """Verificar estrutura dos dados para garantir compatibilidade"""
    print("🔍 VERIFICANDO ESTRUTURA DOS DADOS...")
    print("-" * 50)

    # Verificar escolas
    with open('dados/json/dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        escolas = json.load(f)

    print(f"📊 Escolas: {len(escolas):,}")

    # Verificar estrutura da primeira escola
    if escolas:
        primeira_escola = escolas[0]
        print("🏫 Estrutura da primeira escola:")
        for key, value in primeira_escola.items():
            print(f"  {key}: {type(value).__name__} = {str(value)[:50]}...")

    # Verificar tipos únicos
    tipos = set(escola.get('type', 'sem_tipo') for escola in escolas)
    print(f"\n📈 Tipos únicos: {sorted(tipos)}")

    # Verificar coordenadas válidas
    com_coords = sum(1 for e in escolas if e.get('lat') and e.get('lng'))
    print(f"📍 Escolas com coordenadas: {com_coords:,} / {len(escolas):,}")

    # Verificar veículos
    try:
        with open('dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
            veiculos = json.load(f)

        print(f"\n🚗 Veículos carregados")
        print(f"  Metadata: {veiculos.get('metadata', {})}")
        print(
            f"  Diretorias com veículos: {len(veiculos.get('diretorias', {}))}")

    except Exception as e:
        print(f"❌ Erro ao carregar veículos: {e}")

    # Verificar JavaScript modules
    js_files = [
        'static/js/modules/data-loader.js',
        'static/js/modules/charts.js',
        'static/js/dashboard-main.js'
    ]

    print(f"\n📜 Arquivos JavaScript:")
    for js_file in js_files:
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"  ✅ {js_file}: {len(content):,} caracteres")
        except Exception as e:
            print(f"  ❌ {js_file}: {e}")


if __name__ == "__main__":
    verificar_estrutura_dados()
