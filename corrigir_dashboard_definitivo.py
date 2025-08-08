#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd
import re


def atualizar_dashboard_com_dados_corretos():
    """Atualiza o dashboard com os dados corretos das escolas e veículos"""

    print("🔄 Carregando dados corretos...")

    # Carregar dados das escolas atualizados
    with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        escolas = json.load(f)

    # Carregar dados dos veículos corretos
    df_veiculos = pd.read_excel(
        'QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx')

    print(f"📚 Escolas carregadas: {len(escolas)}")
    print(f"🚗 Dados de veículos carregados: {len(df_veiculos)} diretorias")

    # Processar dados dos veículos
    vehicleData = {}
    total_veiculos = 0

    for _, row in df_veiculos.iterrows():
        diretoria = str(row['DIRETORIA']).upper().strip()
        s1 = int(row.get('QUANTIDADE S-1', 0) or 0)
        s2 = int(row.get('QUANTIDADE S-2', 0) or 0)
        s2_4x4 = int(row.get('QUANTIDADE S-2 4X4 ', 0) or 0)
        total = s1 + s2 + s2_4x4
        total_veiculos += total

        vehicleData[diretoria] = {
            "total": total,
            "s1": s1,
            "s2": s2,
            "s2_4x4": s2_4x4
        }

    print(f"🚗 Total de veículos calculado: {total_veiculos}")

    # Criar mapeamento de normalizacao
    def normalizar_nome_diretoria(nome):
        """Normaliza o nome da diretoria para comparação"""
        if not nome:
            return ""

        import unicodedata
        nome = unicodedata.normalize('NFKD', str(nome).upper())
        nome = ''.join([c for c in nome if not unicodedata.combining(c)])
        nome = re.sub(r'[^\w\s]', '', nome)
        nome = re.sub(r'\s+', ' ', nome).strip()

        return nome

    # Função para mapear nomes de diretorias
    def mapear_diretoria(nome_escola):
        """Mapeia nome da diretoria da escola para o nome usado nos veículos"""
        mapeamento = {
            'SAO VICENTE': 'SAO VICENTE',
            'SÃO VICENTE': 'SAO VICENTE',
            'LESTE 5': 'LESTE 5',
            'SUL 3': 'SUL 3',
            'NORTE 1': 'NORTE 1'
        }

        nome_normalizado = normalizar_nome_diretoria(nome_escola)
        return mapeamento.get(nome_normalizado, nome_normalizado)

    # Calcular estatísticas
    escolas_50km = len([e for e in escolas if e['distance'] > 50])
    distancia_media = round(sum(e['distance']
                            for e in escolas) / len(escolas), 1)
    diretorias_unicas = len(set(e['diretoria'] for e in escolas))

    print(f"📊 Estatísticas calculadas:")
    print(f"  • Escolas >50km: {escolas_50km}")
    print(f"  • Distância média: {distancia_media} km")
    print(f"  • Diretorias únicas: {diretorias_unicas}")

    # Ler arquivo HTML
    with open('dashboard_integrado.html', 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Atualizar estatísticas
    conteudo = re.sub(
        r'<div class="stat-number" id="total-vehicles">\d+</div>',
        f'<div class="stat-number" id="total-vehicles">{total_veiculos}</div>',
        conteudo
    )

    conteudo = re.sub(
        r'<div class="stat-number" id="total-diretorias">\d+</div>',
        f'<div class="stat-number" id="total-diretorias">{diretorias_unicas}</div>',
        conteudo
    )

    conteudo = re.sub(
        r'<div class="stat-number" id="avg-distance">[\d.]+</div>',
        f'<div class="stat-number" id="avg-distance">{distancia_media}</div>',
        conteudo
    )

    conteudo = re.sub(
        r'<div class="stat-number" id="high-priority">\d+</div>',
        f'<div class="stat-number" id="high-priority">{escolas_50km}</div>',
        conteudo
    )

    # Atualizar dados dos veículos no JavaScript
    vehicle_data_js = "const vehicleData = {\n"
    for diretoria, dados in vehicleData.items():
        vehicle_data_js += f'      "{diretoria}": {{ "total": {dados["total"]}, "s1": {dados["s1"]}, "s2": {dados["s2"]}, "s2_4x4": {dados["s2_4x4"]} }},\n'
    vehicle_data_js += "    };"

    # Substituir dados dos veículos
    pattern = r'const vehicleData = \{[^}]+\};'
    conteudo = re.sub(pattern, vehicle_data_js, conteudo, flags=re.DOTALL)

    # Atualizar dados das escolas no JavaScript
    schools_data_js = "const schoolsData = " + \
        json.dumps(escolas, ensure_ascii=False, indent=6) + ";"

    # Substituir dados das escolas
    pattern = r'const schoolsData = \[.*?\];'
    conteudo = re.sub(pattern, schools_data_js, conteudo, flags=re.DOTALL)

    # Adicionar função de normalização se não existir
    if 'function normalizeDiretoriaName' not in conteudo:
        normalization_function = '''
    // Função para normalizar nomes de diretorias
    function normalizeDiretoriaName(name) {
      if (!name) return "";
      
      // Remover acentos e converter para maiúsculo
      let normalized = name.normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").toUpperCase();
      
      // Remover caracteres especiais e espaços extras
      normalized = normalized.replace(/[^\\w\\s]/g, '').replace(/\\s+/g, ' ').trim();
      
      return normalized;
    }
'''
        # Inserir antes dos dados das escolas
        conteudo = conteudo.replace(
            '// Dados das escolas', normalization_function + '\n    // Dados das escolas')

    # Corrigir função calculatePriority para usar normalização
    if 'const vehicles = vehicleData[school.diretoria.toUpperCase()]' in conteudo:
        conteudo = conteudo.replace(
            'const vehicles = vehicleData[school.diretoria.toUpperCase()]',
            'const vehicles = vehicleData[normalizeDiretoriaName(school.diretoria)]'
        )

    # Salvar arquivo atualizado
    with open('dashboard_integrado.html', 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print("✅ Dashboard atualizado com dados corretos!")
    print(f"📚 Total de escolas: {len(escolas)}")
    print(f"🚗 Total de veículos: {total_veiculos}")
    print(f"🏢 Total de diretorias: {diretorias_unicas}")


def main():
    atualizar_dashboard_com_dados_corretos()


if __name__ == "__main__":
    main()
