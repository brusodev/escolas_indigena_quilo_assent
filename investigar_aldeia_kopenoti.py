#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula a distância haversine entre dois pontos em km"""
    R = 6371  # Raio da Terra em km

    # Converter para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Diferenças
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def main():
    print("=== INVESTIGAÇÃO ALDEIA KOPENOTI ===\n")

    # 1. Carregar dados das escolas
    with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        escolas_data = json.load(f)

    # Encontrar ALDEIA KOPENOTI
    kopenoti = None
    for escola in escolas_data:
        if escola.get('name') == 'ALDEIA KOPENOTI':
            kopenoti = escola
            break

    if not kopenoti:
        print("❌ ALDEIA KOPENOTI não encontrada!")
        return

    print("1. DADOS ATUAIS DA ESCOLA:")
    print(f"   Nome: {kopenoti['name']}")
    print(f"   Cidade: {kopenoti['city']}")
    print(f"   Diretoria: {kopenoti['diretoria']}")
    print(f"   Coordenadas Escola: {kopenoti['lat']}, {kopenoti['lng']}")
    print(
        f"   Coordenadas Diretoria: {kopenoti['de_lat']}, {kopenoti['de_lng']}")
    print(f"   Distância Atual: {kopenoti['distance']} km")
    print(f"   Endereço Escola: {kopenoti['endereco_escola']}")
    print(f"   Endereço Diretoria: {kopenoti['endereco_diretoria']}")

    # 2. Recalcular distância
    print(f"\n2. RECALCULANDO DISTÂNCIA:")
    distancia_calculada = haversine_distance(
        kopenoti['lat'], kopenoti['lng'],
        kopenoti['de_lat'], kopenoti['de_lng']
    )
    print(f"   Distância recalculada: {distancia_calculada:.2f} km")

    if abs(distancia_calculada - kopenoti['distance']) > 1:
        print(
            f"   ⚠️  DISCREPÂNCIA: {abs(distancia_calculada - kopenoti['distance']):.2f} km de diferença!")
    else:
        print(f"   ✅ Distância consistente")

    # 3. Verificar outras escolas de Bauru para comparação
    print(f"\n3. OUTRAS ESCOLAS DE BAURU:")
    escolas_bauru = [e for e in escolas_data if e.get('diretoria') == 'Bauru']

    for escola in escolas_bauru:
        if escola['name'] != 'ALDEIA KOPENOTI':
            dist_calc = haversine_distance(
                escola['lat'], escola['lng'],
                escola['de_lat'], escola['de_lng']
            )
            print(
                f"   - {escola['name']}: {escola['distance']:.2f} km (calc: {dist_calc:.2f} km)")

    # 4. Investigar coordenadas
    print(f"\n4. ANÁLISE DE COORDENADAS:")
    print(f"   Escola KOPENOTI:")
    print(f"   - Latitude: {kopenoti['lat']} (Sul)")
    print(f"   - Longitude: {kopenoti['lng']} (Oeste)")
    print(f"   - Localização: Avaí/SP")

    print(f"\n   Diretoria Bauru:")
    print(f"   - Latitude: {kopenoti['de_lat']} (Sul)")
    print(f"   - Longitude: {kopenoti['de_lng']} (Oeste)")
    print(f"   - Localização: Bauru/SP")

    # 5. Verificar se a escola deveria estar em outra diretoria
    print(f"\n5. VERIFICANDO DIRETORIAS MAIS PRÓXIMAS:")

    # Carregar todas as diretorias
    diretorias_coords = {}
    for escola in escolas_data:
        diretoria = escola.get('diretoria')
        if diretoria and diretoria not in diretorias_coords:
            diretorias_coords[diretoria] = {
                'lat': escola['de_lat'],
                'lng': escola['de_lng']
            }

    # Calcular distâncias para todas as diretorias
    distancias_diretorias = []
    for nome_diretoria, coords in diretorias_coords.items():
        distancia = haversine_distance(
            kopenoti['lat'], kopenoti['lng'],
            coords['lat'], coords['lng']
        )
        distancias_diretorias.append((nome_diretoria, distancia))

    # Ordenar por distância
    distancias_diretorias.sort(key=lambda x: x[1])

    print(f"   Diretorias mais próximas de ALDEIA KOPENOTI:")
    for i, (nome, dist) in enumerate(distancias_diretorias[:5]):
        status = "⭐ ATUAL" if nome == kopenoti['diretoria'] else ""
        print(f"   {i+1}. {nome}: {dist:.2f} km {status}")

    # 6. Verificar endereço para validar localização
    print(f"\n6. VALIDAÇÃO DO ENDEREÇO:")
    endereco = kopenoti['endereco_escola']
    print(f"   Endereço: {endereco}")

    if "Avaí" in endereco and "SP" in endereco:
        print(f"   ✅ Endereço confirma localização em Avaí/SP")
    else:
        print(f"   ⚠️  Endereço pode estar incorreto")

    # 7. Sugestões de correção
    print(f"\n7. ANÁLISE E SUGESTÕES:")

    diretoria_mais_proxima = distancias_diretorias[0]
    if diretoria_mais_proxima[0] != kopenoti['diretoria']:
        print(
            f"   ⚠️  POSSÍVEL ERRO: Escola está atribuída à diretoria '{kopenoti['diretoria']}' ({kopenoti['distance']:.2f} km)")
        print(
            f"       mas a diretoria mais próxima é '{diretoria_mais_proxima[0]}' ({diretoria_mais_proxima[1]:.2f} km)")
        print(
            f"       Diferença: {kopenoti['distance'] - diretoria_mais_proxima[1]:.2f} km")
    else:
        print(f"   ✅ Escola está corretamente atribuída à diretoria mais próxima")

    if distancia_calculada > 200:
        print(
            f"   ⚠️  DISTÂNCIA MUITO ALTA: {distancia_calculada:.2f} km pode indicar erro de coordenadas")

    return kopenoti, distancias_diretorias


if __name__ == "__main__":
    main()
