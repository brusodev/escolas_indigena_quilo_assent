#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpeza e Organização do Projeto
Preparação para migração Flask + SQLAlchemy + PostgreSQL
"""

import os
import shutil
from pathlib import Path
import json


def arquivos_para_manter():
    """Define quais arquivos devem ser mantidos"""
    return {
        # Bases de dados padronizadas (recém criadas)
        'bases_padronizadas/',

        # JSONs principais de dados
        'dados_escolas_atualizados.json',
        'dados_veiculos_diretorias.json',
        'dados_supervisao_atualizados.json',
        'estatisticas_atualizadas.json',

        # Excel com informações importantes
        'diretorias_com_coordenadas.xlsx',
        'diretorias_ensino_completo.xlsx',
        'QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx',
        'GEP.xlsx',
        'ENDERECO_ESCOLAS_062025 (1).csv',

        # Documentação
        'README.md',
        'GUIA_RAPIDO.md',
        'relatorio_bruno.md',

        # Scripts úteis que podem ser aproveitados
        'calcular_distancias.py',
        'processar_dados_atualizados.py',
        'padronizar_bases.py',

        # Git
        '.git/',
        '.gitignore'
    }


def arquivos_para_remover():
    """Identifica arquivos que podem ser removidos"""
    return {
        # Dashboard antigo e arquivos relacionados
        'dashboard_integrado.html',
        'index.html',
        'distancias_escolas.html',
        'dashboard_corrigido_final.html',

        # Scripts do dashboard que não serão mais necessários
        'atualizar_dashboard_completo.py',
        'atualizar_dashboard.py',
        'criar_dashboard_corrigido_final.py',
        'servidor_corrigido_final.py',
        'menu_integrado.py',
        'mostrar_dados_atuais.py',

        # Scripts de geração de relatórios antigos
        'gerar_graficos_frota.py',
        'gerar_relatorio_excel.py',
        'gerar_relatorio_pdf.py',
        'gerar_relatorios.py',
        'relatorio_final_status.py',

        # Scripts de correção que já foram executados
        'corrigir_coordenadas.py',
        'corrigir_distancias.py',
        'atualizar_relatorios_haversine.py',
        'atualizar_sistema_distancias.py',
        'regenerar_tudo_atualizado.py',

        # Scripts de validação antigos
        'validar_distancias_completo.py',
        'verificar_completo.py',
        'verificar_dados.py',
        'verificar_enderecos_v2.py',

        # Outros scripts desnecessários
        'analise_frota_integrada.py',
        'converter_dados.py',
        'criar_bases_exemplo.py',
        'testar_dashboard_completo.py',
        'main.py',

        # JSONs duplicados ou temporários
        'dados_escolas_corrigidos.json',
        'dados_js_corrigidos.txt',
        'dados_veiculos.json',

        # Relatórios PDF gerados (podem ser regenerados)
        'Relatorio_*.pdf',
        'Graficos_*.png',
        'Mapa_Calor_*.png',

        # Excel de relatórios (podem ser regenerados)
        'Analise_Integrada_*.xlsx',
        'distancias_escolas_diretorias*.xlsx',
        'Relatorio_*.xlsx',

        # Arquivos de metodologia (informação já documentada)
        'Metodologia_*.txt',

        # Diretórios antigos do dashboard
        'static/',
        'dados/js/',
        'templates/'
    }


def criar_estrutura_flask():
    """Cria a estrutura básica do projeto Flask"""
    print("\n🏗️ CRIANDO ESTRUTURA FLASK...")
    print("-" * 40)

    # Estrutura do projeto Flask
    estrutura = {
        'app/': {
            '__init__.py': '',
            'models/': {
                '__init__.py': '',
                'escola.py': '',
                'diretoria.py': '',
                'veiculo.py': '',
                'supervisor.py': '',
                'distancia.py': ''
            },
            'routes/': {
                '__init__.py': '',
                'escolas.py': '',
                'diretorias.py': '',
                'veiculos.py': '',
                'api.py': '',
                'dashboard.py': ''
            },
            'templates/': {
                'base.html': '',
                'dashboard/': {
                    'index.html': '',
                    'escolas.html': '',
                    'diretorias.html': '',
                    'relatorios.html': ''
                }
            },
            'static/': {
                'css/': {
                    'style.css': ''
                },
                'js/': {
                    'dashboard.js': '',
                    'maps.js': ''
                }
            },
            'utils/': {
                '__init__.py': '',
                'database.py': '',
                'calculations.py': '',
                'imports.py': ''
            }
        },
        'migrations/': {},
        'data/': {},
        'tests/': {
            '__init__.py': '',
            'test_models.py': '',
            'test_routes.py': ''
        },
        'config/': {
            '__init__.py': '',
            'settings.py': '',
            'database.py': ''
        }
    }

    def criar_estrutura(base_path, estrutura_dict):
        for nome, conteudo in estrutura_dict.items():
            caminho = base_path / nome

            if isinstance(conteudo, dict):
                # É um diretório
                caminho.mkdir(exist_ok=True)
                criar_estrutura(caminho, conteudo)
                print(f"📁 {caminho}")
            else:
                # É um arquivo
                caminho.parent.mkdir(parents=True, exist_ok=True)
                if not caminho.exists():
                    caminho.write_text(conteudo, encoding='utf-8')
                print(f"📄 {caminho}")

    # Criar estrutura
    base_path = Path('flask_sistema')
    base_path.mkdir(exist_ok=True)
    criar_estrutura(base_path, estrutura)

    return base_path


def criar_arquivos_base_flask():
    """Cria arquivos base do Flask"""
    print("\n📝 CRIANDO ARQUIVOS BASE FLASK...")
    print("-" * 40)

    # requirements.txt
    requirements = """Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
