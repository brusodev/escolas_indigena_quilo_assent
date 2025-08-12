#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO DE INTEGRAÇÃO - EXPANSÃO DO DASHBOARD
============================================

Este script demonstra como integrar os novos tipos de escola
no dashboard existente, mantendo compatibilidade.

Funcionalidades:
- Integração gradual por tipo
- Manutenção da estrutura atual
- Adição de novos filtros
- Otimização de performance

Autor: Sistema Dashboard Escolas
Data: 11/08/2025
"""

import json
import os
from pathlib import Path

def criar_dados_integrados(tipos_selecionados=None):
    """
    Cria arquivo integrado com tipos selecionados de escola
    
    Args:
        tipos_selecionados: Lista de códigos de tipos a incluir
                          None = usar apenas tipos atuais (10, 31, 36)
    """
    
    if tipos_selecionados is None:
        # Manter apenas tipos atuais do projeto
        tipos_selecionados = [10, 31, 36]  # Indígena, Assentamento, Quilombola
    
    print("🔄 INTEGRANDO TIPOS DE ESCOLA SELECIONADOS")
    print("=" * 50)
    
    # Mapeamento de tipos
    mapeamento_tipos = {
        3: "escolas_ceeja.json",
        6: "escolas_cel_jto.json", 
        7: "escolas_hospitalar.json",
        8: "escolas_regular.json",
        9: "escolas_centro_atend_socioeduc.json",
        10: "escolas_indigena.json",
        15: "escolas_escola_penitenciaria.json",
        31: "escolas_assentamento.json",
        34: "escolas_centro_atend_soc_educ_adolesc.json",
        36: "escolas_quilombola.json"
    }
    
    escolas_integradas = []
    total_por_tipo = {}
    
    for tipo_codigo in tipos_selecionados:
        if tipo_codigo not in mapeamento_tipos:
            print(f"⚠️ Tipo {tipo_codigo} não encontrado")
            continue
            
        arquivo = mapeamento_tipos[tipo_codigo]
        caminho = f"dados/json/por_tipo/{arquivo}"
        
        if not os.path.exists(caminho):
            print(f"❌ Arquivo não encontrado: {arquivo}")
            continue
            
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                escolas_tipo = json.load(f)
            
            # Converter para formato do dashboard atual
            escolas_convertidas = converter_para_formato_dashboard(escolas_tipo, tipo_codigo)
            escolas_integradas.extend(escolas_convertidas)
            
            total_por_tipo[tipo_codigo] = len(escolas_convertidas)
            print(f"✅ Tipo {tipo_codigo}: {len(escolas_convertidas)} escolas integradas")
            
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}")
    
    # Salvar arquivo integrado
    arquivo_saida = "dados/dados_escolas_integradas.json"
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(escolas_integradas, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 RESUMO DA INTEGRAÇÃO")
    print("-" * 30)
    print(f"Total de escolas integradas: {len(escolas_integradas)}")
    print(f"Arquivo gerado: {arquivo_saida}")
    
    for tipo, quantidade in total_por_tipo.items():
        print(f"Tipo {tipo}: {quantidade} escolas")
    
    return escolas_integradas

def converter_para_formato_dashboard(escolas, tipo_codigo):
    """
    Converte escolas do formato CITEM para formato do dashboard
    """
    escolas_convertidas = []
    
    # Mapeamento de tipos para o dashboard
    tipo_dashboard = {
        10: "indigena",
        31: "assentamento", 
        36: "quilombola",
        8: "regular",
        7: "hospitalar",
        3: "ceeja",
        6: "cel_jto",
        15: "penitenciaria",
        9: "socioeduc",
        34: "socioeduc_adolesc"
    }
    
    for escola in escolas:
        # Converter para estrutura do dashboard atual
        escola_dashboard = {
            "name": escola["nome"],
            "type": tipo_dashboard.get(tipo_codigo, f"tipo_{tipo_codigo}"),
            "city": escola["localizacao"]["municipio"],
            "diretoria": escola["administrativa"]["diretoria_ensino"],
            "distance": None,  # Calcular posteriormente
            "lat": escola["localizacao"]["latitude"],
            "lng": escola["localizacao"]["longitude"],
            "de_lat": None,  # Buscar coordenadas da diretoria
            "de_lng": None,
            "endereco_escola": construir_endereco_completo(escola["endereco"]),
            "endereco_diretoria": None,  # Buscar posteriormente
            
            # Campos adicionais do CITEM
            "codigo": escola["codigo"],
            "codigo_mec": escola["codigo_mec"],
            "tipo_codigo": escola["tipo_codigo"],
            "zona": escola["endereco"]["zona"],
            "dependencia": escola["administrativa"]["dependencia"],
            "situacao": escola["administrativa"]["situacao"]
        }
        
        escolas_convertidas.append(escola_dashboard)
    
    return escolas_convertidas

def construir_endereco_completo(endereco):
    """
    Constrói endereço completo a partir dos campos
    """
    partes = []
    
    if endereco["logradouro"]:
        partes.append(endereco["logradouro"])
    
    if endereco["numero"]:
        partes.append(endereco["numero"])
    
    if endereco["bairro"]:
        partes.append(endereco["bairro"])
    
    if endereco["cep"]:
        partes.append(f"CEP: {endereco['cep']}")
    
    return ", ".join(partes)

def exemplo_expansao_gradual():
    """
    Exemplo de como expandir gradualmente o sistema
    """
    print("\n🚀 EXEMPLO DE EXPANSÃO GRADUAL")
    print("=" * 40)
    
    # Etapa 1: Manter apenas tipos atuais
    print("\n📋 ETAPA 1: Tipos atuais (Indígena, Quilombola, Assentamento)")
    criar_dados_integrados([10, 31, 36])
    
    # Etapa 2: Adicionar escolas regulares (amostra)
    print("\n📋 ETAPA 2: Adicionar escolas regulares")
    criar_dados_integrados([10, 31, 36, 8])
    
    # Etapa 3: Adicionar CEEJA
    print("\n📋 ETAPA 3: Adicionar CEEJA")
    criar_dados_integrados([10, 31, 36, 8, 3])
    
    # Etapa 4: Sistema completo
    print("\n📋 ETAPA 4: Sistema completo")
    criar_dados_integrados([3, 6, 7, 8, 9, 10, 15, 31, 34, 36])

def criar_config_tipos():
    """
    Cria arquivo de configuração para tipos de escola
    """
    config = {
        "tipos_escola": {
            "3": {
                "nome": "CEEJA",
                "descricao": "Centro Estadual de Educação de Jovens e Adultos",
                "cor": "#FF9800",
                "icone": "school",
                "ativo": False
            },
            "6": {
                "nome": "CEL JTO",
                "descricao": "Centro de Línguas",
                "cor": "#9C27B0",
                "icone": "language",
                "ativo": False
            },
            "7": {
                "nome": "Hospitalar",
                "descricao": "Escola Hospitalar",
                "cor": "#FF5722",
                "icone": "local_hospital",
                "ativo": False
            },
            "8": {
                "nome": "Regular",
                "descricao": "Escola Regular",
                "cor": "#2196F3",
                "icone": "school",
                "ativo": True
            },
            "9": {
                "nome": "Socioeducativo",
                "descricao": "Centro de Atendimento Socioeducativo",
                "cor": "#795548",
                "icone": "group",
                "ativo": False
            },
            "10": {
                "nome": "Indígena",
                "descricao": "Escola Indígena",
                "cor": "#4CAF50",
                "icone": "nature_people",
                "ativo": True
            },
            "15": {
                "nome": "Penitenciária",
                "descricao": "Escola Penitenciária",
                "cor": "#607D8B",
                "icone": "security",
                "ativo": False
            },
            "31": {
                "nome": "Assentamento",
                "descricao": "Escola de Assentamento",
                "cor": "#8BC34A",
                "icone": "agriculture",
                "ativo": True
            },
            "34": {
                "nome": "Socioeducativo Adolescente",
                "descricao": "Centro de Atendimento Socioeducativo ao Adolescente",
                "cor": "#FFC107",
                "icone": "group",
                "ativo": False
            },
            "36": {
                "nome": "Quilombola",
                "descricao": "Escola Quilombola",
                "cor": "#E91E63",
                "icone": "people",
                "ativo": True
            }
        },
        "configuracao": {
            "tipos_padrao": [10, 31, 36],
            "tipos_disponiveis": [3, 6, 7, 8, 9, 10, 15, 31, 34, 36],
            "limite_mapa": 1000,
            "agrupamento_necessario": 500
        }
    }
    
    with open("dados/config_tipos_escola.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ Arquivo de configuração criado: dados/config_tipos_escola.json")

if __name__ == "__main__":
    print("📚 EXEMPLO DE INTEGRAÇÃO DE TIPOS DE ESCOLA")
    print("Data: 11/08/2025")
    print()
    
    # Criar configuração de tipos
    criar_config_tipos()
    
    # Executar exemplo de expansão gradual
    exemplo_expansao_gradual()
    
    print("\n✅ Exemplos de integração concluídos!")
    print("📂 Verifique os arquivos gerados em 'dados/'")
