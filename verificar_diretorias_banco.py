#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar e corrigir diretorias não encontradas no banco
"""

import sys
import os
import json

# Adicionar o diretório flask_sistema ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "flask_sistema"))

from app import create_app, db
from app.models.diretoria import Diretoria
from datetime import datetime


def verificar_diretorias_nao_encontradas():
    """Verifica as diretorias que não foram encontradas e sugere correções"""
    print("🔍 VERIFICANDO DIRETORIAS NÃO ENCONTRADAS")
    print("=" * 60)

    # Carregar dados das escolas
    with open("dados_escolas_atualizados.json", "r", encoding="utf-8") as f:
        escolas = json.load(f)

    # Diretorias não encontradas no último log
    nao_encontradas = [
        "Mirante do Paranapanema",
        "Sao Bernardo do Campo",
        "SÃO VICENTE",
    ]

    app = create_app()
    with app.app_context():
        # Listar todas as diretorias no banco
        diretorias_banco = Diretoria.query.all()
        nomes_banco = [d.nome for d in diretorias_banco]

        print(f"📋 Diretorias no banco ({len(nomes_banco)}):")
        for nome in sorted(nomes_banco):
            print(f"   - {nome}")

        print(f"\n⚠️ Diretorias não encontradas:")
        for nome in nao_encontradas:
            print(f"   - {nome}")

            # Buscar por coordenadas dessas diretorias
            coords_encontradas = None
            for escola in escolas:
                if escola.get("diretoria") == nome:
                    coords_encontradas = {
                        "latitude": escola.get("de_lat"),
                        "longitude": escola.get("de_lng"),
                        "endereco": escola.get("endereco_diretoria"),
                    }
                    break

            if coords_encontradas:
                print(
                    f"     Coordenadas: ({coords_encontradas['latitude']}, {coords_encontradas['longitude']})"
                )
                print(f"     Endereço: {coords_encontradas['endereco']}")

                # Tentar encontrar correspondência no banco
                correspondencias = []
                for nome_banco in nomes_banco:
                    if (
                        nome.lower() in nome_banco.lower()
                        or nome_banco.lower() in nome.lower()
                    ):
                        correspondencias.append(nome_banco)

                if correspondencias:
                    print(
                        f"     Possíveis correspondências: {', '.join(correspondencias)}"
                    )
                else:
                    print(
                        f"     ❌ Nenhuma correspondência encontrada - requer criação manual"
                    )
            else:
                print(f"     ❌ Coordenadas não encontradas")


def criar_diretorias_faltantes():
    """Cria as diretorias que estão faltando no banco"""
    print("\n🏗️ CRIANDO DIRETORIAS FALTANTES")
    print("=" * 60)

    # Carregar dados das escolas
    with open("dados_escolas_atualizados.json", "r", encoding="utf-8") as f:
        escolas = json.load(f)

    # Diretorias para criar
    diretorias_criar = {
        "Mirante do Paranapanema": {"codigo": "DE092", "regiao": "Interior"},
        "Sao Bernardo do Campo": {"codigo": "DE093", "regiao": "Grande São Paulo"},
        "SÃO VICENTE": {"codigo": "DE094", "regiao": "Baixada Santista"},
    }

    app = create_app()
    with app.app_context():
        criadas = 0

        for nome_diretoria, info in diretorias_criar.items():
            # Verificar se já existe
            existe = Diretoria.query.filter_by(nome=nome_diretoria).first()
            if existe:
                print(f"⚠️ {nome_diretoria} já existe no banco")
                continue

            # Buscar coordenadas nos dados das escolas
            coords = None
            endereco = None
            for escola in escolas:
                if escola.get("diretoria") == nome_diretoria:
                    coords = {
                        "latitude": escola.get("de_lat"),
                        "longitude": escola.get("de_lng"),
                    }
                    endereco = escola.get("endereco_diretoria")
                    break

            if coords and coords["latitude"] and coords["longitude"]:
                # Criar nova diretoria
                nova_diretoria = Diretoria(
                    nome=nome_diretoria,
                    codigo=info["codigo"],
                    regiao=info["regiao"],
                    latitude=coords["latitude"],
                    longitude=coords["longitude"],
                    endereco=endereco,
                    uf="SP",
                    total_veiculos=0,
                    veiculos_s1=0,
                    veiculos_s2=0,
                    veiculos_s2_4x4=0,
                )

                db.session.add(nova_diretoria)
                criadas += 1
                print(
                    f"✅ {nome_diretoria}: ({coords['latitude']:.6f}, {coords['longitude']:.6f})"
                )
            else:
                print(f"❌ {nome_diretoria}: Coordenadas não encontradas")

        # Salvar mudanças
        try:
            db.session.commit()
            print(f"\n📊 Resumo:")
            print(f"   Diretorias criadas: {criadas}")

            if criadas > 0:
                print(
                    f"\n🔄 Execute novamente o script de cálculo de distâncias para processar as novas diretorias"
                )

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao criar diretorias: {e}")
            raise


def relatorio_final():
    """Gera relatório final das diretorias no banco"""
    print("\n📋 RELATÓRIO FINAL DAS DIRETORIAS")
    print("=" * 60)

    app = create_app()
    with app.app_context():
        # Estatísticas das diretorias
        total_diretorias = Diretoria.query.count()
        com_coordenadas = Diretoria.query.filter(
            Diretoria.latitude.isnot(None), Diretoria.longitude.isnot(None)
        ).count()

        print(f"📊 Estatísticas:")
        print(f"   Total de diretorias: {total_diretorias}")
        print(f"   Com coordenadas: {com_coordenadas}")
        print(f"   Sem coordenadas: {total_diretorias - com_coordenadas}")

        # Diretorias sem coordenadas
        sem_coordenadas = Diretoria.query.filter(
            db.or_(Diretoria.latitude.is_(None), Diretoria.longitude.is_(None))
        ).all()

        if sem_coordenadas:
            print(f"\n⚠️ Diretorias sem coordenadas ({len(sem_coordenadas)}):")
            for diretoria in sem_coordenadas:
                print(f"   - {diretoria.nome} (ID: {diretoria.id})")


def main():
    """Função principal"""
    print("🔧 VERIFICADOR E CORRETOR DE DIRETORIAS")
    print("=" * 50)
    print()

    try:
        # 1. Verificar diretorias não encontradas
        verificar_diretorias_nao_encontradas()

        # 2. Criar diretorias faltantes
        criar_diretorias_faltantes()

        # 3. Relatório final
        relatorio_final()

        print(f"\n✅ VERIFICAÇÃO CONCLUÍDA!")

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
