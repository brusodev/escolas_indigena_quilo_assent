#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re


def main():
    print("=== VERIFICAÇÃO FINAL - SÃO VICENTE E CONTAGEM ===\n")

    # 1. Verificar dados JSON
    print("1. DADOS JSON:")
    with open('dados_veiculos_atualizados.json', 'r', encoding='utf-8') as f:
        dados_json = json.load(f)

    print(f"   Total de diretorias: {len(dados_json)}")

    if 'SÃO VICENTE' in dados_json:
        sv_data = dados_json['SÃO VICENTE']
        print(
            f"   ✅ São Vicente: S-1={sv_data['s1']}, S-2={sv_data['s2']}, S-2 4X4={sv_data['s2_4x4']}, Total={sv_data['total']}")
    else:
        print("   ❌ São Vicente não encontrado no JSON")

    # 2. Verificar dashboard HTML
    print("\n2. DASHBOARD HTML:")
    with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extrair vehicleData
    start = html_content.find('const vehicleData = {')
    if start != -1:
        end = html_content.find('};', start) + 2
        vehicle_data_js = html_content[start:end]

        # Contar entradas usando regex mais preciso
        pattern = r'"([^"]+)":\s*\{'
        matches = re.findall(pattern, vehicle_data_js)

        print(f"   Total de diretorias no vehicleData: {len(matches)}")

        # Verificar São Vicente
        sao_vicente_found = False
        for match in matches:
            if 'VICENTE' in match.upper():
                print(f"   ✅ Encontrado: '{match}'")
                sao_vicente_found = True

        if not sao_vicente_found:
            print("   ❌ São Vicente não encontrado no vehicleData")

        # Verificar se há duplicatas
        unique_matches = set(matches)
        if len(matches) != len(unique_matches):
            print(
                f"   ⚠️  DUPLICATAS ENCONTRADAS: {len(matches)} entradas, {len(unique_matches)} únicas")
            duplicates = []
            for match in matches:
                if matches.count(match) > 1 and match not in duplicates:
                    duplicates.append(match)
            for dup in duplicates:
                print(f"       - '{dup}' aparece {matches.count(dup)} vezes")
        else:
            print(f"   ✅ Sem duplicatas: {len(matches)} entradas únicas")

    # 3. Testar busca de São Vicente no dashboard
    print("\n3. TESTE DE BUSCA DE SÃO VICENTE:")

    # Simular busca como o dashboard faria
    test_diretorias = ['SAO VICENTE',
                       'SÃO VICENTE', 'Sao Vicente', 'são vicente']

    for test_dir in test_diretorias:
        test_key = test_dir.upper()
        if test_key in matches:
            print(f"   ✅ '{test_dir}' → '{test_key}' ENCONTRADO")
        else:
            print(f"   ❌ '{test_dir}' → '{test_key}' NÃO ENCONTRADO")

    # 4. Verificar dados de escolas que referenciam São Vicente
    print("\n4. ESCOLAS DE SÃO VICENTE:")
    try:
        with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
            escolas_data = json.load(f)

        escolas_sao_vicente = []
        for escola in escolas_data:
            if 'diretoria' in escola and 'VICENTE' in escola['diretoria'].upper():
                escolas_sao_vicente.append({
                    'nome': escola.get('nome', 'N/A'),
                    'diretoria': escola['diretoria'],
                    'tipo': escola.get('tipo', 'N/A')
                })

        print(f"   Encontradas {len(escolas_sao_vicente)} escolas:")
        for escola in escolas_sao_vicente:
            print(
                f"   - {escola['nome']} ({escola['tipo']}) → '{escola['diretoria']}'")

    except Exception as e:
        print(f"   ❌ Erro ao verificar escolas: {e}")

    # 5. Criar teste para browser
    print("\n5. CRIANDO TESTE JAVASCRIPT:")

    js_test = """
    // Teste para o console do browser
    console.log('=== TESTE SÃO VICENTE ===');
    console.log('Diretorias no vehicleData:', Object.keys(vehicleData).length);
    console.log('Total de veículos:', Object.values(vehicleData).reduce((sum, v) => sum + v.total, 0));
    
    // Testar São Vicente
    const testKeys = ['SAO VICENTE', 'SÃO VICENTE', 'São Vicente'.toUpperCase()];
    testKeys.forEach(key => {
        if (vehicleData[key]) {
            console.log(`✅ ${key}:`, vehicleData[key]);
        } else {
            console.log(`❌ ${key}: não encontrado`);
        }
    });
    
    // Mostrar todas as chaves que contêm 'VICENTE'
    const vicenteKeys = Object.keys(vehicleData).filter(k => k.includes('VICENTE'));
    console.log('Chaves contendo VICENTE:', vicenteKeys);
    """

    with open('teste_sao_vicente.js', 'w', encoding='utf-8') as f:
        f.write(js_test)

    print("   ✅ Teste JavaScript salvo em 'teste_sao_vicente.js'")
    print("   🔍 Para testar no browser:")
    print("   1. Abra o dashboard (distancias_escolas.html)")
    print("   2. Abra o console do navegador (F12)")
    print("   3. Cole e execute o código do arquivo teste_sao_vicente.js")


if __name__ == "__main__":
    main()
