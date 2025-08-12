#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar coordenadas das diretorias no banco SQLite
e calcular distâncias entre escolas e diretorias
"""

import sys
import os
import json
import math
from datetime import datetime

# Adicionar o diretório flask_sistema ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "flask_sistema"))

from app import create_app, db
from app.models.diretoria import Diretoria
from app.models.escola import Escola
from app.models.distancia import Distancia


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine
    """
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


def atualizar_coordenadas_banco(app, diretorias_coords):
    """Atualiza as coordenadas das diretorias no banco SQLite"""
    print("\n🏛️ ATUALIZANDO COORDENADAS NO BANCO DE DADOS")
    print("=" * 60)

    with app.app_context():
        atualizadas = 0
        nao_encontradas = []

        for nome_diretoria, coords in diretorias_coords.items():
            # Buscar diretoria no banco
            diretoria = Diretoria.query.filter_by(nome=nome_diretoria).first()

            if diretoria:
                # Atualizar coordenadas
                diretoria.latitude = coords["latitude"]
                diretoria.longitude = coords["longitude"]
                if coords.get("endereco"):
                    diretoria.endereco = coords["endereco"]
                diretoria.updated_at = datetime.utcnow()

                atualizadas += 1
                print(
                    f"✅ {nome_diretoria}: ({coords['latitude']:.6f}, {coords['longitude']:.6f})"
                )
            else:
                nao_encontradas.append(nome_diretoria)
                print(f"⚠️ Diretoria não encontrada no banco: {nome_diretoria}")

        # Salvar mudanças
        try:
            db.session.commit()
            print(f"\n📊 Resumo:")
            print(f"   Diretorias atualizadas: {atualizadas}")
            print(f"   Não encontradas: {len(nao_encontradas)}")
            if nao_encontradas:
                print(f"   Lista não encontradas: {', '.join(nao_encontradas)}")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao salvar no banco: {e}")
            raise


def calcular_distancias_escolas(app):
    """Calcula distâncias entre escolas e suas diretorias"""
    print("\n📏 CALCULANDO DISTÂNCIAS ESCOLAS → DIRETORIAS")
    print("=" * 60)

    with app.app_context():
        # Buscar todas as escolas com coordenadas
        escolas = Escola.query.filter(
            Escola.latitude.isnot(None),
            Escola.longitude.isnot(None),
            Escola.diretoria_id.isnot(None),
        ).all()

        print(f"📋 Processando {len(escolas)} escolas...")

        distancias_calculadas = 0
        distancias_atualizadas = 0

        for escola in escolas:
            # Buscar diretoria relacionada
            diretoria = Diretoria.query.get(escola.diretoria_id)

            if diretoria and diretoria.latitude and diretoria.longitude:
                # Calcular distância
                distancia = calcular_distancia_haversine(
                    escola.latitude,
                    escola.longitude,
                    diretoria.latitude,
                    diretoria.longitude,
                )

                if distancia:
                    # Atualizar campo distancia_diretoria na escola
                    escola.distancia_diretoria = round(distancia, 2)
                    escola.updated_at = datetime.utcnow()

                    # Verificar se já existe registro na tabela distancias
                    distancia_existente = Distancia.query.filter_by(
                        escola_id=escola.id, diretoria_id=diretoria.id
                    ).first()

                    if distancia_existente:
                        # Atualizar registro existente
                        distancia_existente.distancia_km = round(distancia, 2)
                        distancia_existente.updated_at = datetime.utcnow()
                        distancias_atualizadas += 1
                    else:
                        # Criar novo registro
                        nova_distancia = Distancia(
                            escola_id=escola.id,
                            diretoria_id=diretoria.id,
                            distancia_km=round(distancia, 2),
                            metodo_calculo="Haversine",
                        )
                        db.session.add(nova_distancia)
                        distancias_calculadas += 1

                    # Log para verificação
                    if distancias_calculadas % 10 == 0:
                        print(
                            f"   Processadas {distancias_calculadas + distancias_atualizadas} escolas..."
                        )

        # Salvar mudanças
        try:
            db.session.commit()
            print(f"\n📊 Resumo das Distâncias:")
            print(f"   Escolas processadas: {len(escolas)}")
            print(f"   Novas distâncias calculadas: {distancias_calculadas}")
            print(f"   Distâncias atualizadas: {distancias_atualizadas}")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao salvar distâncias: {e}")
            raise


def gerar_relatorio_banco(app):
    """Gera relatório das distâncias no banco"""
    print("\n📈 RELATÓRIO DE DISTÂNCIAS NO BANCO")
    print("=" * 60)

    with app.app_context():
        # Estatísticas gerais
        total_escolas = Escola.query.count()
        escolas_com_coordenadas = Escola.query.filter(
            Escola.latitude.isnot(None), Escola.longitude.isnot(None)
        ).count()
        escolas_com_distancia = Escola.query.filter(
            Escola.distancia_diretoria.isnot(None)
        ).count()

        total_diretorias = Diretoria.query.count()
        diretorias_com_coordenadas = Diretoria.query.filter(
            Diretoria.latitude.isnot(None), Diretoria.longitude.isnot(None)
        ).count()

        total_distancias = Distancia.query.count()

        print(f"📊 Estatísticas Gerais:")
        print(f"   Total de escolas: {total_escolas}")
        print(f"   Escolas com coordenadas: {escolas_com_coordenadas}")
        print(f"   Escolas com distância calculada: {escolas_com_distancia}")
        print(f"   Total de diretorias: {total_diretorias}")
        print(f"   Diretorias com coordenadas: {diretorias_com_coordenadas}")
        print(f"   Registros na tabela distâncias: {total_distancias}")

        # Top 10 maiores distâncias
        print(f"\n🎯 Top 10 Maiores Distâncias:")
        maiores_distancias = (
            Escola.query.filter(Escola.distancia_diretoria.isnot(None))
            .order_by(Escola.distancia_diretoria.desc())
            .limit(10)
            .all()
        )

        for i, escola in enumerate(maiores_distancias, 1):
            diretoria = Diretoria.query.get(escola.diretoria_id)
            diretoria_nome = diretoria.nome if diretoria else "N/A"
            print(
                f"   {i:2d}. {escola.nome[:40]:<40} | {diretoria_nome:<15} | {escola.distancia_diretoria:6.2f} km"
            )

        # Por tipo de escola
        print(f"\n📋 Por Tipo de Escola:")
        tipos = db.session.query(Escola.tipo).distinct().all()
        for (tipo,) in tipos:
            count = Escola.query.filter_by(tipo=tipo).count()
            com_distancia = Escola.query.filter(
                Escola.tipo == tipo, Escola.distancia_diretoria.isnot(None)
            ).count()
            print(f"   {tipo}: {count} escolas, {com_distancia} com distância")


def main():
    """Função principal"""
    print("🚀 ATUALIZADOR DE COORDENADAS E DISTÂNCIAS - BANCO SQLITE")
    print("=" * 70)
    print()

    try:
        # Criar aplicação Flask
        app = create_app()

        # 1. Extrair coordenadas das diretorias
        diretorias_coords = extrair_coordenadas_diretorias()

        # 2. Atualizar coordenadas no banco
        atualizar_coordenadas_banco(app, diretorias_coords)

        # 3. Calcular distâncias
        calcular_distancias_escolas(app)

        # 4. Gerar relatório
        gerar_relatorio_banco(app)

        print(f"\n✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print(f"   Banco de dados SQLite atualizado com:")
        print(f"   - Coordenadas das diretorias")
        print(f"   - Distâncias calculadas entre escolas e diretorias")
        print(f"   - Registros na tabela distancias")

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
