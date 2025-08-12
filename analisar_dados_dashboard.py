#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise dos dados atualizados para correção do dashboard
"""

import json

def analisar_dados_atualizados():
    """Analisar dados atualizados para corrigir dashboard"""
    print("🔍 ANALISANDO DADOS ATUALIZADOS...")
    print("-" * 40)
    
    # Carregar dados originais (mais atualizados)
    with open('dados/json/dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        data_original = json.load(f)
    
    print(f"📊 Total de escolas nos dados originais: {len(data_original)}")
    
    # Analisar diretorias
    diretorias = set(escola['diretoria'] for escola in data_original)
    print(f"🏛️ Total de diretorias: {len(diretorias)}")
    
    print("\n📋 Diretorias encontradas:")
    for i, d in enumerate(sorted(diretorias), 1):
        print(f"  {i:2d}. {d}")
    
    # Analisar tipos
    tipos = {}
    for escola in data_original:
        tipo = escola.get('type', 'sem_tipo')
        tipos[tipo] = tipos.get(tipo, 0) + 1
    
    print(f"\n📈 Distribuição por tipo:")
    for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
        print(f"  {tipo}: {count:,} escolas")
    
    # Verificar coordenadas
    com_coords = sum(1 for e in data_original if e.get('lat') and e.get('lng'))
    print(f"\n📍 Coordenadas:")
    print(f"  ✅ Válidas: {com_coords:,}")
    print(f"  ❌ Inválidas: {len(data_original) - com_coords:,}")
    
    return data_original, diretorias, tipos

if __name__ == "__main__":
    analisar_dados_atualizados()
