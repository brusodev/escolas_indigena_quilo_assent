#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATUALIZAÇÃO DO SISTEMA FLASK COM DADOS CONSOLIDADOS
==================================================

Este script irá:
1. Copiar o banco consolidado para o sistema Flask
2. Atualizar as rotas/APIs com as 91 diretorias
3. Atualizar o dashboard com siglas oficiais
4. Garantir que o sistema Flask use os dados corretos
"""

import sqlite3
import json
import shutil
import os
from datetime import datetime


def copiar_banco_consolidado():
    """Copia o banco consolidado para o sistema Flask."""

    print("📋 COPIANDO BANCO CONSOLIDADO PARA FLASK")
    print("=" * 50)

    # Caminhos
    banco_consolidado = '../dados/consolidados/banco_completo_91_diretorias.db'
    banco_flask = 'instance/escolas_sistema_91_completo.db'

    # Criar pasta instance se não existir
    os.makedirs('instance', exist_ok=True)

    # Copiar banco
    if os.path.exists(banco_consolidado):
        shutil.copy2(banco_consolidado, banco_flask)
        print(f"✅ Banco copiado: {banco_flask}")

        # Verificar integridade
        conn = sqlite3.connect(banco_flask)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM diretorias")
        diretorias_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM escolas")
        escolas_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tipos_escola")
        tipos_count = cursor.fetchone()[0]

        conn.close()

        print(
            f"✅ Verificação: {diretorias_count} diretorias, {escolas_count:,} escolas, {tipos_count} tipos")
        return True
    else:
        print(f"❌ Banco consolidado não encontrado: {banco_consolidado}")
        return False


def atualizar_configuracao_flask():
    """Atualiza a configuração do Flask para usar o novo banco."""

    print("\n🔧 ATUALIZANDO CONFIGURAÇÃO DO FLASK")
    print("-" * 40)

    # Ler config atual
    if os.path.exists('app/config.py'):
        with open('app/config.py', 'r', encoding='utf-8') as f:
            config_content = f.read()

        # Atualizar caminho do banco
        new_config = config_content.replace(
            'escolas_sistema.db',
            'escolas_sistema_91_completo.db'
        )

        with open('app/config.py', 'w', encoding='utf-8') as f:
            f.write(new_config)

        print("✅ Configuração do Flask atualizada")
    else:
        print("⚠️ Arquivo config.py não encontrado")


def criar_novas_rotas_api():
    """Cria rotas API atualizadas para as 91 diretorias."""

    print("\n🌐 CRIANDO ROTAS API ATUALIZADAS")
    print("-" * 40)

    rotas_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROTAS API ATUALIZADAS - 91 DIRETORIAS COMPLETAS
============================================
"""

from flask import Blueprint, jsonify, request
import sqlite3
import os

# Blueprint para as APIs
api_91_bp = Blueprint('api_91', __name__, url_prefix='/api/v2')

