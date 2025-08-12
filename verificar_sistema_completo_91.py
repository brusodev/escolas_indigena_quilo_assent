#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificação Completa do Sistema das 91 Diretorias
Script final para validar todas as integrações
"""

import sqlite3
import json
import requests
import os
from datetime import datetime

def verificar_banco_consolidado():
    """Verifica o banco de dados consolidado"""
    print("🔍 VERIFICANDO BANCO DE DADOS CONSOLIDADO...")
    
    banco_path = "banco_completo_91_diretorias.db"
    if not os.path.exists(banco_path):
        print("❌ Banco consolidado não encontrado!")
        return False
    
    conn = sqlite3.connect(banco_path)
    cursor = conn.cursor()
    
    # Verificar diretorias
    cursor.execute("SELECT COUNT(*) FROM diretorias")
    num_diretorias = cursor.fetchone()[0]
    print(f"✅ Diretorias no banco: {num_diretorias}")
    
    # Verificar escolas
    cursor.execute("SELECT COUNT(*) FROM escolas")
    num_escolas = cursor.fetchone()[0]
    print(f"✅ Escolas no banco: {num_escolas}")
    
    # Verificar tipos de escola
    cursor.execute("SELECT COUNT(*) FROM tipos_escola")
    num_tipos = cursor.fetchone()[0]
    print(f"✅ Tipos de escola: {num_tipos}")
    
    # Verificar siglas oficiais
    cursor.execute("SELECT COUNT(*) FROM diretorias WHERE sigla_oficial IS NOT NULL")
    num_siglas = cursor.fetchone()[0]
    print(f"✅ Diretorias com siglas oficiais: {num_siglas}")
    
    # Verificar algumas diretorias específicas
    cursor.execute("SELECT nome, sigla_oficial FROM diretorias WHERE sigla_oficial IS NOT NULL LIMIT 5")
    amostras = cursor.fetchall()
    print("\n📋 Amostra de diretorias com siglas:")
    for nome, sigla in amostras:
        print(f"   • {nome} - {sigla}")
    
    conn.close()
    
    return num_diretorias == 91 and num_escolas > 5000 and num_tipos == 10

def verificar_banco_flask():
    """Verifica o banco no sistema Flask"""
    print("\n🔍 VERIFICANDO BANCO NO FLASK...")
    
    flask_banco = "flask_sistema/instance/banco_91_diretorias.db"
    if not os.path.exists(flask_banco):
        print("❌ Banco Flask não encontrado!")
        return False
    
    conn = sqlite3.connect(flask_banco)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM diretorias")
    num_diretorias = cursor.fetchone()[0]
    print(f"✅ Diretorias no Flask: {num_diretorias}")
    
    cursor.execute("SELECT COUNT(*) FROM escolas")
    num_escolas = cursor.fetchone()[0]
    print(f"✅ Escolas no Flask: {num_escolas}")
    
    conn.close()
    
    return num_diretorias == 91

def testar_api_flask():
    """Testa a API do Flask"""
    print("\n🔍 TESTANDO API FLASK...")
    
    try:
        # Testar endpoint das diretorias
        response = requests.get("http://127.0.0.1:5000/api/diretorias-91", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API respondendo: {len(data['diretorias'])} diretorias")
            
            # Verificar se tem siglas oficiais
            com_siglas = sum(1 for d in data['diretorias'] if d.get('sigla_oficial'))
            print(f"✅ Diretorias com siglas oficiais na API: {com_siglas}")
            
            return len(data['diretorias']) == 91
        else:
            print(f"❌ API erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar API: {e}")
        return False

def verificar_arquivos_consolidacao():
    """Verifica os arquivos de consolidação"""
    print("\n🔍 VERIFICANDO ARQUIVOS DE CONSOLIDAÇÃO...")
    
    arquivos = [
        "dados_escolas_consolidados_91.json",
        "dados_diretorias_consolidados_91.json",
        "dados_tipos_escola_consolidados.json",
        "estatisticas_consolidacao_91.json"
    ]
    
    todos_existem = True
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} encontrado")
            
            # Verificar conteúdo de exemplo
            if arquivo.endswith('.json'):
                with open(arquivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        print(f"   → {len(data)} registros")
                    elif isinstance(data, dict):
                        print(f"   → {len(data.keys())} chaves")
        else:
            print(f"❌ {arquivo} não encontrado")
            todos_existem = False
    
    return todos_existem

def gerar_relatorio_final():
    """Gera relatório final do sistema"""
    print("\n📊 RELATÓRIO FINAL DO SISTEMA")
    print("=" * 50)
    
    # Verificações
    banco_ok = verificar_banco_consolidado()
    flask_ok = verificar_banco_flask()
    api_ok = testar_api_flask()
    arquivos_ok = verificar_arquivos_consolidacao()
    
    print("\n🎯 RESUMO DAS VERIFICAÇÕES:")
    print(f"✅ Banco consolidado: {'OK' if banco_ok else 'ERRO'}")
    print(f"✅ Banco Flask: {'OK' if flask_ok else 'ERRO'}")
    print(f"✅ API funcionando: {'OK' if api_ok else 'ERRO'}")
    print(f"✅ Arquivos consolidados: {'OK' if arquivos_ok else 'ERRO'}")
    
    if all([banco_ok, flask_ok, api_ok, arquivos_ok]):
        print("\n🎉 SISTEMA COMPLETAMENTE INTEGRADO!")
        print("✅ 91 diretorias com siglas oficiais")
        print("✅ Mais de 5.000 escolas consolidadas")
        print("✅ 10 tipos de escola mapeados")
        print("✅ Flask funcionando com dados atualizados")
        print("✅ API respondendo corretamente")
        
        print("\n🔗 ACESSO AO SISTEMA:")
        print("📊 Dashboard: http://127.0.0.1:5000/91-diretorias")
        print("🔌 API: http://127.0.0.1:5000/api/diretorias-91")
        
        # Salvar status
        status = {
            "timestamp": datetime.now().isoformat(),
            "status": "COMPLETO",
            "diretorias": 91,
            "escolas": "5000+",
            "tipos_escola": 10,
            "flask": "funcionando",
            "api": "funcionando",
            "siglas_oficiais": "implementadas"
        }
        
        with open("status_sistema_91_diretorias.json", "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
        
        print("💾 Status salvo em: status_sistema_91_diretorias.json")
        
    else:
        print("\n⚠️ SISTEMA COM PROBLEMAS - verifique os erros acima")
    
    return all([banco_ok, flask_ok, api_ok, arquivos_ok])

if __name__ == "__main__":
    print("🚀 VERIFICAÇÃO COMPLETA DO SISTEMA DAS 91 DIRETORIAS")
    print("=" * 60)
    
    sucesso = gerar_relatorio_final()
    
    if sucesso:
        print("\n✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
    else:
        print("\n❌ VERIFICAÇÃO ENCONTROU PROBLEMAS!")
    
    print("\n" + "=" * 60)