psycopg2-binary==2.9.7
python-dotenv==1.0.0
pandas==2.0.3
geopy==2.3.0
folium==0.14.0
plotly==5.15.0
gunicorn==21.2.0
"""

    with open('flask_sistema/requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ requirements.txt criado")

    # .env.example
    env_example = """# Configurações do Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/escolas_sistema
POSTGRES_USER=sistema_escolas
POSTGRES_PASSWORD=sua_senha_aqui
POSTGRES_DB=escolas_sistema
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Configurações da Aplicação
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui

# Configurações de Debug
DEBUG=True
"""

    with open('flask_sistema/.env.example', 'w') as f:
        f.write(env_example)
    print("✅ .env.example criado")

    # run.py
    run_py = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Ponto de entrada da aplicação Flask
Sistema de Gestão de Escolas, Diretorias e Transporte
\"\"\"

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
"""

    with open('flask_sistema/run.py', 'w', encoding='utf-8') as f:
        f.write(run_py)
    print("✅ run.py criado")

    # docker-compose.yml
    docker_compose = """version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://sistema_escolas:senha123@db:5432/escolas_sistema
    depends_on:
      - db
    volumes:
      - .:/app
      - ./data:/app/data

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: sistema_escolas
      POSTGRES_PASSWORD: senha123
      POSTGRES_DB: escolas_sistema
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./data/sql:/docker-entrypoint-initdb.d

volumes:
  postgres_data:
"""

    with open('flask_sistema/docker-compose.yml', 'w') as f:
        f.write(docker_compose)
    print("✅ docker-compose.yml criado")

    # Dockerfile
    dockerfile = """FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]
"""

    with open('flask_sistema/Dockerfile', 'w') as f:
        f.write(dockerfile)
    print("✅ Dockerfile criado")


def mover_bases_padronizadas():
    """Move as bases padronizadas para o projeto Flask"""
    print("\n📦 MOVENDO BASES PADRONIZADAS...")
    print("-" * 40)

    source = Path('bases_padronizadas')
    destination = Path('flask_sistema/data/json')

    if source.exists():
        destination.mkdir(parents=True, exist_ok=True)

        for arquivo in source.glob('*.json'):
            shutil.copy2(arquivo, destination)
            print(f"✅ {arquivo.name} -> {destination}/{arquivo.name}")

    # Copiar também outros JSONs importantes
    arquivos_importantes = [
        'dados_escolas_atualizados.json',
        'dados_veiculos_diretorias.json',
        'dados_supervisao_atualizados.json',
        'estatisticas_atualizadas.json'
    ]

    for arquivo in arquivos_importantes:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, destination)
            print(f"✅ {arquivo} -> {destination}/{arquivo}")