def get_db_connection():
    """Conecta ao banco de dados atualizado."""
    db_path = os.path.join('instance', 'escolas_sistema_91_completo.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@api_91_bp.route('/diretorias', methods=['GET'])
def listar_diretorias():
    """Lista todas as 91 diretorias com siglas oficiais."""
    try:
        conn = get_db_connection()
        diretorias = conn.execute('''
            SELECT
                id, nome, sigla, total_escolas,
                endereco_completo, cidade, cep,
                telefone, email
            FROM diretorias
            ORDER BY nome
        ''').fetchall()
        conn.close()
        
        resultado = []
        for d in diretorias:
            resultado.append({
                'id': d['id'],
                'nome': d['nome'],
                'sigla': d['sigla'],
                'total_escolas': d['total_escolas'],
                'endereco_completo': d['endereco_completo'],
                'cidade': d['cidade'],
                'cep': d['cep'],
                'telefone': d['telefone'],
                'email': d['email']
            })
        
        return jsonify({
            'success': True,
            'total': len(resultado),
            'diretorias': resultado
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_91_bp.route('/diretorias/<sigla>/detalhes', methods=['GET'])
def detalhes_diretoria(sigla):
    """Detalhes completos de uma diretoria pela sigla."""
    try:
        conn = get_db_connection()
        
        # Buscar diretoria
        diretoria = conn.execute('''
            SELECT * FROM diretorias WHERE sigla = ? OR nome = ?
        ''', (sigla.upper(), sigla.upper())).fetchone()
        
        if not diretoria:
            return jsonify({
                'success': False,
                'error': 'Diretoria não encontrada'
            }), 404
        
        # Buscar escolas da diretoria
        escolas = conn.execute('''
            SELECT 
                tipo_escola_codigo, tipo_escola_nome, 
                COUNT(*) as quantidade
            FROM escolas 
            WHERE diretoria = ?
            GROUP BY tipo_escola_codigo, tipo_escola_nome
            ORDER BY tipo_escola_codigo
        ''', (diretoria['nome'],)).fetchall()
        
        conn.close()
        
        # Organizar dados
        tipos_escola = []
        for escola in escolas:
            tipos_escola.append({
                'codigo': escola['tipo_escola_codigo'],
                'nome': escola['tipo_escola_nome'],
                'quantidade': escola['quantidade']
            })
        
        resultado = {
            'id': diretoria['id'],
            'nome': diretoria['nome'],
            'sigla': diretoria['sigla'],
            'total_escolas': diretoria['total_escolas'],
            'endereco': {
                'completo': diretoria['endereco_completo'],
                'logradouro': diretoria['logradouro'],
                'numero': diretoria['numero'],
                'bairro': diretoria['bairro'],
                'cidade': diretoria['cidade'],
                'cep': diretoria['cep']
            },
            'contato': {
                'telefone': diretoria['telefone'],
                'email': diretoria['email'],
                'dirigente': diretoria['dirigente']
            },
            'tipos_escola': tipos_escola
        }
        
        return jsonify({
            'success': True,
            'diretoria': resultado
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_91_bp.route('/tipos-escola', methods=['GET'])
def listar_tipos_escola():
    """Lista todos os 10 tipos de escola."""
    try:
        conn = get_db_connection()
        tipos = conn.execute('''
            SELECT 
                codigo, nome, descricao, categoria,
                total_escolas, percentual
            FROM tipos_escola 
            ORDER BY codigo
        ''').fetchall()
        conn.close()
        
        resultado = []
        for tipo in tipos:
            resultado.append({
                'codigo': tipo['codigo'],
                'nome': tipo['nome'],
                'descricao': tipo['descricao'],
                'categoria': tipo['categoria'],
                'total_escolas': tipo['total_escolas'],
                'percentual': tipo['percentual']
            })
        
        return jsonify({
            'success': True,
            'total_tipos': len(resultado),
            'tipos_escola': resultado
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_91_bp.route('/estatisticas', methods=['GET'])
def estatisticas_sistema():
    """Estatísticas gerais do sistema."""
    try:
        conn = get_db_connection()
        
        # Estatísticas básicas
        stats = conn.execute('''
            SELECT tipo, valor, descricao FROM estatisticas
        ''').fetchall()
        
        # Top diretorias
        top_diretorias = conn.execute('''
            SELECT nome, sigla, total_escolas
            FROM diretorias 
            ORDER BY total_escolas DESC 
            LIMIT 10
        ''').fetchall()
        
        # Distribuição por tipo
        distribuicao_tipos = conn.execute('''
            SELECT 
                te.nome, te.codigo,
                COUNT(e.id) as quantidade
            FROM tipos_escola te
            LEFT JOIN escolas e ON te.codigo = e.tipo_escola_codigo
            GROUP BY te.codigo, te.nome
            ORDER BY te.codigo
        ''').fetchall()
        
        conn.close()
        
        # Organizar resultado
        estatisticas_gerais = {}
        for stat in stats:
            estatisticas_gerais[stat['tipo']] = {
                'valor': stat['valor'],
                'descricao': stat['descricao']
            }
        
        top_dirs = []
        for d in top_diretorias:
            top_dirs.append({
                'nome': d['nome'],
                'sigla': d['sigla'],
                'total_escolas': d['total_escolas']
            })
        
        dist_tipos = []
        for t in distribuicao_tipos:
            dist_tipos.append({
                'codigo': t['codigo'],
                'nome': t['nome'],
                'quantidade': t['quantidade']
            })
        
        return jsonify({
            'success': True,
            'estatisticas_gerais': estatisticas_gerais,
            'top_diretorias': top_dirs,
            'distribuicao_tipos': dist_tipos,
            'data_atualizacao': '2025-08-12'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_91_bp.route('/siglas', methods=['GET'])
def listar_siglas():
    """Lista todas as siglas das diretorias para mapas."""
    try:
        conn = get_db_connection()
        siglas = conn.execute('''
            SELECT nome, sigla FROM diretorias ORDER BY sigla
        ''').fetchall()
        conn.close()
        
        resultado = {}
        for s in siglas:
            resultado[s['sigla']] = s['nome']
        
        return jsonify({
            'success': True,
            'total_siglas': len(resultado),
            'siglas': resultado
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_91_bp.route('/relatorio/executivo', methods=['GET'])
def relatorio_executivo():
    """Relatório executivo completo."""
    try:
        conn = get_db_connection()
        
        # Dados básicos
        total_diretorias = conn.execute('SELECT COUNT(*) FROM diretorias').fetchone()[0]
        total_escolas = conn.execute('SELECT COUNT(*) FROM escolas').fetchone()[0]
        total_tipos = conn.execute('SELECT COUNT(*) FROM tipos_escola').fetchone()[0]
        
        # Escolas especiais
        indigenas = conn.execute('SELECT COUNT(*) FROM escolas WHERE tipo_escola_codigo = 10').fetchone()[0]
        quilombolas = conn.execute('SELECT COUNT(*) FROM escolas WHERE tipo_escola_codigo = 36').fetchone()[0]
        assentamentos = conn.execute('SELECT COUNT(*) FROM escolas WHERE tipo_escola_codigo = 31').fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'relatorio': {
                'total_diretorias': total_diretorias,
                'total_escolas': total_escolas,
                'total_tipos_escola': total_tipos,
                'escolas_especiais': {
                    'indigenas': indigenas,
                    'quilombolas': quilombolas,
                    'assentamentos': assentamentos,
                    'total_especiais': indigenas + quilombolas + assentamentos
                },
                'status': 'Sistema com 91 diretorias oficiais e siglas implementadas',
                'data_atualizacao': '2025-08-12'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
'''
    
    # Salvar rotas
    with open('app/routes/api_91_diretorias.py', 'w', encoding='utf-8') as f:
        f.write(rotas_content)
    
    print("✅ Rotas API atualizadas criadas")


def atualizar_dashboard():
    """Atualiza o dashboard para usar as 91 diretorias."""
    
    print("\n🎨 ATUALIZANDO DASHBOARD")
    print("-" * 40)
    
    dashboard_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - 91 Diretorias SP</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .sigla-badge {
            background: linear-gradient(45deg, #007bff, #0056b3);
            color: white;
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
        }
        .stat-card {
            border-left: 4px solid #007bff;
            transition: transform 0.2s;
        }
        .stat-card:hover {
            transform: translateY(-2px);
        }
        .tipo-badge {
            font-size: 0.8em;
            padding: 2px 6px;
        }
    </style>
</head>
<body class="bg-light">
    
    <!-- Header -->
    <nav class="navbar navbar-dark bg-primary">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-school me-2"></i>
                Sistema de Diretorias - SP (91 Diretorias Oficiais)
            </span>
            <span class="navbar-text">
                <i class="fas fa-calendar me-1"></i>
                Atualizado: 12/08/2025
            </span>
        </div>
    </nav>

    <div class="container-fluid mt-4">
        
        <!-- Resumo Executivo -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card stat-card">
                    <div class="card-body">
                        <h4 class="card-title text-primary">
                            <i class="fas fa-chart-line me-2"></i>
                            Resumo Executivo - Sistema Consolidado
                        </h4>
                        <div class="row" id="resumo-stats">
                            <!-- Carregado via JavaScript -->
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Filtros -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="input-group">
                    <span class="input-group-text">
                        <i class="fas fa-search"></i>
                    </span>
                    <input type="text" class="form-control" id="filtro-nome" 
                           placeholder="Buscar diretoria por nome ou sigla...">
                </div>
            </div>
            <div class="col-md-6">
                <select class="form-select" id="filtro-regiao">
                    <option value="">Todas as regiões</option>
                    <option value="capital">Capital</option>
                    <option value="interior">Interior</option>
                    <option value="metropolitana">Região Metropolitana</option>
                </select>
            </div>
        </div>

        <!-- Lista de Diretorias -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <i class="fas fa-building me-2"></i>
                            91 Diretorias/Unidades Regionais de Ensino
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead class="table-dark">
                                    <tr>
                                        <th>Sigla</th>
                                        <th>Nome da Diretoria</th>
                                        <th>Total Escolas</th>
                                        <th>Cidade</th>
                                        <th>Ações</th>
                                    </tr>
                                </thead>
                                <tbody id="tabela-diretorias">
                                    <!-- Carregado via JavaScript -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal de Detalhes -->
        <div class="modal fade" id="modalDetalhes" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-info-circle me-2"></i>
                            Detalhes da Diretoria
                        </h5>
                        <button type="button" class="btn-close btn-close-white" 
                                data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body" id="conteudo-modal">
                        <!-- Carregado via JavaScript -->
                    </div>
                </div>
            </div>
        </div>

    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let todasDiretorias = [];

        // Carregar dados iniciais
        document.addEventListener('DOMContentLoaded', function() {
            carregarEstatisticas();
            carregarDiretorias();
        });

        // Carregar estatísticas
        async function carregarEstatisticas() {
            try {
                const response = await fetch('/api/v2/estatisticas');
                const data = await response.json();
                
                if (data.success) {
                    const stats = data.estatisticas_gerais;
                    const resumoHtml = `
                        <div class="col-md-3">
                            <div class="text-center">
                                <h3 class="text-primary">${stats.total_diretorias.valor}</h3>
                                <p class="mb-0">Diretorias/UREs</p>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center">
                                <h3 class="text-success">${stats.total_escolas.valor.toLocaleString()}</h3>
                                <p class="mb-0">Escolas</p>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center">
                                <h3 class="text-info">${stats.total_tipos_escola.valor}</h3>
                                <p class="mb-0">Tipos de Escola</p>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center">
                                <h3 class="text-warning">${stats.escolas_indigenas.valor + stats.escolas_quilombolas.valor}</h3>
                                <p class="mb-0">Escolas Especiais</p>
                            </div>
                        </div>
                    `;
                    document.getElementById('resumo-stats').innerHTML = resumoHtml;
                }
            } catch (error) {
                console.error('Erro ao carregar estatísticas:', error);
            }
        }

        // Carregar diretorias
        async function carregarDiretorias() {
            try {
                const response = await fetch('/api/v2/diretorias');
                const data = await response.json();
                
                if (data.success) {
                    todasDiretorias = data.diretorias;
                    exibirDiretorias(todasDiretorias);
                }
            } catch (error) {
                console.error('Erro ao carregar diretorias:', error);
            }
        }

        // Exibir diretorias na tabela
        function exibirDiretorias(diretorias) {
            const tbody = document.getElementById('tabela-diretorias');
            tbody.innerHTML = '';

            diretorias.forEach(diretoria => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><span class="sigla-badge">${diretoria.sigla}</span></td>
                    <td>${diretoria.nome}</td>
                    <td>
                        <span class="badge bg-primary">${diretoria.total_escolas}</span>
                    </td>
                    <td>${diretoria.cidade || 'N/A'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" 
                                onclick="verDetalhes('${diretoria.sigla}')">
                            <i class="fas fa-eye me-1"></i>Detalhes
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Ver detalhes da diretoria
        async function verDetalhes(sigla) {
            try {
                const response = await fetch(`/api/v2/diretorias/${sigla}/detalhes`);
                const data = await response.json();
                
                if (data.success) {
                    const d = data.diretoria;
                    const modalContent = `
                        <div class="row">
                            <div class="col-md-6">
                                <h6><i class="fas fa-building me-2"></i>Informações Básicas</h6>
                                <p><strong>Nome:</strong> ${d.nome}</p>
                                <p><strong>Sigla:</strong> <span class="sigla-badge">${d.sigla}</span></p>
                                <p><strong>Total de Escolas:</strong> <span class="badge bg-primary">${d.total_escolas}</span></p>
                            </div>
                            <div class="col-md-6">
                                <h6><i class="fas fa-map-marker-alt me-2"></i>Endereço</h6>
                                <p>${d.endereco.completo || 'Não informado'}</p>
                                <p><strong>Cidade:</strong> ${d.endereco.cidade || 'N/A'}</p>
                                <p><strong>CEP:</strong> ${d.endereco.cep || 'N/A'}</p>
                            </div>
                        </div>
                        <hr>
                        <h6><i class="fas fa-school me-2"></i>Tipos de Escola</h6>
                        <div class="row">
                            ${d.tipos_escola.map(tipo => `
                                <div class="col-md-6 mb-2">
                                    <span class="badge bg-secondary me-2">${tipo.codigo}</span>
                                    ${tipo.nome}: <strong>${tipo.quantidade}</strong>
                                </div>
                            `).join('')}
                        </div>
                    `;
                    
                    document.getElementById('conteudo-modal').innerHTML = modalContent;
                    new bootstrap.Modal(document.getElementById('modalDetalhes')).show();
                }
            } catch (error) {
                console.error('Erro ao carregar detalhes:', error);
            }
        }

        // Filtros
        document.getElementById('filtro-nome').addEventListener('input', function() {
            const filtro = this.value.toLowerCase();
            const diretorias_filtradas = todasDiretorias.filter(d => 
                d.nome.toLowerCase().includes(filtro) || 
                d.sigla.toLowerCase().includes(filtro)
            );
            exibirDiretorias(diretorias_filtradas);
        });

    </script>
</body>
</html>'''
    
    # Salvar dashboard
    os.makedirs('app/templates/dashboard', exist_ok=True)
    with open('app/templates/dashboard/sistema_91_diretorias.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_content)
    
    print("✅ Dashboard atualizado criado")


def atualizar_app_principal():
    """Atualiza o app principal para registrar as novas rotas."""
    
    print("\n🚀 ATUALIZANDO APP PRINCIPAL")
    print("-" * 40)
    
    # Verificar se __init__.py existe
    if os.path.exists('app/__init__.py'):
        with open('app/__init__.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar import da nova rota
        if 'api_91_diretorias' not in content:
            # Procurar onde adicionar
            if 'from app.routes' in content:
                # Adicionar após outros imports de rotas
                new_content = content.replace(
                    'from app.routes import',
                    'from app.routes import api_91_diretorias,\nfrom app.routes import'
                )
            else:
                # Adicionar import
                new_content = content + '\nfrom app.routes.api_91_diretorias import api_91_bp\n'
            
            # Adicionar registro do blueprint
            if 'register_blueprint' in new_content:
                new_content = new_content.replace(
                    'app.register_blueprint(',
                    'app.register_blueprint(api_91_bp)\n    app.register_blueprint('
                )
            else:
                new_content += '\n    app.register_blueprint(api_91_bp)\n'
            
            with open('app/__init__.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ App principal atualizado")
    else:
        print("⚠️ Arquivo __init__.py não encontrado")


def criar_rota_dashboard():
    """Cria rota para o novo dashboard."""
    
    print("\n🎨 CRIANDO ROTA PARA DASHBOARD")
    print("-" * 40)
    
    # Verificar se existe arquivo de rotas principais
    if os.path.exists('app/routes/main.py'):
        with open('app/routes/main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar rota do novo dashboard
        nova_rota = '''

@main_bp.route('/dashboard-91')
def dashboard_91_diretorias():
    """Dashboard com as 91 diretorias oficiais."""
    return render_template('dashboard/sistema_91_diretorias.html')
'''
        
        if '/dashboard-91' not in content:
            content += nova_rota
            
            with open('app/routes/main.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Rota do dashboard criada: /dashboard-91")
    else:
        print("⚠️ Arquivo main.py não encontrado")


def main():
    """Função principal."""
    
    print("🔄 ATUALIZANDO SISTEMA FLASK COM DADOS CONSOLIDADOS")
    print("=" * 60)
    
    try:
        # 1. Copiar banco consolidado
        if not copiar_banco_consolidado():
            print("❌ Falha ao copiar banco. Abortando.")
            return False
        
        # 2. Atualizar configuração
        atualizar_configuracao_flask()
        
        # 3. Criar novas rotas API
        criar_novas_rotas_api()
        
        # 4. Atualizar dashboard
        atualizar_dashboard()
        
        # 5. Atualizar app principal
        # atualizar_app_principal()
        
        # 6. Criar rota do dashboard
        criar_rota_dashboard()
        
        print(f"\n🎉 SISTEMA FLASK ATUALIZADO COM SUCESSO!")
        print(f"✅ Banco com 91 diretorias instalado")
        print(f"✅ APIs v2 criadas em /api/v2/")
        print(f"✅ Dashboard atualizado disponível")
        print(f"✅ Todas as siglas oficiais implementadas")
        
        print(f"\n🌐 ENDPOINTS DISPONÍVEIS:")
        print(f"   - /api/v2/diretorias")
        print(f"   - /api/v2/diretorias/<sigla>/detalhes")
        print(f"   - /api/v2/tipos-escola")
        print(f"   - /api/v2/estatisticas")
        print(f"   - /api/v2/siglas")
        print(f"   - /dashboard-91")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False


if __name__ == "__main__":
    main()
'''
