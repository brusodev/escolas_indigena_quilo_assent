#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mostrar exemplos de escolas com coordenadas para verificação final
"""

import json

def mostrar_exemplos_coordenadas():
    print("🗺️  VERIFICAÇÃO FINAL DAS COORDENADAS")
    print("=" * 50)
    
    # Escolas Indígenas
    with open('dados/json/por_tipo/escolas_indigena.json', 'r', encoding='utf-8') as f:
        indigenas = json.load(f)
    
    print(f"\n🏞️  ESCOLAS INDÍGENAS ({len(indigenas)} total):")
    print("-" * 30)
    for escola in indigenas[:5]:  # Primeiras 5
        lat = escola['localizacao']['latitude']
        lng = escola['localizacao']['longitude']
        print(f"📍 {escola['nome']}")
        print(f"   📍 Coordenadas: ({lat}, {lng})")
        print(f"   🏛️  Diretoria: {escola['administrativa']['diretoria_ensino']}")
        print(f"   🌍 Município: {escola['localizacao']['municipio']}")
        print()
    
    # Escolas Quilombolas  
    with open('dados/json/por_tipo/escolas_quilombola.json', 'r', encoding='utf-8') as f:
        quilombolas = json.load(f)
    
    print(f"\n🏛️  ESCOLAS QUILOMBOLAS ({len(quilombolas)} total):")
    print("-" * 30)
    for escola in quilombolas[:3]:  # Primeiras 3
        lat = escola['localizacao']['latitude']
        lng = escola['localizacao']['longitude']
        print(f"📍 {escola['nome']}")
        print(f"   📍 Coordenadas: ({lat}, {lng})")
        print(f"   🏛️  Diretoria: {escola['administrativa']['diretoria_ensino']}")
        print(f"   🌍 Município: {escola['localizacao']['municipio']}")
        print()
    
    # Escolas de Assentamento
    with open('dados/json/por_tipo/escolas_assentamento.json', 'r', encoding='utf-8') as f:
        assentamento = json.load(f)
    
    print(f"\n🚜 ESCOLAS DE ASSENTAMENTO ({len(assentamento)} total):")
    print("-" * 30)
    for escola in assentamento:  # Todas (são poucas)
        lat = escola['localizacao']['latitude']
        lng = escola['localizacao']['longitude']
        print(f"📍 {escola['nome']}")
        print(f"   📍 Coordenadas: ({lat}, {lng})")
        print(f"   🏛️  Diretoria: {escola['administrativa']['diretoria_ensino']}")
        print(f"   🌍 Município: {escola['localizacao']['municipio']}")
        print()

if __name__ == "__main__":
    mostrar_exemplos_coordenadas()
