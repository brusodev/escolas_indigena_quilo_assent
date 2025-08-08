#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd
import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula a distância haversine entre dois pontos em km"""
    R = 6371  # Raio da Terra em km

    # Converter para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Diferenças
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def main():
    print("=== ADICIONANDO 4 NOVAS ESCOLAS DE ASSENTAMENTO ===\n")

    # 1. Carregar dados atuais
    print("1. CARREGANDO DADOS ATUAIS:")
    with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        escolas_atuais = json.load(f)

    print(f"   Escolas atuais: {len(escolas_atuais)}")

    # Contar por tipo
    indigenas_atuais = [
        e for e in escolas_atuais if e.get('type') == 'indigena']
    quilombolas_atuais = [
        e for e in escolas_atuais if e.get('type') == 'quilombola']

    print(f"   - Indígenas: {len(indigenas_atuais)}")
    print(f"   - Quilombolas/Assentamentos: {len(quilombolas_atuais)}")

    # 2. Carregar dados de diretorias para coordenadas
    print(f"\n2. CARREGANDO COORDENADAS DAS DIRETORIAS:")
    try:
        df_diretorias = pd.read_excel('diretorias_com_coordenadas.xlsx')
        print(f"   ✅ {len(df_diretorias)} diretorias carregadas")
    except Exception as e:
        print(f"   ❌ Erro ao carregar diretorias: {e}")
        return

    # 3. Definir as 4 novas escolas
    print(f"\n3. DEFININDO NOVAS ESCOLAS DE ASSENTAMENTO:")

    novas_escolas = [
        {
            'nome': 'BAIRRO DE BOMBAS',
            'cod_escola': '35005693',
            'municipio': 'IPORANGA',
            'diretoria_original': 'APIAI',
            'endereco': 'BAIRRO BOMBAS DE BAIXO, SN',
            'bairro': 'BOMBAS DE BAIXO',
            'cep': '18330000',
            'lat': -24.60935974,
            'lng': -48.65967178
        },
        {
            'nome': 'BAIRRO BOMBAS DE CIMA',
            'cod_escola': '35006283',
            'municipio': 'IPORANGA',
            'diretoria_original': 'APIAI',
            'endereco': 'BAIRRO BOMBAS DE CIMA, SN',
            'bairro': 'BAIRRO BOMBAS DE CIMA',
            'cep': '18330000',
            'lat': -24.60933304,
            'lng': -48.65969086
        },
        {
            'nome': 'FAZENDA DA CAIXA',
            'cod_escola': '35307221',
            'municipio': 'UBATUBA',
            'diretoria_original': 'CARAGUATATUBA',
            'endereco': 'CASA DA FARINHA, S/N',
            'bairro': 'AREA RURAL DE UBATUBA',
            'cep': '11698899',
            'lat': -23.34110069,
            'lng': -44.83760834
        },
        {
            'nome': 'MARIA ANTONIA CHULES PRINCS',
            'cod_escola': '35924489',
            'municipio': 'ELDORADO',
            'diretoria_original': 'REGISTRO',
            'endereco': 'BENEDITO PASCOAL DE FRANCA, KM 37, KM 111',
            'bairro': 'ANDRE LOPEZ',
            'cep': '11960000',
            'lat': -24.60128975,
            'lng': -48.40626144
        }
    ]

    print(f"   ✅ {len(novas_escolas)} escolas definidas")

    # 4. Processar cada escola
    print(f"\n4. PROCESSANDO NOVAS ESCOLAS:")
    escolas_processadas = []

    for escola in novas_escolas:
        print(f"\n   Processando: {escola['nome']}")

        # Buscar coordenadas da diretoria
        diretoria_info = df_diretorias[
            df_diretorias['nome'].str.upper().str.contains(
                escola['diretoria_original'].upper(), na=False)
        ]

        if diretoria_info.empty:
            print(
                f"   ⚠️  Diretoria '{escola['diretoria_original']}' não encontrada, tentando correspondência...")

            # Tentar correspondências alternativas
            mapeamento_diretorias = {
                'APIAI': 'APIAI',
                'CARAGUATATUBA': 'CARAGUATATUBA',
                'REGISTRO': 'REGISTRO'
            }

            diretoria_corrigida = mapeamento_diretorias.get(
                escola['diretoria_original'])
            if diretoria_corrigida:
                diretoria_info = df_diretorias[
                    df_diretorias['nome'].str.upper().str.contains(
                        diretoria_corrigida.upper(), na=False)
                ]

        if not diretoria_info.empty:
            diretoria_row = diretoria_info.iloc[0]
            de_lat = diretoria_row['latitude']
            de_lng = diretoria_row['longitude']
            diretoria_nome = diretoria_row['nome']
            endereco_diretoria = f"{diretoria_row.get('endereco', 'N/A')}, {diretoria_row.get('cidade', 'N/A')}, SP"

            print(f"      ✅ Diretoria encontrada: {diretoria_nome}")
        else:
            print(f"      ❌ Diretoria não encontrada, usando coordenadas padrão")
            de_lat = -22.0
            de_lng = -47.0
            diretoria_nome = escola['diretoria_original']
            endereco_diretoria = f"Diretoria de {escola['diretoria_original']}, SP"

        # Calcular distância
        distancia = haversine_distance(
            escola['lat'], escola['lng'], de_lat, de_lng)

        print(f"      📍 Coordenadas escola: {escola['lat']}, {escola['lng']}")
        print(f"      📍 Coordenadas diretoria: {de_lat}, {de_lng}")
        print(f"      📏 Distância calculada: {distancia:.2f} km")

        # Criar objeto da escola formatado
        escola_formatada = {
            "name": escola['nome'],
            "type": "quilombola",  # Assentamentos são classificados como quilombolas no sistema
            "city": escola['municipio'],
            "diretoria": diretoria_nome,
            "distance": round(distancia, 2),
            "lat": escola['lat'],
            "lng": escola['lng'],
            "de_lat": de_lat,
            "de_lng": de_lng,
            "endereco_escola": escola['endereco'],
            "endereco_diretoria": endereco_diretoria,
            "codigo_escola": escola['cod_escola'],
            "bairro": escola['bairro'],
            "cep": escola['cep']
        }

        escolas_processadas.append(escola_formatada)
        print(f"      ✅ Escola processada com sucesso")

    # 5. Verificar duplicatas
    print(f"\n5. VERIFICANDO DUPLICATAS:")
    nomes_atuais = [e.get('name', '') for e in escolas_atuais]
    duplicatas = []

    for escola in escolas_processadas:
        if escola['name'] in nomes_atuais:
            duplicatas.append(escola['name'])

    if duplicatas:
        print(f"   ⚠️  Duplicatas encontradas: {duplicatas}")
        print(f"   Pulando escolas duplicadas...")
        escolas_processadas = [
            e for e in escolas_processadas if e['name'] not in duplicatas]
    else:
        print(f"   ✅ Nenhuma duplicata encontrada")

    # 6. Adicionar as novas escolas
    print(f"\n6. ADICIONANDO ESCOLAS AO SISTEMA:")
    escolas_atualizadas = escolas_atuais + escolas_processadas

    print(f"   Escolas antes: {len(escolas_atuais)}")
    print(f"   Escolas adicionadas: {len(escolas_processadas)}")
    print(f"   Total final: {len(escolas_atualizadas)}")

    # Contar novos totais
    indigenas_final = [
        e for e in escolas_atualizadas if e.get('type') == 'indigena']
    quilombolas_final = [
        e for e in escolas_atualizadas if e.get('type') == 'quilombola']

    print(f"   - Indígenas: {len(indigenas_final)}")
    print(f"   - Quilombolas/Assentamentos: {len(quilombolas_final)}")

    # 7. Salvar dados atualizados
    print(f"\n7. SALVANDO DADOS ATUALIZADOS:")
    with open('dados_escolas_atualizados.json', 'w', encoding='utf-8') as f:
        json.dump(escolas_atualizadas, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Arquivo 'dados_escolas_atualizados.json' atualizado")

    # 8. Relatório das novas escolas
    print(f"\n8. RELATÓRIO DAS NOVAS ESCOLAS:")
    for escola in escolas_processadas:
        print(f"   ⭐ {escola['name']}")
        print(f"      📍 {escola['city']} → {escola['diretoria']}")
        print(f"      📏 Distância: {escola['distance']} km")
        print(f"      🏷️  Código: {escola['codigo_escola']}")
        print(f"      📧 CEP: {escola['cep']}")
        print(f"")

    print(f"✅ PROCESSO CONCLUÍDO!")
    print(
        f"   {len(escolas_processadas)} escolas de assentamento adicionadas com sucesso")
    print(f"   Total de escolas no sistema: {len(escolas_atualizadas)}")
    print(f"   ({len(indigenas_final)} indígenas + {len(quilombolas_final)} quilombolas/assentamentos)")


if __name__ == "__main__":
    main()
