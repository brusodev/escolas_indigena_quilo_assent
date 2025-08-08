#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def main():
    print("=== CORRIGINDO MAPEAMENTO SÃO VICENTE ===\n")

    # 1. Verificar dados de escolas
    print("1. VERIFICANDO ESCOLAS:")
    with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        escolas_data = json.load(f)

    # Encontrar escolas de São Vicente
    escolas_sao_vicente = []
    for escola in escolas_data:
        if 'diretoria' in escola and 'VICENTE' in escola['diretoria'].upper():
            escolas_sao_vicente.append(escola)

    print(f"   Encontradas {len(escolas_sao_vicente)} escolas de São Vicente")
    print(
        f"   Diretoria referenciada: '{escolas_sao_vicente[0]['diretoria'] if escolas_sao_vicente else 'N/A'}'")

    # 2. Corrigir referências nas escolas
    print("\n2. CORRIGINDO REFERÊNCIAS NAS ESCOLAS:")
    escolas_corrigidas = 0

    for escola in escolas_data:
        if 'diretoria' in escola and escola['diretoria'].upper().replace('Ã', 'A').strip() == 'SAO VICENTE':
            escola['diretoria'] = 'SÃO VICENTE'
            escolas_corrigidas += 1

    print(f"   ✅ {escolas_corrigidas} escolas corrigidas")

    # Salvar dados de escolas corrigidos
    with open('dados_escolas_atualizados.json', 'w', encoding='utf-8') as f:
        json.dump(escolas_data, f, ensure_ascii=False, indent=2)

    # 3. Adicionar mapeamento alternativo no dashboard
    print("\n3. ADICIONANDO MAPEAMENTO ALTERNATIVO NO DASHBOARD:")

    with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Procurar por onde as escolas buscam veículos
    # Adicionar função de normalização
    normalization_function = '''
    // Função para normalizar nomes de diretorias
    function normalizeDiretoriaName(name) {
      if (!name) return '';
      
      const normalized = name.toUpperCase().trim();
      
      // Mapeamentos específicos
      const mappings = {
        'SAO VICENTE': 'SÃO VICENTE',
        'ITARARE': 'ITARARÉ',
        'REGISTRO ': 'REGISTRO',
        'SANTOS ': 'SANTOS',
        'SAO BERNARDO DO CAMPO': 'SÃO BERNARDO DO CAMPO',
        'SANTO ANASTACIO': 'SANTO ANASTÁCIO',
        'PENAPOLIS': 'PENÁPOLIS',
        'TUPA': 'TUPÃ'
      };
      
      return mappings[normalized] || normalized;
    }
    '''

    # Encontrar onde inserir a função
    script_start = html_content.find('<script>')
    if script_start != -1:
        insertion_point = html_content.find('\n', script_start) + 1

        new_html = (html_content[:insertion_point] +
                    normalization_function + '\n' +
                    html_content[insertion_point:])

        # Substituir todas as ocorrências de vehicleData[school.diretoria.toUpperCase()]
        old_pattern = 'vehicleData[school.diretoria.toUpperCase()]'
        new_pattern = 'vehicleData[normalizeDiretoriaName(school.diretoria)]'

        new_html = new_html.replace(old_pattern, new_pattern)

        # Substituir também para diretorias
        old_pattern2 = 'vehicleData[diretoria.name.toUpperCase()]'
        new_pattern2 = 'vehicleData[normalizeDiretoriaName(diretoria.name)]'

        new_html = new_html.replace(old_pattern2, new_pattern2)

        # Salvar
        with open('distancias_escolas.html', 'w', encoding='utf-8') as f:
            f.write(new_html)

        print("   ✅ Função de normalização adicionada ao dashboard")
        print("   ✅ Referências a vehicleData atualizadas para usar normalização")

    # 4. Verificação final
    print("\n4. VERIFICAÇÃO FINAL:")

    # Contar escolas corrigidas
    escolas_sao_vicente_final = [
        e for e in escolas_data if 'diretoria' in e and e['diretoria'] == 'SÃO VICENTE']
    print(f"   Escolas de 'SÃO VICENTE': {len(escolas_sao_vicente_final)}")

    # Verificar vehicleData
    with open('dados_veiculos_atualizados.json', 'r', encoding='utf-8') as f:
        vehicle_data = json.load(f)

    if 'SÃO VICENTE' in vehicle_data:
        sv_data = vehicle_data['SÃO VICENTE']
        print(
            f"   ✅ Dados de veículos para SÃO VICENTE: {sv_data['total']} veículos")
        print(
            f"      S-1: {sv_data['s1']}, S-2: {sv_data['s2']}, S-2 4X4: {sv_data['s2_4x4']}")

    print(f"\n✅ CORREÇÃO CONCLUÍDA!")
    print(
        f"   - {len(escolas_sao_vicente_final)} escolas agora referenciam 'SÃO VICENTE' corretamente")
    print(f"   - Dashboard atualizado com função de normalização")
    print(f"   - São Vicente deve exibir: S-1=0, S-2=2, S-2 4X4=1, Total=3")


if __name__ == "__main__":
    main()
