#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir dados da ALDEIA KOPENOTI
"""

import sys
import os

# Adicionar o diretório flask_sistema ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "flask_sistema"))

from app import create_app, db
from app.models.diretoria import Diretoria
from app.models.escola import Escola
from app.models.distancia import Distancia
import math


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine"""
    if not all([lat1, lon1, lat2, lon2]):
        return None

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


def verificar_aldeia_kopenoti():
    """Verifica as informações atuais da ALDEIA KOPENOTI"""
    print("🔍 VERIFICANDO DADOS ATUAIS DA ALDEIA KOPENOTI")
    print("=" * 60)

    app = create_app()
    with app.app_context():
        # Buscar escola ALDEIA KOPENOTI
        kopenoti = Escola.query.filter(Escola.nome.like("%KOPENOTI%")).first()

        if kopenoti:
            print(f"📋 Dados atuais encontrados:")
            print(f"   ID: {kopenoti.id}")
            print(f"   Nome: {kopenoti.nome}")
            print(f"   Cidade: {kopenoti.cidade}")
            print(f"   Endereço: {kopenoti.endereco}")
            print(f"   Coordenadas: ({kopenoti.latitude}, {kopenoti.longitude})")
            print(f"   Diretoria ID: {kopenoti.diretoria_id}")
            print(f"   Distância atual: {kopenoti.distancia_diretoria} km")

            # Buscar diretoria atual
            if kopenoti.diretoria_id:
                diretoria_atual = Diretoria.query.get(kopenoti.diretoria_id)
                if diretoria_atual:
                    print(f"   Diretoria atual: {diretoria_atual.nome}")
                    print(
                        f"   Coord. Diretoria: ({diretoria_atual.latitude}, {diretoria_atual.longitude})"
                    )

            return kopenoti
        else:
            print("❌ ALDEIA KOPENOTI não encontrada!")
            return None


def encontrar_diretoria_mais_proxima(escola):
    """Encontra a diretoria mais próxima da escola"""
    print(f"\n🗺️ CALCULANDO DIRETORIA MAIS PRÓXIMA")
    print("=" * 60)

    app = create_app()
    with app.app_context():
        # Buscar todas as diretorias com coordenadas
        diretorias = Diretoria.query.filter(
            Diretoria.latitude.isnot(None), Diretoria.longitude.isnot(None)
        ).all()

        distancias = []
        for diretoria in diretorias:
            distancia = calcular_distancia_haversine(
                escola.latitude,
                escola.longitude,
                diretoria.latitude,
                diretoria.longitude,
            )
            if distancia:
                distancias.append((diretoria, distancia))

        # Ordenar por distância
        distancias.sort(key=lambda x: x[1])

        print(f"📊 Top 5 diretorias mais próximas:")
        for i, (diretoria, dist) in enumerate(distancias[:5], 1):
            print(f"   {i}. {diretoria.nome}: {dist:.2f} km")

        if distancias:
            return distancias[0]  # Retorna a mais próxima
        return None, None