def criar_readme_flask():
    """Cria README do projeto Flask"""
    readme_content = """# Sistema de Gestão Escolar

Sistema web desenvolvido em Flask para gestão de escolas, diretorias de ensino e transporte escolar do estado de São Paulo.

## 🏗️ Arquitetura

- **Backend**: Flask + SQLAlchemy
- **Banco de Dados**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript (Leaflet.js para mapas)
- **Deploy**: Docker + Docker Compose

## 📊 Entidades Principais

### 🏫 Escolas (5,582 registros)
- Escolas Indígenas, Quilombolas, Assentamento e Regulares
- Geolocalização e endereços completos
- Relacionamento com Diretorias de Ensino

### 🏛️ Diretorias de Ensino (91 registros)
- Diretorias responsáveis pelas escolas
- Coordenadas geográficas
- Controle de veículos por diretoria

### 🚗 Veículos (172 registros)
- Tipos: S-1, S-2 e S-2 4X4
- Distribuição por diretoria
- Capacidade e especificações

### 👥 Supervisores
- Supervisores do GEP por diretoria
- Áreas de responsabilidade

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.11+
- PostgreSQL 15+
- Docker (opcional)

### Instalação Local

1. **Clone o repositório**
```bash
git clone <repo-url>
cd flask_sistema
```

2. **Crie ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Configure banco de dados**
```bash
# Configure PostgreSQL
createdb escolas_sistema

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações
```

5. **Execute migrações**
```bash
flask db upgrade
```

6. **Importe dados iniciais**
```bash
python -c "from app.utils.imports import import_all_data; import_all_data()"
```

7. **Execute a aplicação**
```bash
python run.py
```

### Execução com Docker

```bash
docker-compose up -d
```

## 📂 Estrutura do Projeto

```
flask_sistema/
├── app/
│   ├── models/          # Modelos SQLAlchemy
│   ├── routes/          # Rotas da aplicação
│   ├── templates/       # Templates HTML
│   ├── static/          # CSS, JS, imagens
│   └── utils/           # Utilitários
├── data/
│   ├── json/           # Dados JSON originais
│   └── sql/            # Scripts SQL
├── migrations/         # Migrações do banco
├── tests/             # Testes
└── config/            # Configurações
```

## 🔧 Funcionalidades

- ✅ Dashboard interativo com mapas
- ✅ Gestão de escolas por tipo
- ✅ Controle de veículos por diretoria
- ✅ Cálculo de distâncias (Haversine)
- ✅ Relatórios estatísticos
- ✅ API REST para integração
- ✅ Sistema de filtros avançados

## 📊 Dashboard

O sistema inclui um dashboard completo com:
- 🗺️ Mapa interativo com todas as escolas e diretorias
- 📊 Gráficos estatísticos
- 🔍 Sistema de filtros por tipo de escola
- 📏 Visualização de distâncias escola-diretoria
- 🚗 Controle de frota por diretoria

## 🛠️ Desenvolvimento

### Adicionando novas funcionalidades

1. **Modelos**: Adicione em `app/models/`
2. **Rotas**: Adicione em `app/routes/`
3. **Templates**: Adicione em `app/templates/`
4. **Migrações**: Execute `flask db migrate -m "descrição"`

### Testes

```bash
python -m pytest tests/
```

## 📄 Licença

Projeto desenvolvido para gestão educacional do estado de São Paulo.

## 👥 Contribuição

Para contribuir:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para suporte técnico, consulte a documentação ou abra uma issue no repositório.
"""

    with open('flask_sistema/README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ README.md do Flask criado")


def listar_arquivos_para_limpeza():
    """Lista arquivos que serão removidos"""
    print("\n🧹 ANALISANDO ARQUIVOS PARA LIMPEZA...")
    print("-" * 40)

    manter = arquivos_para_manter()
    remover = arquivos_para_remover()

    arquivos_existentes = []
    for item in Path('.').rglob('*'):
        if item.is_file():
            arquivos_existentes.append(str(item))

    # Identificar o que será mantido e removido
    sera_mantido = []
    sera_removido = []

    for arquivo in arquivos_existentes:
        arquivo_normalizado = arquivo.replace('\\', '/')

        # Verificar se deve ser mantido
        deve_manter = False
        for padrao in manter:
            if padrao.endswith('/'):
                if arquivo_normalizado.startswith(padrao):
                    deve_manter = True
                    break
            else:
                if arquivo_normalizado.endswith(padrao) or padrao in arquivo_normalizado:
                    deve_manter = True
                    break

        if deve_manter:
            sera_mantido.append(arquivo)
        else:
            # Verificar se está na lista de remoção
            for padrao in remover:
                if padrao in arquivo_normalizado or arquivo_normalizado.endswith(padrao):
                    sera_removido.append(arquivo)
                    break

    print(f"📊 RESUMO:")
    print(f"   📁 Total de arquivos: {len(arquivos_existentes)}")
    print(f"   ✅ Serão mantidos: {len(sera_mantido)}")
    print(f"   🗑️ Serão removidos: {len(sera_removido)}")

    if sera_removido:
        print(f"\n🗑️ ARQUIVOS PARA REMOÇÃO:")
        for arquivo in sorted(sera_removido):
            print(f"   - {arquivo}")

    return sera_mantido, sera_removido


def main():
    """Função principal"""
    print("🧹 LIMPEZA E ORGANIZAÇÃO DO PROJETO")
    print("Preparando para migração Flask + SQLAlchemy + PostgreSQL")
    print("=" * 60)

    # 1. Analisar arquivos
    mantidos, removidos = listar_arquivos_para_limpeza()

    # 2. Criar estrutura Flask
    flask_dir = criar_estrutura_flask()

    # 3. Criar arquivos base
    criar_arquivos_base_flask()

    # 4. Mover bases padronizadas
    mover_bases_padronizadas()

    # 5. Criar README
    criar_readme_flask()

    print(f"\n🎉 ORGANIZAÇÃO CONCLUÍDA!")
    print(f"📁 Projeto Flask criado em: {flask_dir}")
    print(f"📊 Estrutura preparada para SQLAlchemy + PostgreSQL")
    print(f"\n📋 PRÓXIMOS PASSOS:")
    print(f"   1. cd flask_sistema")
    print(f"   2. pip install -r requirements.txt")
    print(f"   3. Configurar PostgreSQL")
    print(f"   4. cp .env.example .env (e editar)")
    print(f"   5. flask db init && flask db migrate && flask db upgrade")
    print(f"   6. python run.py")

    # Opção de limpar arquivos antigos
    if removidos:
        print(
            f"\n⚠️ ATENÇÃO: {len(removidos)} arquivos antigos identificados para remoção")
        print(f"Execute o script com --clean para remover arquivos desnecessários")


if __name__ == "__main__":
    main()
