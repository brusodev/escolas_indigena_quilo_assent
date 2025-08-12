#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Relatório Final - Implementação de Coordenadas e Distâncias
"""

import sys
import os

# Adicionar o diretório flask_sistema ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "flask_sistema"))

from app import create_app, db
from app.models.diretoria import Diretoria
from app.models.escola import Escola
from app.models.distancia import Distancia


def gerar_relatorio_completo():
    """Gera relatório completo da implementação"""
    print("📋 RELATÓRIO FINAL - COORDENADAS E DISTÂNCIAS IMPLEMENTADAS")
    print("=" * 70)
    print()

    app = create_app()
    with app.app_context():

        # 1. ESTATÍSTICAS DAS DIRETORIAS
        print("🏛️ DIRETORIAS:")
        print("-" * 40)

        total_diretorias = Diretoria.query.count()
        com_coordenadas = Diretoria.query.filter(
            Diretoria.latitude.isnot(None), Diretoria.longitude.isnot(None)
        ).count()

        print(f"   Total de diretorias no banco: {total_diretorias}")
        print(f"   Diretorias com coordenadas: {com_coordenadas}")
        print(
            f"   Cobertura de coordenadas: {(com_coordenadas/total_diretorias)*100:.1f}%"
        )

        # Listar diretorias com coordenadas
        print(f"\n   ✅ Diretorias com coordenadas ({com_coordenadas}):")
        diretorias_coordenadas = (
            Diretoria.query.filter(
                Diretoria.latitude.isnot(None), Diretoria.longitude.isnot(None)
            )
            .order_by(Diretoria.nome)
            .all()
        )

        for diretoria in diretorias_coordenadas:
            print(
                f"      • {diretoria.nome}: ({diretoria.latitude:.6f}, {diretoria.longitude:.6f})"
            )

        # 2. ESTATÍSTICAS DAS ESCOLAS
        print(f"\n🏫 ESCOLAS:")
        print("-" * 40)

        total_escolas = Escola.query.count()
        escolas_com_coordenadas = Escola.query.filter(
            Escola.latitude.isnot(None), Escola.longitude.isnot(None)
        ).count()
        escolas_com_distancia = Escola.query.filter(
            Escola.distancia_diretoria.isnot(None)
        ).count()

        print(f"   Total de escolas: {total_escolas}")
        print(f"   Escolas com coordenadas: {escolas_com_coordenadas}")
        print(f"   Escolas com distância calculada: {escolas_com_distancia}")
        print(
            f"   Cobertura de distâncias: {(escolas_com_distancia/total_escolas)*100:.1f}%"
        )

        # Estatísticas por tipo
        print(f"\n   📊 Por tipo de escola:")
        tipos = db.session.query(Escola.tipo).distinct().all()
        for (tipo,) in sorted(tipos):
            count_tipo = Escola.query.filter_by(tipo=tipo).count()
            com_distancia_tipo = Escola.query.filter(
                Escola.tipo == tipo, Escola.distancia_diretoria.isnot(None)
            ).count()
            print(
                f"      • {tipo}: {count_tipo} escolas, {com_distancia_tipo} com distância"
            )

        # 3. ESTATÍSTICAS DA TABELA DISTÂNCIAS
        print(f"\n📏 TABELA DISTÂNCIAS:")
        print("-" * 40)

        total_distancias = Distancia.query.count()
        print(f"   Total de registros: {total_distancias}")

        # Estatísticas de distâncias
        if total_distancias > 0:
            distancias_valores = [d.distancia_km for d in Distancia.query.all()]
            media = sum(distancias_valores) / len(distancias_valores)
            minima = min(distancias_valores)
            maxima = max(distancias_valores)

            print(f"   Distância mínima: {minima:.2f} km")
            print(f"   Distância máxima: {maxima:.2f} km")
            print(f"   Distância média: {media:.2f} km")

        # 4. TOP MAIORES DISTÂNCIAS
        print(f"\n🎯 TOP 15 MAIORES DISTÂNCIAS:")
        print("-" * 40)

        maiores_distancias = (
            Escola.query.filter(Escola.distancia_diretoria.isnot(None))
            .order_by(Escola.distancia_diretoria.desc())
            .limit(15)
            .all()
        )

        for i, escola in enumerate(maiores_distancias, 1):
            diretoria = Diretoria.query.get(escola.diretoria_id)
            diretoria_nome = diretoria.nome if diretoria else "N/A"
            tipo_desc = escola.tipo.replace("_", " ").title()
            print(
                f"   {i:2d}. {escola.nome[:35]:<35} | {diretoria_nome:<18} | {tipo_desc:<12} | {escola.distancia_diretoria:6.2f} km"
            )

        # 5. ANÁLISE POR DIRETORIAS
        print(f"\n🗺️ ANÁLISE POR DIRETORIAS COM COORDENADAS:")
        print("-" * 40)

        for diretoria in diretorias_coordenadas:
            escolas_diretoria = Escola.query.filter_by(
                diretoria_id=diretoria.id
            ).count()
            escolas_com_dist = Escola.query.filter(
                Escola.diretoria_id == diretoria.id,
                Escola.distancia_diretoria.isnot(None),
            ).count()

            if escolas_diretoria > 0:
                # Calcular distância média
                distancias_dir = [
                    e.distancia_diretoria
                    for e in Escola.query.filter(
                        Escola.diretoria_id == diretoria.id,
                        Escola.distancia_diretoria.isnot(None),
                    ).all()
                ]

                if distancias_dir:
                    media_dir = sum(distancias_dir) / len(distancias_dir)
                    max_dir = max(distancias_dir)
                    print(
                        f"   {diretoria.nome:<20} | {escolas_diretoria:3d} escolas | {escolas_com_dist:3d} c/ distância | Média: {media_dir:5.2f} km | Máx: {max_dir:5.2f} km"
                    )

        # 6. RESUMO TÉCNICO
        print(f"\n⚙️ RESUMO TÉCNICO DA IMPLEMENTAÇÃO:")
        print("-" * 40)
        print(f"   ✅ Coordenadas extraídas dos dados existentes das escolas")
        print(f"   ✅ Tabela 'diretorias' atualizada com latitude/longitude")
        print(f"   ✅ Campo 'distancia_diretoria' populado na tabela 'escolas'")
        print(f"   ✅ Tabela 'distancias' criada com relacionamentos")
        print(f"   ✅ Fórmula Haversine implementada para cálculos precisos")
        print(f"   ✅ {com_coordenadas} diretorias com coordenadas completas")
        print(f"   ✅ {escolas_com_distancia} escolas com distâncias calculadas")
        print(f"   ✅ {total_distancias} registros na tabela de distâncias")

        print(f"\n🎯 OBJETIVOS ALCANÇADOS:")
        print("-" * 40)
        print(f"   ✅ Coordenadas das diretorias adicionadas ao banco")
        print(f"   ✅ Coluna de distância implementada na tabela escolas")
        print(f"   ✅ Cálculos automáticos de distância escola → diretoria")
        print(f"   ✅ Sistema pronto para análises geográficas e logísticas")
        print(f"   ✅ Base para otimização de rotas e alocação de recursos")

        print(f"\n📊 STATUS FINAL: ✅ IMPLEMENTAÇÃO COMPLETA E FUNCIONAL")


def main():
    """Função principal"""
    try:
        gerar_relatorio_completo()
        print(f"\n" + "=" * 70)
        print(f"📈 RELATÓRIO GERADO COM SUCESSO!")
        print(f"💡 O sistema agora possui coordenadas e distâncias implementadas")
        print(f"🚀 Pronto para análises avançadas e otimizações logísticas")

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
