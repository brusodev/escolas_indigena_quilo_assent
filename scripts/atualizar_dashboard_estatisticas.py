#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd
import re
from collections import defaultdict


def carregar_dados():
    """Carrega dados das escolas e veículos"""

    # Carregar dados das escolas
    with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        escolas = json.load(f)

    # Carregar dados dos veículos
    df_veiculos = pd.read_excel(
        'QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx')

    print("📋 Colunas encontradas:", list(df_veiculos.columns))

    vehicleData = {}
    for _, row in df_veiculos.iterrows():
        diretoria = str(row['DIRETORIA']).upper().strip()

        # Usar os nomes corretos das colunas
        s1 = int(row.get('QUANTIDADE S-1', 0) or 0)
        s2 = int(row.get('QUANTIDADE S-2', 0) or 0)
        s2_4x4 = int(row.get('QUANTIDADE S-2 4X4 ', 0)
                     or 0)  # Note o espaço no final
        total = s1 + s2 + s2_4x4

        vehicleData[diretoria] = {
            "total": total,
            "s1": s1,
            "s2": s2,
            "s2_4x4": s2_4x4
        }

    return escolas, vehicleData


def normalizar_nome_diretoria(nome):
    """Normaliza o nome da diretoria para comparação"""
    if not nome:
        return ""

    # Converter para maiúsculo e remover acentos
    import unicodedata
    nome = unicodedata.normalize('NFKD', str(nome).upper())
    nome = ''.join([c for c in nome if not unicodedata.combining(c)])

    # Remover caracteres especiais e espaços extras
    nome = re.sub(r'[^\w\s]', '', nome)
    nome = re.sub(r'\s+', ' ', nome).strip()

    return nome


def calcular_prioridade(escola, vehicleData):
    """Calcula a prioridade de uma escola baseada na distância e disponibilidade de veículos"""
    diretoria_normalizada = normalizar_nome_diretoria(escola['diretoria'])
    veiculos = vehicleData.get(diretoria_normalizada, {"total": 0})

    distancia = escola['distance']
    total_veiculos = veiculos['total']

    # Nova lógica de priorização:
    # 1. Escolas com distância > 50km E sem veículos = ALTA prioridade
    # 2. Escolas com distância > 30km E sem veículos = MÉDIA prioridade
    # 3. Escolas com distância > 50km MAS com veículos = MÉDIA prioridade
    # 4. Resto = BAIXA prioridade

    if distancia > 50 and total_veiculos == 0:
        return 'high'
    elif distancia > 30 and total_veiculos == 0:
        return 'medium'
    elif distancia > 50:
        return 'medium'
    else:
        return 'low'


def calcular_estatisticas(escolas, vehicleData):
    """Calcula estatísticas do dashboard"""

    # Total de escolas
    total_escolas = len(escolas)

    # Total de veículos
    total_veiculos = sum(v['total'] for v in vehicleData.values())

    # Diretorias únicas (baseadas nas escolas)
    diretorias_unicas = set()
    for escola in escolas:
        diretorias_unicas.add(escola['diretoria'])
    total_diretorias = len(diretorias_unicas)

    # Distância média
    distancias = [escola['distance'] for escola in escolas]
    distancia_media = round(sum(distancias) / len(distancias), 1)

    # Escolas por tipo
    indigenas = len([e for e in escolas if e['type'] == 'indigena'])
    quilombolas = len([e for e in escolas if e['type'] == 'quilombola'])

    # Calcular prioridades
    prioridades = {'high': 0, 'medium': 0, 'low': 0}
    for escola in escolas:
        prioridade = calcular_prioridade(escola, vehicleData)
        prioridades[prioridade] += 1

    # Escolas por diretoria
    escolas_por_diretoria = defaultdict(int)
    for escola in escolas:
        escolas_por_diretoria[escola['diretoria']] += 1

    return {
        'total_escolas': total_escolas,
        'total_veiculos': total_veiculos,
        'total_diretorias': total_diretorias,
        'distancia_media': distancia_media,
        'indigenas': indigenas,
        'quilombolas': quilombolas,
        'alta_prioridade': prioridades['high'],
        'media_prioridade': prioridades['medium'],
        'baixa_prioridade': prioridades['low'],
        'escolas_por_diretoria': dict(escolas_por_diretoria)
    }


