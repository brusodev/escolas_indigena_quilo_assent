#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar se as coordenadas estão corretas nos JSONs gerados
"""

import json

def verificar_coordenadas_json():
    # Verificar escola indígena
    with open('dados/json/por_tipo/escolas_indigena.json', 'r', encoding='utf-8') as f:
        indigenas = json.load(f)
    
    print("=== VERIFICAÇÃO COORDENADAS NOS JSONs ===")
    print(f"Total escolas indígenas: {len(indigenas)}")
    
    # Encontrar escola com coordenadas
    escola_com_coords = None
    escola_sem_coords = None
    
    for escola in indigenas:
        lat = escola['localizacao']['latitude']
        lng = escola['localizacao']['longitude']
        
        if lat is not None and lng is not None:
            if escola_com_coords is None:
                escola_com_coords = escola
        else:
            if escola_sem_coords is None:
                escola_sem_coords = escola
    
    if escola_com_coords:
        print(f"\n✅ Escola COM coordenadas:")
        print(f"   Nome: {escola_com_coords['nome']}")
        print(f"   Lat: {escola_com_coords['localizacao']['latitude']}")
        print(f"   Lng: {escola_com_coords['localizacao']['longitude']}")
        print(f"   Município: {escola_com_coords['localizacao']['municipio']}")
    
    if escola_sem_coords:
        print(f"\n❌ Escola SEM coordenadas:")
        print(f"   Nome: {escola_sem_coords['nome']}")
        print(f"   Lat: {escola_sem_coords['localizacao']['latitude']}")
        print(f"   Lng: {escola_sem_coords['localizacao']['longitude']}")
        print(f"   Município: {escola_sem_coords['localizacao']['municipio']}")
    
    # Contar quantas têm coordenadas
    com_coordenadas = sum(1 for e in indigenas 
                         if e['localizacao']['latitude'] is not None 
                         and e['localizacao']['longitude'] is not None)
    
    print(f"\n📊 Resumo:")
    print(f"   Escolas indígenas com coordenadas: {com_coordenadas}")
    print(f"   Escolas indígenas sem coordenadas: {len(indigenas) - com_coordenadas}")
    
    # Verificar uma escola regular também
    with open('dados/json/por_tipo/escolas_regular.json', 'r', encoding='utf-8') as f:
        regulares = json.load(f)
    
    escola_regular = regulares[0]  # Primeira escola regular
    print(f"\n📍 Primeira escola regular:")
    print(f"   Nome: {escola_regular['nome']}")
    print(f"   Lat: {escola_regular['localizacao']['latitude']}")
    print(f"   Lng: {escola_regular['localizacao']['longitude']}")

if __name__ == "__main__":
    verificar_coordenadas_json()