def corrigir_aldeia_kopenoti():
    """Corrige os dados da ALDEIA KOPENOTI"""
    print(f"\n🔧 CORRIGINDO DADOS DA ALDEIA KOPENOTI")
    print("=" * 60)

    # Dados corretos conforme fornecido
    dados_corretos = {
        "nome": "ALDEIA KOPENOTI",
        "endereco": "Posto Indigena Kopenoti, S/N - Aldeia Kopenoti, Avaí - SP, 16680-000",
        "cidade": "AVAI",
        "latitude": -22.264515,
        "longitude": -49.35027069,
        "tipo": "indigena",
        "zona": "Rural",
    }

    app = create_app()
    with app.app_context():
        # Buscar a escola
        kopenoti = Escola.query.filter(Escola.nome.like("%KOPENOTI%")).first()

        if not kopenoti:
            print("❌ Escola não encontrada!")
            return

        print(f"✅ Escola encontrada: {kopenoti.nome}")

        # Atualizar dados da escola
        kopenoti.endereco = dados_corretos["endereco"]
        kopenoti.cidade = dados_corretos["cidade"]
        kopenoti.latitude = dados_corretos["latitude"]
        kopenoti.longitude = dados_corretos["longitude"]
        kopenoti.tipo = dados_corretos["tipo"]
        kopenoti.zona = dados_corretos["zona"]

        print(f"✅ Dados da escola atualizados")

        # Encontrar diretoria mais próxima com as coordenadas corretas
        diretorias = Diretoria.query.filter(
            Diretoria.latitude.isnot(None), Diretoria.longitude.isnot(None)
        ).all()

        melhor_diretoria = None
        menor_distancia = float("inf")

        for diretoria in diretorias:
            distancia = calcular_distancia_haversine(
                dados_corretos["latitude"],
                dados_corretos["longitude"],
                diretoria.latitude,
                diretoria.longitude,
            )
            if distancia and distancia < menor_distancia:
                menor_distancia = distancia
                melhor_diretoria = diretoria

        if melhor_diretoria:
            # Atualizar diretoria
            diretoria_anterior = kopenoti.diretoria_id
            kopenoti.diretoria_id = melhor_diretoria.id
            kopenoti.diretoria_nome = melhor_diretoria.nome
            kopenoti.distancia_diretoria = round(menor_distancia, 2)

            print(f"✅ Diretoria corrigida:")
            print(f"   Anterior: ID {diretoria_anterior}")
            print(f"   Nova: {melhor_diretoria.nome} (ID {melhor_diretoria.id})")
            print(f"   Nova distância: {menor_distancia:.2f} km")

            # Atualizar registro na tabela distancias
            # Remover registro antigo se existir
            distancia_antiga = Distancia.query.filter_by(
                escola_id=kopenoti.id, diretoria_id=diretoria_anterior
            ).first()

            if distancia_antiga:
                db.session.delete(distancia_antiga)
                print(f"✅ Registro antigo de distância removido")

            # Verificar se já existe registro para a nova diretoria
            distancia_nova = Distancia.query.filter_by(
                escola_id=kopenoti.id, diretoria_id=melhor_diretoria.id
            ).first()

            if distancia_nova:
                # Atualizar existente
                distancia_nova.distancia_km = round(menor_distancia, 2)
                print(f"✅ Registro de distância atualizado")
            else:
                # Criar novo
                nova_distancia = Distancia(
                    escola_id=kopenoti.id,
                    diretoria_id=melhor_diretoria.id,
                    distancia_km=round(menor_distancia, 2),
                    metodo_calculo="Haversine",
                )
                db.session.add(nova_distancia)
                print(f"✅ Novo registro de distância criado")

            # Salvar mudanças
            try:
                db.session.commit()
                print(f"\n✅ CORREÇÃO SALVA COM SUCESSO!")
                return kopenoti, melhor_diretoria

            except Exception as e:
                db.session.rollback()
                print(f"❌ Erro ao salvar: {e}")
                raise
        else:
            print("❌ Nenhuma diretoria com coordenadas encontrada!")
            return None, None


def verificar_correcao():
    """Verifica se a correção foi aplicada corretamente"""
    print(f"\n✅ VERIFICANDO CORREÇÃO APLICADA")
    print("=" * 60)

    app = create_app()
    with app.app_context():
        kopenoti = Escola.query.filter(Escola.nome.like("%KOPENOTI%")).first()

        if kopenoti:
            print(f"📋 Dados após correção:")
            print(f"   Nome: {kopenoti.nome}")
            print(f"   Cidade: {kopenoti.cidade}")
            print(f"   Endereço: {kopenoti.endereco}")
            print(f"   Coordenadas: ({kopenoti.latitude}, {kopenoti.longitude})")
            print(
                f"   Diretoria: {kopenoti.diretoria_nome} (ID: {kopenoti.diretoria_id})"
            )
            print(f"   Distância: {kopenoti.distancia_diretoria} km")

            # Verificar registro na tabela distancias
            distancia_reg = Distancia.query.filter_by(escola_id=kopenoti.id).first()
            if distancia_reg:
                diretoria = Diretoria.query.get(distancia_reg.diretoria_id)
                print(
                    f"   Registro distância: {distancia_reg.distancia_km} km → {diretoria.nome if diretoria else 'N/A'}"
                )

            return True
        else:
            print("❌ Escola não encontrada após correção!")
            return False


def main():
    """Função principal"""
    print("🔧 CORREÇÃO DOS DADOS DA ALDEIA KOPENOTI")
    print("=" * 70)
    print()

    try:
        # 1. Verificar dados atuais
        escola_atual = verificar_aldeia_kopenoti()

        if not escola_atual:
            return

        # 2. Encontrar diretoria mais próxima (informativo)
        diretoria_proxima, distancia_proxima = encontrar_diretoria_mais_proxima(
            escola_atual
        )

        # 3. Corrigir dados
        escola_corrigida, nova_diretoria = corrigir_aldeia_kopenoti()

        if escola_corrigida and nova_diretoria:
            # 4. Verificar correção
            verificar_correcao()

            print(f"\n🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
            print(f"   A ALDEIA KOPENOTI foi corrigida e está agora")
            print(f"   associada corretamente à diretoria {nova_diretoria.nome}")

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
