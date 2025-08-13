# -*- coding: utf-8 -*-
"""
Utilitários para Cálculos Matemáticos
"""

import math


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula a distância entre dois pontos na Terra usando a fórmula de Haversine

    Args:
        lat1, lon1: Latitude e longitude do primeiro ponto
        lat2, lon2: Latitude e longitude do segundo ponto

    Returns:
        Distância em quilômetros
    """
    # Converter coordenadas para radianos
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferenças
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = (math.sin(dlat/2)**2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))

    # Raio da Terra em km
    r = 6371

    # Calcular distância
    distance = c * r

    return round(distance, 2)


def calcular_estatisticas_distancia(distancias):
    """
    Calcula estatísticas de uma lista de distâncias

    Args:
        distancias: Lista de valores de distância

    Returns:
        Dicionário com estatísticas
    """
    if not distancias:
        return {
            'total': 0,
            'media': 0,
            'minima': 0,
            'maxima': 0,
            'mediana': 0
        }

    distancias_sorted = sorted(distancias)
    n = len(distancias)

    # Mediana
    if n % 2 == 0:
        mediana = (distancias_sorted[n//2 - 1] + distancias_sorted[n//2]) / 2
    else:
        mediana = distancias_sorted[n//2]

    return {
        'total': n,
        'media': round(sum(distancias) / n, 2),
        'minima': min(distancias),
        'maxima': max(distancias),
        'mediana': round(mediana, 2)
    }


def classificar_distancia(distancia_km):
    """
    Classifica uma distância em categorias

    Args:
        distancia_km: Distância em quilômetros

    Returns:
        Categoria da distância
    """
    if distancia_km <= 10:
        return 'Muito Próxima'
    elif distancia_km <= 25:
        return 'Próxima'
    elif distancia_km <= 50:
        return 'Média'
    elif distancia_km <= 100:
        return 'Distante'
    else:
        return 'Muito Distante'


def calcular_tempo_estimado(distancia_km, velocidade_media=60):
    """
    Calcula tempo estimado de viagem

    Args:
        distancia_km: Distância em quilômetros
        velocidade_media: Velocidade média em km/h (padrão: 60 km/h)

    Returns:
        Tempo em minutos
    """
    tempo_horas = distancia_km / velocidade_media
    tempo_minutos = tempo_horas * 60
    return round(tempo_minutos)


def converter_coordenadas_dms_para_decimal(graus, minutos, segundos, hemisferio):
    """
    Converte coordenadas de graus, minutos e segundos para decimal

    Args:
        graus: Graus
        minutos: Minutos
        segundos: Segundos
        hemisferio: 'N', 'S', 'E', 'W'

    Returns:
        Coordenada em decimal
    """
    decimal = graus + (minutos / 60) + (segundos / 3600)

    if hemisferio in ['S', 'W']:
        decimal = -decimal

    return decimal


def validar_coordenadas(latitude, longitude):
    """
    Valida se as coordenadas estão dentro dos limites válidos

    Args:
        latitude: Latitude
        longitude: Longitude

    Returns:
        True se válidas, False caso contrário
    """
    if latitude is None or longitude is None:
        return False

    if not (-90 <= latitude <= 90):
        return False

    if not (-180 <= longitude <= 180):
        return False

    return True


def coordenadas_brasil_validas(latitude, longitude):
    """
    Verifica se as coordenadas estão dentro do território brasileiro

    Args:
        latitude: Latitude
        longitude: Longitude

    Returns:
        True se dentro do Brasil, False caso contrário
    """
    if not validar_coordenadas(latitude, longitude):
        return False

    # Limites aproximados do Brasil
    lat_min, lat_max = -33.7, 5.3
    lon_min, lon_max = -73.9, -28.8

    return (lat_min <= latitude <= lat_max and
            lon_min <= longitude <= lon_max)
