#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATUALIZAÇÃO SIMPLES DO SISTEMA FLASK
===================================
"""

import sqlite3
import shutil
import os


def atualizar_sistema_flask():
    """Atualiza o sistema Flask com os dados consolidados."""

    print("🔄 ATUALIZANDO SISTEMA FLASK")
    print("=" * 40)

    # 1. Copiar banco consolidado
    print("\n1. 📋 Copiando banco consolidado...")
    banco_origem = '../dados/consolidados/banco_completo_91_diretorias.db'
    banco_destino = 'instance/escolas_sistema_91.db'

    # Criar pasta instance
    os.makedirs('instance', exist_ok=True)

    if os.path.exists(banco_origem):
        shutil.copy2(banco_origem, banco_destino)
        print(f"✅ Banco copiado para: {banco_destino}")

        # Verificar
        conn = sqlite3.connect(banco_destino)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM diretorias")
        diretorias = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM escolas")
        escolas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tipos_escola")
        tipos = cursor.fetchone()[0]

        conn.close()

        print(
            f"✅ Verificação: {diretorias} diretorias, {escolas:,} escolas, {tipos} tipos")

    else:
        print(f"❌ Banco não encontrado: {banco_origem}")
        return False

    # 2. Criar rota de teste simples
    print("\n2. 🌐 Criando rota de teste...")

    rota_teste = '''from flask import Blueprint, jsonify, render_template_string
import sqlite3
import os

test_91_bp = Blueprint('test_91', __name__)

def get_db():
    conn = sqlite3.connect('instance/escolas_sistema_91.db')
    conn.row_factory = sqlite3.Row
    return conn

@test_91_bp.route('/teste-91')
def teste_91_diretorias():
    """Testa as 91 diretorias."""
    try:
        conn = get_db()

        # Contar diretorias
        total_diretorias = conn.execute(
            'SELECT COUNT(*) FROM diretorias').fetchone()[0]

        # Listar algumas diretorias com siglas
        diretorias = conn.execute('''
            SELECT nome, sigla, total_escolas
            FROM diretorias
            ORDER BY total_escolas DESC
            LIMIT 10
        ''').fetchall()
        
        # Tipos de escola
        tipos = conn.execute('''
            SELECT codigo, nome, total_escolas 
            FROM tipos_escola 
            ORDER BY codigo
        ''').fetchall()
        
        conn.close()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Teste 91 Diretorias</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .sigla {{ background: #007bff; color: white; padding: 2px 6px; border-radius: 3px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>✅ Sistema Atualizado - {total_diretorias} Diretorias</h1>
            
            <h2>🏆 Top 10 Diretorias por Escolas</h2>
            <table>
                <tr><th>Nome</th><th>Sigla</th><th>Total Escolas</th></tr>
                {''.join(f'<tr><td>{d["nome"]}</td><td><span class="sigla">{d["sigla"]}</span></td><td>{d["total_escolas"]}</td></tr>' for d in diretorias)}
            </table>
            
            <h2>🏫 Tipos de Escola ({len(tipos)} tipos)</h2>
            <table>
                <tr><th>Código</th><th>Nome</th><th>Total</th></tr>
                {''.join(f'<tr><td>{t["codigo"]}</td><td>{t["nome"]}</td><td>{t["total_escolas"]}</td></tr>' for t in tipos)}
            </table>
            
            <p><strong>Status:</strong> ✅ Sistema Flask atualizado com sucesso!</p>
            <p><strong>Data:</strong> 12/08/2025</p>
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        return f"❌ Erro: {str(e)}"

@test_91_bp.route('/api/teste-diretorias')
def api_teste_diretorias():
    """API de teste para as diretorias."""
    try:
        conn = get_db()
        
        diretorias = conn.execute('''
            SELECT nome, sigla, total_escolas 
            FROM diretorias 
            ORDER BY nome
        ''').fetchall()
        
        conn.close()
        
        resultado = []
        for d in diretorias:
            resultado.append({
                'nome': d['nome'],
                'sigla': d['sigla'],
                'total_escolas': d['total_escolas']
            })
        
        return jsonify({
            'success': True,
            'total_diretorias': len(resultado),
            'diretorias': resultado
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
'''
    
    # Salvar rota de teste
    os.makedirs('app/routes', exist_ok=True)
    with open('app/routes/teste_91.py', 'w', encoding='utf-8') as f:
        f.write(rota_teste)
    
    print("✅ Rota de teste criada: /teste-91")
    
    # 3. Atualizar __init__.py se existir
    print("\n3. 🚀 Atualizando registro de rotas...")
    
    if os.path.exists('app/__init__.py'):
        with open('app/__init__.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar import e registro
        if 'teste_91' not in content:
            # Adicionar no final
            content += '''
# Rota de teste para 91 diretorias
try:
    from app.routes.teste_91 import test_91_bp
    app.register_blueprint(test_91_bp)
except ImportError:
    pass
'''
            
            with open('app/__init__.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ __init__.py atualizado")
    
    print(f"\n🎉 ATUALIZAÇÃO CONCLUÍDA!")
    print(f"✅ Banco com 91 diretorias instalado")
    print(f"✅ Rota de teste disponível: /teste-91")
    print(f"✅ API de teste: /api/teste-diretorias")
    
    return True


if __name__ == "__main__":
    atualizar_sistema_flask()
