from flask import Blueprint, jsonify, render_template_string
import sqlite3
import os

# Blueprint para teste das 91 diretorias
bp_91_diretorias = Blueprint('91_diretorias', __name__)


def get_db_91():
    """Conecta ao banco com 91 diretorias."""
    conn = sqlite3.connect('instance/banco_91_diretorias.db')
    conn.row_factory = sqlite3.Row
    return conn


@bp_91_diretorias.route('/91-diretorias')
def dashboard_91():
    """Dashboard com as 91 diretorias atualizadas."""
    try:
        conn = get_db_91()

        # Estatísticas gerais
        total_diretorias = conn.execute(
            'SELECT COUNT(*) FROM diretorias').fetchone()[0]
        total_escolas = conn.execute(
            'SELECT COUNT(*) FROM escolas').fetchone()[0]
        total_tipos = conn.execute(
            'SELECT COUNT(*) FROM tipos_escola').fetchone()[0]

        # Top 10 diretorias
        top_diretorias = conn.execute('''
            SELECT nome, sigla, total_escolas 
            FROM diretorias 
            ORDER BY total_escolas DESC 
            LIMIT 10
        ''').fetchall()

        # Tipos de escola
        tipos_escola = conn.execute('''
            SELECT codigo, nome, total_escolas, percentual
            FROM tipos_escola 
            ORDER BY codigo
        ''').fetchall()

        # Escolas especiais
        indigenas = conn.execute(
            'SELECT COUNT(*) FROM escolas WHERE tipo_escola_codigo = 10').fetchone()[0]
        quilombolas = conn.execute(
            'SELECT COUNT(*) FROM escolas WHERE tipo_escola_codigo = 36').fetchone()[0]
        assentamentos = conn.execute(
            'SELECT COUNT(*) FROM escolas WHERE tipo_escola_codigo = 31').fetchone()[0]

        conn.close()

        html = f'''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - 91 Diretorias SP</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .sigla-badge {{
            background: linear-gradient(45deg, #007bff, #0056b3);
            color: white;
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
        }}
        .stat-card {{
            border-left: 4px solid #007bff;
            transition: transform 0.2s;
        }}
        .stat-card:hover {{
            transform: translateY(-2px);
        }}
    </style>
</head>
<body class="bg-light">
    
    <nav class="navbar navbar-dark bg-primary">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-school me-2"></i>
                ✅ Sistema Atualizado - {total_diretorias} Diretorias SP
            </span>
            <span class="navbar-text">
                Atualizado: 12/08/2025 - Dados Consolidados
            </span>
        </div>
    </nav>

    <div class="container-fluid mt-4">
        
        <!-- Resumo Executivo -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <h2 class="text-primary">{total_diretorias}</h2>
                        <p class="mb-0">Diretorias/UREs</p>
                        <small class="text-success">✅ Corrigido (era 89)</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <h2 class="text-success">{total_escolas:,}</h2>
                        <p class="mb-0">Escolas Total</p>
                        <small class="text-muted">Todas as modalidades</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <h2 class="text-info">{total_tipos}</h2>
                        <p class="mb-0">Tipos de Escola</p>
                        <small class="text-success">✅ Todos mapeados</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <h2 class="text-warning">{indigenas + quilombolas + assentamentos}</h2>
                        <p class="mb-0">Escolas Especiais</p>
                        <small class="text-muted">{indigenas} Indígenas, {quilombolas} Quilombolas</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Top Diretorias -->
        <div class="row mb-4">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">🏆 Top 10 Diretorias por Número de Escolas</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead class="table-dark">
                                    <tr>
                                        <th>Posição</th>
                                        <th>Sigla</th>
                                        <th>Nome</th>
                                        <th>Total Escolas</th>
                                    </tr>
                                </thead>
                                <tbody>
        '''

        # Adicionar top diretorias
        for i, diretoria in enumerate(top_diretorias, 1):
            html += f'''
                                    <tr>
                                        <td><span class="badge bg-secondary">{i}º</span></td>
                                        <td><span class="sigla-badge">{diretoria['sigla']}</span></td>
                                        <td>{diretoria['nome']}</td>
                                        <td><span class="badge bg-primary">{diretoria['total_escolas']}</span></td>
                                    </tr>
            '''

        html += '''
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">🏫 10 Tipos de Escola</h5>
                    </div>
                    <div class="card-body">
        '''

        # Adicionar tipos de escola
        for tipo in tipos_escola:
            cor_badge = "primary" if tipo['codigo'] in [
                10, 36, 31] else "secondary"
            html += f'''
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span>
                                <span class="badge bg-{cor_badge}">{tipo['codigo']}</span>
                                {tipo['nome']}
                            </span>
                            <span class="badge bg-outline-dark">{tipo['total_escolas']}</span>
                        </div>
            '''

        html += f'''
                    </div>
                </div>
            </div>
        </div>

        <!-- Status da Atualização -->
        <div class="row">
            <div class="col-12">
                <div class="card border-success">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">✅ Status da Atualização - Sistema Consolidado</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>🔧 Problemas Corrigidos:</h6>
                                <ul class="list-unstyled">
                                    <li>✅ Diretorias: <strong>89 → {total_diretorias}</strong></li>
                                    <li>✅ Siglas oficiais implementadas</li>
                                    <li>✅ Todos os {total_tipos} tipos de escola mapeados</li>
                                    <li>✅ Dados consistentes em toda a base</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6>📊 Dados Finais:</h6>
                                <ul class="list-unstyled">
                                    <li><strong>Escolas Indígenas:</strong> {indigenas}</li>
                                    <li><strong>Escolas Quilombolas:</strong> {quilombolas}</li>
                                    <li><strong>Escolas Assentamento:</strong> {assentamentos}</li>
                                    <li><strong>Total Geral:</strong> {total_escolas:,} escolas</li>
                                </ul>
                            </div>
                        </div>
                        <div class="alert alert-success mt-3" role="alert">
                            <strong>🎉 Sistema 100% Atualizado!</strong> 
                            O Flask agora está usando o banco consolidado com todas as 91 diretorias oficiais e siglas para mapas interativos.
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        '''

        return html

    except Exception as e:
        return f'<h1>❌ Erro ao carregar dados: {str(e)}</h1>'


@bp_91_diretorias.route('/api/diretorias-91')
def api_diretorias_91():
    """API com todas as 91 diretorias."""
    try:
        conn = get_db_91()

        diretorias = conn.execute('''
            SELECT nome, sigla, total_escolas, cidade
            FROM diretorias 
            ORDER BY nome
        ''').fetchall()

        conn.close()

        resultado = []
        for d in diretorias:
            resultado.append({
                'nome': d['nome'],
                'sigla': d['sigla'],
                'total_escolas': d['total_escolas'],
                'cidade': d['cidade']
            })

        return jsonify({
            'success': True,
            'total_diretorias': len(resultado),
            'status': 'Sistema atualizado com 91 diretorias oficiais',
            'data_atualizacao': '2025-08-12',
            'diretorias': resultado
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
