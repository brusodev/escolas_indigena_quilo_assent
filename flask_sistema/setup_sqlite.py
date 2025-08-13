#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Inicialização Simplificado para SQLite
Sistema Flask + SQLAlchemy + SQLite (migração futura para PostgreSQL)
"""

from app.models import Escola, Diretoria, Veiculo, Supervisor, Distancia
from app import create_app, db
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.insert(0, str(Path(__file__).parent))


def create_tables():
    """Cria todas as tabelas no banco SQLite"""
    print("📊 Criando tabelas SQLite...")
    db.create_all()
    print("✅ Tabelas criadas com sucesso!")


def import_data_sqlite():
    """Importa dados dos JSONs padronizados"""
    print("📥 Importando dados...")

    try:
        from app.utils.imports import import_all_data
        success = import_all_data()
        return success
    except ImportError as e:
        print(f"❌ Erro na importação: {e}")
        print("📝 Importando dados manualmente...")
        return import_basic_data()


def import_basic_data():
    """Importação básica de dados se os utilitários não funcionarem"""
    import json

    # Importar diretorias básicas
    try:
        with open('data/json/diretorias.json', 'r', encoding='utf-8') as f:
            diretorias_data = json.load(f)

        for diretoria_data in diretorias_data[:5]:  # Apenas 5 para teste
            if not Diretoria.query.filter_by(nome=diretoria_data.get('nome')).first():
                diretoria = Diretoria(
                    nome=diretoria_data.get('nome'),
                    codigo=diretoria_data.get('codigo'),
                    uf='SP',
                    total_veiculos=diretoria_data.get('total_veiculos', 0)
                )
                db.session.add(diretoria)

        db.session.commit()
        print("✅ Dados básicos importados")
        return True

    except Exception as e:
        print(f"❌ Erro na importação básica: {e}")
        return False


def init_sqlite():
    """Inicializa banco SQLite completo"""
    print("🗄️ INICIALIZANDO SISTEMA SQLITE...")
    print("=" * 50)

    # Criar aplicação
    app = create_app()

    with app.app_context():
        # Criar tabelas
        create_tables()

        # Importar dados
        success = import_data_sqlite()

        if success:
            # Mostrar estatísticas
            print("\n📊 DADOS IMPORTADOS:")
            print(f"   🏫 Escolas: {Escola.query.count()}")
            print(f"   🏛️ Diretorias: {Diretoria.query.count()}")
            print(f"   🚗 Veículos: {Veiculo.query.count()}")
            print(f"   👥 Supervisores: {Supervisor.query.count()}")
            print(f"   📏 Distâncias: {Distancia.query.count()}")

            print("\n✅ SISTEMA SQLITE PRONTO!")
            print("🚀 Execute: python run.py")
            return True
        else:
            print("⚠️ Sistema criado, mas com dados limitados")
            return False


def check_sqlite():
    """Verifica status do banco SQLite"""
    print("🔍 VERIFICANDO SISTEMA SQLITE...")

    app = create_app()

    with app.app_context():
        try:
            # Verificar arquivo de banco
            db_path = Path('data/escolas_sistema.db')
            if db_path.exists():
                print(f"✅ Banco SQLite encontrado: {db_path}")
                print(f"   📦 Tamanho: {db_path.stat().st_size / 1024:.1f} KB")
            else:
                print("❌ Banco SQLite não encontrado")
                return False

            # Testar conexão
            db.session.execute('SELECT 1')
            print("✅ Conexão: OK")

            # Contar registros
            counts = {
                'Escolas': Escola.query.count(),
                'Diretorias': Diretoria.query.count(),
                'Veículos': Veiculo.query.count(),
                'Supervisores': Supervisor.query.count(),
                'Distâncias': Distancia.query.count()
            }

            print("\n📊 REGISTROS:")
            for table, count in counts.items():
                status = "✅" if count > 0 else "⚠️"
                print(f"   {status} {table}: {count}")

            return True

        except Exception as e:
            print(f"❌ Erro: {e}")
            return False


def main():
    """Função principal"""
    print("🗄️ GERENCIADOR SQLITE")
    print("Sistema preparado para migração futura para PostgreSQL")
    print("=" * 60)

    if len(sys.argv) < 2:
        print("\nComandos disponíveis:")
        print("  init    - Inicializar sistema SQLite")
        print("  check   - Verificar status")
        print("  reset   - Resetar banco (cuidado!)")
        print("\nExemplo: python setup_sqlite.py init")
        return

    comando = sys.argv[1].lower()

    if comando == 'init':
        init_sqlite()
    elif comando == 'check':
        check_sqlite()
    elif comando == 'reset':
        print("🔄 RESET DO BANCO...")
        print("⚠️ ATENÇÃO: Todos os dados serão perdidos!")
        confirm = input("Digite 'CONFIRMAR': ")
        if confirm == 'CONFIRMAR':
            # Remove arquivo do banco
            db_path = Path('data/escolas_sistema.db')
            if db_path.exists():
                db_path.unlink()
                print("🗑️ Banco removido")
            init_sqlite()
        else:
            print("❌ Cancelado")
    else:
        print(f"❌ Comando inválido: {comando}")


if __name__ == "__main__":
    main()
