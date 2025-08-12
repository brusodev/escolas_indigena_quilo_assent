# -*- coding: utf-8 -*-
"""
Utilitários para Importação de Dados
"""

import json
import os
from pathlib import Path
from app import db
from app.models import Escola, Diretoria, Veiculo, Supervisor, Distancia


def import_escolas(json_file_path='data/json/escolas.json'):
    """Importa dados de escolas do JSON"""
    print("📚 Importando escolas...")
    
    file_path = Path(json_file_path)
    if not file_path.exists():
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        escolas_data = json.load(f)
    
    count = 0
    for escola_data in escolas_data:
        # Verificar se já existe
        existing = Escola.query.filter_by(
            codigo_mec=escola_data.get('codigo_mec')
        ).first()
        
        if existing:
            continue
        
        # Buscar diretoria correspondente
        diretoria = None
        if escola_data.get('diretoria_nome'):
            diretoria = Diretoria.query.filter_by(
                nome=escola_data['diretoria_nome']
            ).first()
        
        escola = Escola(
            codigo_mec=escola_data.get('codigo_mec'),
            codigo=escola_data.get('codigo'),
            nome=escola_data.get('nome'),
            tipo=escola_data.get('tipo', 'regular'),
            endereco=escola_data.get('endereco'),
            cidade=escola_data.get('cidade'),
            uf=escola_data.get('uf', 'SP'),
            zona=escola_data.get('zona', 'Urbana'),
            situacao=escola_data.get('situacao', 1),
            latitude=escola_data.get('latitude'),
            longitude=escola_data.get('longitude'),
            diretoria_id=diretoria.id if diretoria else None,
            diretoria_nome=escola_data.get('diretoria_nome'),
            distancia_diretoria=escola_data.get('distancia_diretoria'),
            codigo_ibge=escola_data.get('codigo_ibge'),
            tipo_original=escola_data.get('tipo_original')
        )
        
        db.session.add(escola)
        count += 1
    
    try:
        db.session.commit()
        print(f"✅ {count} escolas importadas com sucesso")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao importar escolas: {e}")
        return False


def import_diretorias(json_file_path='data/json/diretorias.json'):
    """Importa dados de diretorias do JSON"""
    print("🏛️ Importando diretorias...")
    
    file_path = Path(json_file_path)
    if not file_path.exists():
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        diretorias_data = json.load(f)
    
    count = 0
    for diretoria_data in diretorias_data:
        # Verificar se já existe
        existing = Diretoria.query.filter_by(
            nome=diretoria_data.get('nome')
        ).first()
        
        if existing:
            continue
        
        diretoria = Diretoria(
            nome=diretoria_data.get('nome'),
            codigo=diretoria_data.get('codigo'),
            uf=diretoria_data.get('uf', 'SP'),
            regiao=diretoria_data.get('regiao'),
            total_veiculos=diretoria_data.get('total_veiculos', 0),
            veiculos_s1=diretoria_data.get('veiculos_s1', 0),
            veiculos_s2=diretoria_data.get('veiculos_s2', 0),
            veiculos_s2_4x4=diretoria_data.get('veiculos_s2_4x4', 0),
            latitude=diretoria_data.get('latitude'),
            longitude=diretoria_data.get('longitude')
        )
        
        db.session.add(diretoria)
        count += 1
    
    try:
        db.session.commit()
        print(f"✅ {count} diretorias importadas com sucesso")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao importar diretorias: {e}")
        return False


def import_veiculos(json_file_path='data/json/veiculos.json'):
    """Importa dados de veículos do JSON"""
    print("🚗 Importando veículos...")
    
    file_path = Path(json_file_path)
    if not file_path.exists():
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        veiculos_data = json.load(f)
    
    count = 0
    for veiculo_data in veiculos_data:
        # Buscar diretoria correspondente
        diretoria = Diretoria.query.filter_by(
            nome=veiculo_data.get('diretoria_nome')
        ).first()
        
        if not diretoria:
            print(f"⚠️ Diretoria não encontrada: {veiculo_data.get('diretoria_nome')}")
            continue
        
        veiculo = Veiculo(
            tipo=veiculo_data.get('tipo'),
            descricao=veiculo_data.get('descricao'),
            placa=veiculo_data.get('placa'),
            modelo=veiculo_data.get('modelo'),
            ano=veiculo_data.get('ano'),
            capacidade=veiculo_data.get('capacidade'),
            status=veiculo_data.get('status', 'Ativo'),
            diretoria_id=diretoria.id
        )
        
        db.session.add(veiculo)
        count += 1
    
    try:
        db.session.commit()
        print(f"✅ {count} veículos importados com sucesso")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao importar veículos: {e}")
        return False


def calcular_distancias():
    """Calcula e importa distâncias entre escolas e diretorias"""
    print("📏 Calculando distâncias...")
    
    from .calculations import calcular_distancia_haversine
    
    escolas = Escola.query.filter(
        Escola.latitude.isnot(None),
        Escola.longitude.isnot(None),
        Escola.diretoria_id.isnot(None)
    ).all()
    
    count = 0
    for escola in escolas:
        diretoria = escola.diretoria
        if not diretoria or not diretoria.latitude or not diretoria.longitude:
            continue
        
        # Verificar se já existe
        existing = Distancia.query.filter_by(
            escola_id=escola.id,
            diretoria_id=diretoria.id
        ).first()
        
        if existing:
            continue
        
        # Calcular distância
        distancia_km = calcular_distancia_haversine(
            escola.latitude, escola.longitude,
            diretoria.latitude, diretoria.longitude
        )
        
        distancia = Distancia(
            escola_id=escola.id,
            diretoria_id=diretoria.id,
            distancia_km=distancia_km,
            metodo_calculo='Haversine'
        )
        
        db.session.add(distancia)
        count += 1
    
    try:
        db.session.commit()
        print(f"✅ {count} distâncias calculadas com sucesso")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao calcular distâncias: {e}")
        return False


def import_all_data():
    """Importa todos os dados na ordem correta"""
    print("🚀 INICIANDO IMPORTAÇÃO COMPLETA...")
    print("=" * 50)
    
    # Ordem: diretorias -> escolas -> veículos -> distâncias
    success = True
    success &= import_diretorias()
    success &= import_escolas()
    success &= import_veiculos()
    success &= calcular_distancias()
    
    if success:
        print("🎉 IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
    else:
        print("❌ IMPORTAÇÃO FINALIZADA COM ERROS")
    
    return success