def atualizar_dashboard_html(stats, vehicleData):
    """Atualiza o dashboard HTML com as estatísticas corretas"""

    # Ler o arquivo HTML
    with open('dashboard_integrado.html', 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Atualizar estatísticas nos cards
    conteudo = re.sub(
        r'<div class="stat-number" id="total-schools">\d+</div>',
        f'<div class="stat-number" id="total-schools">{stats["total_escolas"]}</div>',
        conteudo
    )

    conteudo = re.sub(
        r'<div class="stat-number" id="total-vehicles">\d+</div>',
        f'<div class="stat-number" id="total-vehicles">{stats["total_veiculos"]}</div>',
        conteudo
    )

    conteudo = re.sub(
        r'<div class="stat-number" id="total-diretorias">\d+</div>',
        f'<div class="stat-number" id="total-diretorias">{stats["total_diretorias"]}</div>',
        conteudo
    )

    conteudo = re.sub(
        r'<div class="stat-number" id="avg-distance">[\d.]+</div>',
        f'<div class="stat-number" id="avg-distance">{stats["distancia_media"]}</div>',
        conteudo
    )

    conteudo = re.sub(
        r'<div class="stat-number" id="high-priority">\d+</div>',
        f'<div class="stat-number" id="high-priority">{stats["alta_prioridade"]}</div>',
        conteudo
    )

    # Atualizar legenda
    conteudo = re.sub(
        r'<span>Escola Indígena \(\d+ escolas\)</span>',
        f'<span>Escola Indígena ({stats["indigenas"]} escolas)</span>',
        conteudo
    )

    conteudo = re.sub(
        r'<span>Escola Quilombola/Assentamento \(\d+ escolas\)</span>',
        f'<span>Escola Quilombola/Assentamento ({stats["quilombolas"]} escolas)</span>',
        conteudo
    )

    # Atualizar dados dos veículos no JavaScript
    vehicle_data_js = "const vehicleData = {\n"
    for diretoria, dados in vehicleData.items():
        vehicle_data_js += f'      "{diretoria}": {{ "total": {dados["total"]}, "s1": {dados["s1"]}, "s2": {dados["s2"]}, "s2_4x4": {dados["s2_4x4"]} }},\n'
    vehicle_data_js += "    };"

    # Encontrar e substituir o objeto vehicleData
    pattern = r'const vehicleData = \{[^}]+\};'
    conteudo = re.sub(pattern, vehicle_data_js, conteudo, flags=re.DOTALL)

    # Adicionar novo gráfico de escolas por diretoria
    novo_grafico_html = '''
      <div class="chart-panel">
        <h3>🏫 Escolas por Diretoria</h3>
        <div class="chart-container">
          <canvas id="schoolsByDiretoriaChart"></canvas>
        </div>
      </div>'''

    # Substituir a seção de gráficos para ter 3 gráficos
    charts_section = '''    <!-- Gráficos de Análise -->
    <div class="charts-container" style="grid-template-columns: 1fr 1fr 1fr;">
      <div class="chart-panel">
        <h3>📊 Veículos vs Demanda por Diretoria</h3>
        <div class="chart-container">
          <canvas id="vehicleChart"></canvas>
        </div>
      </div>
      <div class="chart-panel">
        <h3>🎯 Prioridade de Atendimento</h3>
        <div class="chart-container">
          <canvas id="priorityChart"></canvas>
        </div>
      </div>
      <div class="chart-panel">
        <h3>🏫 Escolas por Diretoria</h3>
        <div class="chart-container">
          <canvas id="schoolsByDiretoriaChart"></canvas>
        </div>
      </div>
    </div>'''

    conteudo = re.sub(
        r'    <!-- Gráficos de Análise -->.*?</div>',
        charts_section,
        conteudo,
        flags=re.DOTALL
    )

    # Adicionar dados das escolas por diretoria no JavaScript
    escolas_por_diretoria_js = f"""
    // Dados das escolas por diretoria
    const escolasPorDiretoria = {json.dumps(stats['escolas_por_diretoria'], ensure_ascii=False, indent=6)};"""

    # Inserir após a declaração de vehicleData
    conteudo = conteudo.replace(
        '    };',
        f'    }};{escolas_por_diretoria_js}',
        1
    )

    # Adicionar função para criar o novo gráfico
    novo_grafico_js = '''
      // Gráfico de escolas por diretoria
      const ctx3 = document.getElementById('schoolsByDiretoriaChart').getContext('2d');
      const diretoriaLabels = Object.keys(escolasPorDiretoria).sort();
      const escolasData = diretoriaLabels.map(d => escolasPorDiretoria[d]);

      new Chart(ctx3, {
        type: 'bar',
        data: {
          labels: diretoriaLabels,
          datasets: [{
            label: 'Número de Escolas',
            data: escolasData,
            backgroundColor: 'rgba(155, 89, 182, 0.8)',
            borderColor: 'rgba(155, 89, 182, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false,
            }
          },
          scales: {
            x: {
              ticks: {
                maxRotation: 45
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      });'''

    # Adicionar o novo gráfico após o gráfico de prioridades
    conteudo = conteudo.replace(
        '      });',
        f'      }});{novo_grafico_js}',
        1
    )

    # Atualizar CSS para 3 gráficos
    conteudo = re.sub(
        r'@media \(max-width: 1200px\) \{[^}]+\.charts-container \{[^}]+\}',
        '''@media (max-width: 1200px) {
      .dashboard-grid {
        grid-template-columns: 1fr;
      }

      .charts-container {
        grid-template-columns: 1fr !important;
      }

      .stats-section {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      }''',
        conteudo,
        flags=re.DOTALL
    )

    # Salvar arquivo atualizado
    with open('dashboard_integrado.html', 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print("✅ Dashboard HTML atualizado com sucesso!")


def main():
    print("🔄 Carregando dados...")
    escolas, vehicleData = carregar_dados()

    print("📊 Calculando estatísticas...")
    stats = calcular_estatisticas(escolas, vehicleData)

    print("\n📈 ESTATÍSTICAS ATUALIZADAS:")
    print(f"📚 Total de Escolas: {stats['total_escolas']}")
    print(f"🚗 Total de Veículos: {stats['total_veiculos']}")
    print(f"🏢 Total de Diretorias: {stats['total_diretorias']}")
    print(f"📍 Distância Média: {stats['distancia_media']} km")
    print(f"🔴 Escolas Alta Prioridade: {stats['alta_prioridade']}")
    print(f"🟡 Escolas Média Prioridade: {stats['media_prioridade']}")
    print(f"🟢 Escolas Baixa Prioridade: {stats['baixa_prioridade']}")
    print(f"🏛️ Escolas Indígenas: {stats['indigenas']}")
    print(f"🏘️ Escolas Quilombolas/Assentamento: {stats['quilombolas']}")

    print("\n🏫 ESCOLAS POR DIRETORIA:")
    for diretoria, count in sorted(stats['escolas_por_diretoria'].items()):
        print(f"  • {diretoria}: {count} escolas")

    print("\n🔄 Atualizando dashboard...")
    atualizar_dashboard_html(stats, vehicleData)

    print("\n✅ Processo concluído com sucesso!")


if __name__ == "__main__":
    main()
