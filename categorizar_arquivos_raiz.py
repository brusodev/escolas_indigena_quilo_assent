"""
Análise e categorização dos arquivos na pasta raiz
Data: 09/08/2025
"""

import os
import glob


def categorizar_arquivos_raiz():
    """Categoriza todos os arquivos na pasta raiz"""

    print("📁 ANÁLISE DOS ARQUIVOS NA PASTA RAIZ")
    print("=" * 60)
    print()

    # Categorias
    categorias = {
        "PRINCIPAIS": {
            "arquivos": [],
            "descricao": "Arquivos principais do sistema"
        },
        "SCRIPTS_ATUALIZACAO": {
            "arquivos": [],
            "descricao": "Scripts para atualizar dados e sistemas"
        },
        "SCRIPTS_CORRECAO": {
            "arquivos": [],
            "descricao": "Scripts para corrigir problemas específicos"
        },
        "SCRIPTS_VALIDACAO": {
            "arquivos": [],
            "descricao": "Scripts para validar e verificar dados"
        },
        "SCRIPTS_GERACAO": {
            "arquivos": [],
            "descricao": "Scripts para gerar relatórios e análises"
        },
        "SCRIPTS_TESTE": {
            "arquivos": [],
            "descricao": "Scripts de teste e debug"
        },
        "RELATORIOS_MD": {
            "arquivos": [],
            "descricao": "Documentação e relatórios em Markdown"
        },
        "DADOS_JSON": {
            "arquivos": [],
            "descricao": "Arquivos de dados JSON"
        },
        "HTML": {
            "arquivos": [],
            "descricao": "Arquivos HTML e dashboards"
        },
        "PASTAS": {
            "arquivos": [],
            "descricao": "Diretórios"
        },
        "OUTROS": {
            "arquivos": [],
            "descricao": "Outros arquivos"
        }
    }

    # Listar todos os arquivos
    arquivos = os.listdir('.')

    # Categorizar cada arquivo
    for arquivo in sorted(arquivos):
        if os.path.isdir(arquivo):
            categorias["PASTAS"]["arquivos"].append(arquivo)
        elif arquivo.endswith('.json'):
            categorias["DADOS_JSON"]["arquivos"].append(arquivo)
        elif arquivo.endswith('.html'):
            categorias["HTML"]["arquivos"].append(arquivo)
        elif arquivo.endswith('.md'):
            categorias["RELATORIOS_MD"]["arquivos"].append(arquivo)
        elif arquivo.endswith('.py'):
            # Categorizar scripts Python
            if any(palavra in arquivo.lower() for palavra in ['atualizar', 'adicionar', 'migrar', 'sincronizar']):
                categorias["SCRIPTS_ATUALIZACAO"]["arquivos"].append(arquivo)
            elif any(palavra in arquivo.lower() for palavra in ['corrigir', 'correcao', 'fix']):
                categorias["SCRIPTS_CORRECAO"]["arquivos"].append(arquivo)
            elif any(palavra in arquivo.lower() for palavra in ['verificar', 'validar', 'validacao', 'check']):
                categorias["SCRIPTS_VALIDACAO"]["arquivos"].append(arquivo)
            elif any(palavra in arquivo.lower() for palavra in ['gerar', 'criar', 'processar', 'relatorio']):
                categorias["SCRIPTS_GERACAO"]["arquivos"].append(arquivo)
            elif any(palavra in arquivo.lower() for palavra in ['test', 'debug', 'investigar', 'analisar']):
                categorias["SCRIPTS_TESTE"]["arquivos"].append(arquivo)
            elif arquivo in ['main.py', 'README.md']:
                categorias["PRINCIPAIS"]["arquivos"].append(arquivo)
            else:
                categorias["OUTROS"]["arquivos"].append(arquivo)
        else:
            if arquivo in ['README.md', 'main.py']:
                categorias["PRINCIPAIS"]["arquivos"].append(arquivo)
            else:
                categorias["OUTROS"]["arquivos"].append(arquivo)

    # Exibir resultado
    total_arquivos = 0
    for categoria, info in categorias.items():
        if info["arquivos"]:
            print(f"🔸 {categoria} ({len(info['arquivos'])} arquivos)")
            print(f"   {info['descricao']}")
            print("-" * 50)
            for arquivo in info["arquivos"]:
                print(f"   📄 {arquivo}")
            print()
            total_arquivos += len(info["arquivos"])

    print("=" * 60)
    print(f"📊 TOTAL: {total_arquivos} itens na pasta raiz")
    print()

    # Sugestões de organização
    print("💡 SUGESTÕES DE ORGANIZAÇÃO:")
    print()
    print("📁 ESTRUTURA RECOMENDADA:")
    print("├── 📄 main.py                     (arquivo principal)")
    print("├── 📄 dashboard_integrado.html    (dashboard principal)")
    print("├── 📄 README.md                   (documentação)")
    print("├── 📄 *.json                      (dados principais)")
    print("├── 📁 scripts/")
    print("│   ├── 📁 atualizacao/            (scripts de atualização)")
    print("│   ├── 📁 correcao/               (scripts de correção)")
    print("│   ├── 📁 validacao/              (scripts de validação)")
    print("│   ├── 📁 geracao/                (scripts de geração)")
    print("│   └── 📁 teste/                  (scripts de teste)")
    print("├── 📁 documentacao/")
    print("│   ├── 📁 relatorios/             (relatórios markdown)")
    print("│   └── 📁 historico/              (documentação histórica)")
    print("├── 📁 dados/")
    print("├── 📁 relatorios/")
    print("└── 📁 old_backups/")

    print()
    print("🚀 AÇÕES RECOMENDADAS:")
    print("1. Mover scripts Python para subpastas em scripts/")
    print("2. Mover relatórios .md para documentacao/relatorios/")
    print("3. Manter apenas arquivos essenciais na raiz")
    print("4. Organizar por funcionalidade")


if __name__ == "__main__":
    categorizar_arquivos_raiz()
