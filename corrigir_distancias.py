#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir cálculos de distância entre escolas e diretorias
Utiliza a fórmula de Haversine para cálculo preciso de distâncias geográficas
"""

import pandas as pd
import math
import json

def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula distância entre dois pontos geográficos usando fórmula de Haversine
    
    Args:
        lat1, lon1: Latitude e longitude do primeiro ponto
        lat2, lon2: Latitude e longitude do segundo ponto
    
    Returns:
        float: Distância em quilômetros
    """
    # Raio da Terra em quilômetros
    R = 6371.0
    
    # Converter graus para radianos
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    # Fórmula de Haversine
    a = (math.sin(delta_lat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distancia = R * c
    return distancia

def corrigir_distancias():
    """
    Corrige as distâncias no arquivo Excel e regenera os arquivos JSON
    """
    print("🔧 Iniciando correção de distâncias...")
    print("=" * 50)
    
    # Ler arquivo Excel
    try:
        df = pd.read_excel('distancias_escolas_diretorias.xlsx')
        print(f"✅ Arquivo Excel carregado: {len(df)} escolas encontradas")
    except Exception as e:
        print(f"❌ Erro ao ler arquivo Excel: {e}")
        return
    
    # Contador de correções
    correcoes = 0
    problemas_grandes = []
    
    # Corrigir distâncias linha por linha
    for idx, row in df.iterrows():
        # Obter coordenadas
        lat_escola = row['Latitude_Escola']
        lon_escola = row['Longitude_Escola']
        lat_de = row['Latitude_Diretoria']
        lon_de = row['Longitude_Diretoria']
        
        # Verificar se as coordenadas são válidas
        if pd.isna(lat_escola) or pd.isna(lon_escola) or pd.isna(lat_de) or pd.isna(lon_de):
            print(f"⚠️  Coordenadas inválidas para: {row['Nome_Escola']}")
            continue
        
        # Calcular distância correta
        distancia_correta = calcular_distancia_haversine(lat_escola, lon_escola, lat_de, lon_de)
        distancia_atual = row['Distancia_KM']
        
        # Verificar se há diferença significativa (>5km)
        diferenca = abs(distancia_atual - distancia_correta)
        
        if diferenca > 5:
            print(f"🔧 Corrigindo {row['Nome_Escola']}:")
            print(f"   Distância atual: {distancia_atual:.2f} km")
            print(f"   Distância correta: {distancia_correta:.2f} km")
            print(f"   Diferença: {diferenca:.2f} km")
            print()
            
            # Atualizar a distância
            df.at[idx, 'Distancia_KM'] = round(distancia_correta, 2)
            correcoes += 1
            
            if diferenca > 50:
                problemas_grandes.append({
                    'escola': row['Nome_Escola'],
                    'distancia_antiga': distancia_atual,
                    'distancia_correta': distancia_correta,
                    'diferenca': diferenca
                })
    
    print(f"✅ Processo concluído: {correcoes} distâncias corrigidas")
    
    if problemas_grandes:
        print(f"\n🚨 Problemas grandes encontrados ({len(problemas_grandes)} escolas):")
        for problema in problemas_grandes:
            print(f"   • {problema['escola']}: {problema['distancia_antiga']:.1f}km → {problema['distancia_correta']:.1f}km")
    
    # Salvar arquivo corrigido
    try:
        df.to_excel('distancias_escolas_diretorias_corrigido.xlsx', index=False)
        print(f"\n💾 Arquivo corrigido salvo: distancias_escolas_diretorias_corrigido.xlsx")
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")
        return
    
    # Regenerar arquivo JSON
    try:
        dados_json = []
        for _, row in df.iterrows():
            escola = {
                "name": row['Nome_Escola'],
                "type": "indigena" if row['Tipo_Escola'] == "Indígena" else "quilombola",
                "city": row['Cidade_Escola'],
                "diretoria": row['Nome_Diretoria'],
                "distance": row['Distancia_KM'],
                "lat": row['Latitude_Escola'],
                "lng": row['Longitude_Escola'],
                "de_lat": row['Latitude_Diretoria'],
                "de_lng": row['Longitude_Diretoria'],
                "endereco_escola": row['Endereco_Escola'],
                "endereco_diretoria": row['Endereco_Diretoria']
            }
            dados_json.append(escola)
        
        with open('dados_escolas_corrigidos.json', 'w', encoding='utf-8') as f:
            json.dump(dados_json, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Arquivo JSON corrigido salvo: dados_escolas_corrigidos.json")
        
    except Exception as e:
        print(f"❌ Erro ao gerar JSON: {e}")
    
    return df

def verificar_kopenoti():
    """
    Verifica especificamente a escola KOPENOTI
    """
    print("\n🔍 Verificação específica - ALDEIA KOPENOTI:")
    print("=" * 45)
    
    try:
        df = pd.read_excel('distancias_escolas_diretorias_corrigido.xlsx')
        kopenoti = df[df['Nome_Escola'].str.contains('KOPENOTI', na=False)].iloc[0]
        
        print(f"✅ Nome: {kopenoti['Nome_Escola']}")
        print(f"📍 Coordenadas: {kopenoti['Latitude_Escola']}, {kopenoti['Longitude_Escola']}")
        print(f"🏢 Diretoria: {kopenoti['Nome_Diretoria']}")
        print(f"📍 DE Coordenadas: {kopenoti['Latitude_Diretoria']}, {kopenoti['Longitude_Diretoria']}")
        print(f"📏 Distância corrigida: {kopenoti['Distancia_KM']} km")
        print(f"🗺️  Google Maps referência: ~43.8 km")
        print(f"✨ Diferença com Google Maps: {abs(kopenoti['Distancia_KM'] - 43.8):.1f} km")
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")

if __name__ == "__main__":
    # Executar correção
    df_corrigido = corrigir_distancias()
    
    if df_corrigido is not None:
        # Verificar resultado para KOPENOTI
        verificar_kopenoti()
        
        print("\n" + "=" * 50)
        print("🎯 RESUMO DA CORREÇÃO:")
        print("• Arquivo original: distancias_escolas_diretorias.xlsx")
        print("• Arquivo corrigido: distancias_escolas_diretorias_corrigido.xlsx")
        print("• JSON atualizado: dados_escolas_corrigidos.json")
        print("• Método: Fórmula de Haversine (padrão geográfico)")
        print("=" * 50)
