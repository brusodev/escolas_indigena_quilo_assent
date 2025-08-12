#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Inicialização do Banco de Dados
Sistema Flask + SQLAlchemy + PostgreSQL
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app, db
from app.models import Escola, Diretoria, Veiculo, Supervisor, Distancia
from app.utils.imports import import_all_data


def init_database():
    """Inicializa o banco de dados"""
    print("🗄️ INICIALIZANDO BANCO DE DADOS...")
    print("=" * 50)
    
    # Criar aplicação
    app = create_app()
    
    with app.app_context():
        print("📊 Criando tabelas...")
        
        # Dropar e recriar todas as tabelas (apenas para desenvolvimento)
        db.drop_all()
        db.create_all()
        
        print("✅ Tabelas criadas com sucesso!")
        
        # Importar dados
        print("\n📥 Importando dados...")
        success = import_all_data()
        
        if success:
            # Verificar dados importados
            print("\n📊 RESUMO DOS DADOS IMPORTADOS:")
            print(f"   🏫 Escolas: {Escola.query.count()}")
            print(f"   🏛️ Diretorias: {Diretoria.query.count()}")
            print(f"   🚗 Veículos: {Veiculo.query.count()}")
            print(f"   👥 Supervisores: {Supervisor.query.count()}")
            print(f"   📏 Distâncias: {Distancia.query.count()}")
            
            print("\n🎉 BANCO DE DADOS INICIALIZADO COM SUCESSO!")
            return True
        else:
            print("\n❌ ERRO NA IMPORTAÇÃO DOS DADOS")
            return False


def reset_database():
    """Reset completo do banco de dados"""
    print("🔄 RESETANDO BANCO DE DADOS...")
    print("⚠️ ATENÇÃO: Todos os dados serão perdidos!")
    
    confirm = input("Digite 'CONFIRMAR' para continuar: ")
    if confirm != 'CONFIRMAR':
        print("❌ Operação cancelada")
        return False
    
    return init_database()


def check_database():
    """Verifica o status do banco de dados"""
    print("🔍 VERIFICANDO BANCO DE DADOS...")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Testar conexão
            db.session.execute('SELECT 1')
            print("✅ Conexão com banco: OK")
            
            # Verificar tabelas
            tables = {
                'Escolas': Escola.query.count(),
                'Diretorias': Diretoria.query.count(),
                'Veículos': Veiculo.query.count(),
                'Supervisores': Supervisor.query.count(),
                'Distâncias': Distancia.query.count()
            }
            
            print("\n📊 DADOS EXISTENTES:")
            for table, count in tables.items():
                status = "✅" if count > 0 else "⚠️"
                print(f"   {status} {table}: {count} registros")
            
            # Verificar integridade básica
            print("\n🔍 VERIFICAÇÕES DE INTEGRIDADE:")
            
            # Escolas sem coordenadas
            escolas_sem_coords = Escola.query.filter(
                (Escola.latitude.is_(None)) | (Escola.longitude.is_(None))
            ).count()
            status = "✅" if escolas_sem_coords == 0 else "⚠️"
            print(f"   {status} Escolas sem coordenadas: {escolas_sem_coords}")
            
            # Escolas sem diretoria
            escolas_sem_diretoria = Escola.query.filter(
                Escola.diretoria_id.is_(None)
            ).count()
            status = "✅" if escolas_sem_diretoria == 0 else "⚠️"
            print(f"   {status} Escolas sem diretoria: {escolas_sem_diretoria}")
            
            # Diretorias sem coordenadas
            diretorias_sem_coords = Diretoria.query.filter(
                (Diretoria.latitude.is_(None)) | (Diretoria.longitude.is_(None))
            ).count()
            status = "✅" if diretorias_sem_coords == 0 else "⚠️"
            print(f"   {status} Diretorias sem coordenadas: {diretorias_sem_coords}")
            
            print("\n✅ VERIFICAÇÃO CONCLUÍDA")
            return True
            
        except Exception as e:
            print(f"❌ Erro na verificação: {e}")
            return False


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("🗄️ GERENCIADOR DO BANCO DE DADOS")
        print("=" * 50)
        print("Uso: python init_db.py [comando]")
        print("\nComandos disponíveis:")
        print("  init     - Inicializar banco de dados")
        print("  reset    - Reset completo do banco")
        print("  check    - Verificar status do banco")
        print("\nExemplo:")
        print("  python init_db.py init")
        return
    
    comando = sys.argv[1].lower()
    
    if comando == 'init':
        init_database()
    elif comando == 'reset':
        reset_database()
    elif comando == 'check':
        check_database()
    else:
        print(f"❌ Comando inválido: {comando}")
        print("Comandos válidos: init, reset, check")


if __name__ == "__main__":
    main()
