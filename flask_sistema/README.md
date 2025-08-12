# Sistema de Gestão Escolar

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
venv\Scripts\activate  # Windows
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
