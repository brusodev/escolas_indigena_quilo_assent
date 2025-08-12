#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar coordenadas das diretorias e calcular distâncias
"""
import json
import math
from datetime import datetime


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine
    """
    # Converter graus para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Diferenças
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    # Raio da Terra em quilômetros
    r = 6371

    return c * r


def extrair_coordenadas_diretorias():
    """Extrai coordenadas únicas das diretorias a partir dos dados das escolas"""
    print("🗺️ EXTRAINDO COORDENADAS DAS DIRETORIAS")
    print("=" * 60)

    # Carregar dados das escolas
    with open("dados_escolas_atualizados.json", "r", encoding="utf-8") as f:
        escolas = json.load(f)

    # Extrair coordenadas únicas das diretorias
    diretorias_coords = {}

    for escola in escolas:
        diretoria = escola.get("diretoria")
        de_lat = escola.get("de_lat")
        de_lng = escola.get("de_lng")
        endereco_diretoria = escola.get("endereco_diretoria")

        if diretoria and de_lat and de_lng:
            if diretoria not in diretorias_coords:
                diretorias_coords[diretoria] = {
                    "nome": diretoria,
                    "latitude": de_lat,
                    "longitude": de_lng,
                    "endereco": endereco_diretoria,
                    "total_escolas": 0,
                }
            # Contar escolas por diretoria
            diretorias_coords[diretoria]["total_escolas"] += 1

    print(f"✅ Extraídas coordenadas de {len(diretorias_coords)} diretorias")
    return diretorias_coords


def atualizar_tabela_diretorias(diretorias_coords):
    """Atualiza a tabela de diretorias com as coordenadas"""
    print("\n🏛️ ATUALIZANDO TABELA DE DIRETORIAS")
    print("=" * 60)

    # Carregar tabela atual de diretorias
    with open("flask_sistema/data/json/diretorias.json", "r", encoding="utf-8") as f:
        diretorias = json.load(f)

    # Atualizar coordenadas
    atualizadas = 0
    for diretoria in diretorias:
        nome = diretoria.get("nome")
        if nome in diretorias_coords:
            coords = diretorias_coords[nome]
            diretoria["latitude"] = coords["latitude"]
            diretoria["longitude"] = coords["longitude"]
            diretoria["endereco"] = coords.get("endereco", "")
            diretoria["updated_at"] = datetime.now().strftime("%Y-%m-%d")
            atualizadas += 1
            print(f"✅ {nome}: ({coords['latitude']:.6f}, {coords['longitude']:.6f})")

    # Salvar tabela atualizada
    with open("flask_sistema/data/json/diretorias.json", "w", encoding="utf-8") as f:
        json.dump(diretorias, f, ensure_ascii=False, indent=2)

    print(f"\n📊 Resumo:")
    print(f"   Total de diretorias: {len(diretorias)}")
    print(f"   Coordenadas atualizadas: {atualizadas}")
    print(f"   Arquivo salvo: flask_sistema/data/json/diretorias.json")

    return diretorias


def atualizar_distancias_escolas():
    """Atualiza/adiciona coluna de distância nas escolas"""
    print("\n📏 CALCULANDO DISTÂNCIAS ESCOLAS → DIRETORIAS")
    print("=" * 60)

    # Carregar dados das escolas
    with open("dados_escolas_atualizados.json", "r", encoding="utf-8") as f:
        escolas = json.load(f)

    # Calcular distâncias
    distancias_calculadas = 0
    for escola in escolas:
        lat_escola = escola.get("lat")
        lng_escola = escola.get("lng")
        lat_diretoria = escola.get("de_lat")
        lng_diretoria = escola.get("de_lng")

        if all([lat_escola, lng_escola, lat_diretoria, lng_diretoria]):
            # Calcular distância
            distancia = calcular_distancia_haversine(
                lat_escola, lng_escola, lat_diretoria, lng_diretoria
            )

            # Atualizar/adicionar campo de distância
            escola["distancia_diretoria_km"] = round(distancia, 2)
            distancias_calculadas += 1

            # Verificar se a distância calculada difere muito da existente
            distancia_existente = escola.get("distance")
            if distancia_existente and abs(distancia - distancia_existente) > 1:
                print(
                    f"⚠️ {escola['name']}: Diferença na distância - Nova: {distancia:.2f}km, Antiga: {distancia_existente}km"
                )

    # Salvar dados atualizados
    with open("dados_escolas_atualizados.json", "w", encoding="utf-8") as f:
        json.dump(escolas, f, ensure_ascii=False, indent=2)

    print(f"\n📊 Resumo:")
    print(f"   Total de escolas: {len(escolas)}")
    print(f"   Distâncias calculadas: {distancias_calculadas}")
    print(f"   Arquivo salvo: dados_escolas_atualizados.json")

    return escolas


def gerar_relatorio_distancias(escolas):
    """Gera relatório estatístico das distâncias"""
    print("\n📈 RELATÓRIO ESTATÍSTICO DE DISTÂNCIAS")
    print("=" * 60)

    # Filtrar escolas com distâncias calculadas
    escolas_com_distancia = [e for e in escolas if "distancia_diretoria_km" in e]

    if not escolas_com_distancia:
        print("❌ Nenhuma escola com distância calculada encontrada")
        return

    distancias = [e["distancia_diretoria_km"] for e in escolas_com_distancia]

    # Estatísticas gerais
    print(f"📊 Estatísticas Gerais:")
    print(f"   Total de escolas: {len(escolas_com_distancia)}")
    print(f"   Distância mínima: {min(distancias):.2f} km")
    print(f"   Distância máxima: {max(distancias):.2f} km")
    print(f"   Distância média: {sum(distancias)/len(distancias):.2f} km")

    # Estatísticas por tipo
    print(f"\n📋 Por Tipo de Escola:")
    tipos = {}
    for escola in escolas_com_distancia:
        tipo = escola.get("type", "indefinido")
        if tipo not in tipos:
            tipos[tipo] = []
        tipos[tipo].append(escola["distancia_diretoria_km"])

    for tipo, dists in tipos.items():
        print(
            f"   {tipo.capitalize()}: {len(dists)} escolas, distância média: {sum(dists)/len(dists):.2f} km"
        )

    # Top 10 maiores distâncias
    print(f"\n🎯 Top 10 Maiores Distâncias:")
    escolas_ordenadas = sorted(
        escolas_com_distancia, key=lambda x: x["distancia_diretoria_km"], reverse=True
    )
    for i, escola in enumerate(escolas_ordenadas[:10], 1):
        print(
            f"   {i:2d}. {escola['name'][:40]:<40} | {escola['diretoria']:<15} | {escola['distancia_diretoria_km']:6.2f} km"
        )


def main():
    """Função principal"""
    print("🚀 SISTEMA DE ATUALIZAÇÃO DE COORDENADAS E DISTÂNCIAS")
    print("=" * 70)
    print()

    try:
        # 1. Extrair coordenadas das diretorias
        diretorias_coords = extrair_coordenadas_diretorias()

        # 2. Atualizar tabela de diretorias
        diretorias_atualizadas = atualizar_tabela_diretorias(diretorias_coords)

        # 3. Calcular/atualizar distâncias das escolas
        escolas_atualizadas = atualizar_distancias_escolas()

        # 4. Gerar relatório
        gerar_relatorio_distancias(escolas_atualizadas)

        print(f"\n✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print(f"   Arquivos atualizados:")
        print(f"   - flask_sistema/data/json/diretorias.json")
        print(f"   - dados_escolas_atualizados.json")

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        raise


if __name__ == "__main__":
    main()
