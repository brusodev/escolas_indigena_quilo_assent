# � Dashboard Escolas Indígenas e Quilombolas

**Sistema integrado de monitoramento e análise de escolas indígenas e quilombolas do Estado de São Paulo**

[![Status](https://img.shields.io/badge/Status-Operacional-brightgreen.svg)]()
[![Versão](https://img.shields.io/badge/Versão-2.0-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)]()
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)]()

---

## 🎯 **Visão Geral**

Dashboard interativo desenvolvido para visualizar e analisar dados de **63 escolas indígenas e quilombolas** distribuídas em **91 Unidades Regionais de Ensino** do Estado de São Paulo. O sistema oferece mapas interativos, estatísticas em tempo real e análise da frota de transporte escolar.

### ✨ **Principais Funcionalidades**
- 🗺️ **Mapas interativos** com coordenadas precisas do estado
- � **Dashboard dinâmico** com estatísticas em tempo real  
- 🚌 **Análise de frota** por tipo de veículo (S-1, S-2, S-2 4x4)
- 🔍 **Sistema de busca** e filtros avançados
- � **Interface responsiva** para desktop e mobile
- 🎨 **Visualizações gráficas** interativas

---

## �️ **Arquitetura Modular**

O projeto foi completamente reestruturado com arquitetura modular para facilitar manutenção e expansão:

```
📦 escolas_indigina_quilo_assent/
├── 📄 dashboard_integrado.html          # Interface principal
├── 📁 static/js/modules/               # Módulos JavaScript
│   ├── 📊 data-loader.js              # Carregamento dinâmico
│   ├── 🎨 ui-components.js            # Interface e componentes
│   ├── 🗺️ map-components.js           # Mapas e coordenadas
│   ├── 📈 charts.js                   # Gráficos e visualizações
│   ├── 🎛️ events.js                   # Event listeners
│   ├── 🚀 dashboard-main.js           # Inicialização
│   └── 🌐 coordinates-loader.js       # Sistema de coordenadas
├── 📁 dados/                          # Datasets e mapeamentos
│   ├── 📋 dados_escolas_atualizados.json
│   ├── 🚌 dados_veiculos_atualizados.json
│   ├── 👥 dados_supervisao_atualizados.json
│   └── 🏛️ mapeamento_unidades_regionais.json
├── 📁 static/js/                      # Coordenadas geográficas
│   ├── 🌍 coordenadas_simples.js      # Contorno básico (56K pontos)
│   └── 🌍 coordenadas_completa.js     # Contorno detalhado
└── 📁 docs/                          # Documentação
    └── 📝 CHANGELOG.md               # Histórico de mudanças
```

---

## � **Como Executar**

### **Pré-requisitos**
- Python 3.12+ instalado
- Navegador web moderno (Chrome, Firefox, Edge)

### **Inicialização Rápida**

1. **Clone ou baixe o repositório**
```bash
git clone [repository-url]
cd escolas_indigina_quilo_assent
```

2. **Inicie o servidor Python**
```bash
python -m http.server 8000
```

3. **Acesse o dashboard**
```
http://localhost:8000/dashboard_integrado.html
```

### **URLs Disponíveis**
- 🏠 **Dashboard Principal:** `http://localhost:8000/dashboard_integrado.html`
- 📊 **Dados JSON:** `http://localhost:8000/dados/`
- 🗺️ **Recursos estáticos:** `http://localhost:8000/static/`

---

## 📊 **Dados do Sistema**

### **Estatísticas Gerais**
- 📚 **63 Escolas** (Indígenas e Quilombolas)
- 🏛️ **91 Unidades Regionais de Ensino** (URE)
- 🚌 **39 Veículos** de transporte escolar
- 👥 **19 Supervisões** de ensino
- 📍 **Precisão GPS:** ±0.1km (Sistema WGS84)

### **Distribuição por Tipo**
- 🏘️ **Escolas Indígenas:** [Quantidade exata exibida no dashboard]
- 🌿 **Escolas Quilombolas:** [Quantidade exata exibida no dashboard]

### **Frota de Veículos**
- 🚐 **S-1:** Veículos pequenos (até 20 passageiros)
- 🚌 **S-2:** Ônibus médio (21-44 passageiros)
- 🚛 **S-2 4x4:** Ônibus para terrenos difíceis

---

## 🗺️ **Sistema de Mapas**

### **Recursos dos Mapas**
- 🌍 **Coordenadas do Estado:** Contorno completo de São Paulo
- 📍 **Marcadores inteligentes:** Escolas e Unidades Regionais
- 🔄 **Modo tela cheia:** Visualização expandida
- 🎯 **Popups informativos:** Detalhes ao clicar
- 🔗 **Conexões visuais:** Linhas escola-diretoria

### **Controles Disponíveis**
- ⚡ **Coordenadas Simples:** Contorno básico (performance)
- 🎨 **Coordenadas Completas:** Contorno detalhado com municípios
- 🔍 **Zoom dinâmico:** Navegação suave
- 📱 **Touch friendly:** Funciona em dispositivos móveis

---

## 🏛️ **Unidades Regionais de Ensino (URE)**

### **Atualização 2025**
O sistema foi atualizado para refletir a nova nomenclatura oficial:
- **Antes:** DIRETORIA DE ENSINO DE [CIDADE]  
- **Agora:** UNIDADE REGIONAL DE ENSINO DE [CIDADE]

### **Siglas Oficiais (Exemplos)**
| Unidade Regional | Sigla | Região |
|-----------------|-------|---------|
| Adamantina | ADA | Oeste |
| Americana | AME | Campinas |
| Araraquara | ARA | Central |
| Barretos | BAT | Norte |
| Campinas Leste | CLT | Metropolitana |
| Campinas Oeste | COE | Metropolitana |
| Santos | SAN | Baixada |
| São José dos Campos | SJC | Vale do Paraíba |

*[Total de 91 URE com siglas oficiais]*

---

## 🔧 **Funcionalidades Técnicas**

### **Carregamento Dinâmico**
- ⚡ **Fetch API:** Dados carregados assincronamente
- 📦 **ES6 Modules:** Arquitetura modular moderna
- 🎯 **Event-driven:** Sistema baseado em eventos
- 💾 **Cache inteligente:** Otimização de performance

### **Interatividade**
- 🔍 **Busca em tempo real:** Por nome de escola
- 🎛️ **Filtros dinâmicos:** Indígena/Quilombola/Todos
- 📊 **Gráficos interativos:** Charts.js integrado
- 🗺️ **Mapas responsivos:** Leaflet.js otimizado

### **Compatibilidade**
- 🌐 **Cross-browser:** Chrome, Firefox, Safari, Edge
- 📱 **Mobile-first:** Design responsivo
- ♿ **Acessibilidade:** Suporte a leitores de tela
- 🎨 **Temas:** Interface moderna e limpa

---

## 📁 **Estrutura de Arquivos**

### **Principais Componentes**

#### **Frontend (Interface)**
- `dashboard_integrado.html` - Interface principal
- `static/css/` - Estilos e temas
- `static/js/modules/` - Módulos JavaScript

#### **Backend (Dados)**
- `dados/*.json` - Datasets principais
- `static/js/coordenadas_*.js` - Dados geográficos
- `dados/mapeamento_unidades_regionais.json` - Mapeamento URE

#### **Documentação**
- `README.md` - Este arquivo
- `docs/CHANGELOG.md` - Histórico detalhado
- `GUIA_RAPIDO.md` - Guia de uso rápido

---

## 🛠️ **Desenvolvimento e Manutenção**

### **Adicionando Novas Escolas**
1. Edite `dados/dados_escolas_atualizados.json`
2. Adicione coordenadas GPS precisas
3. Vincule à URE correspondente
4. Teste no dashboard local

### **Atualizando Frota**
1. Modifique `dados/dados_veiculos_atualizados.json`
2. Mantenha tipologia S-1, S-2, S-2 4x4
3. Vincule à supervisão correta

### **Personalizando Interface**
- Módulos independentes facilitam customização
- CSS responsivo em `static/css/`
- Cores e temas configuráveis

---

## 🔗 **Tecnologias Utilizadas**

- **Frontend:** HTML5, CSS3, JavaScript ES6+
- **Mapas:** Leaflet.js + OpenStreetMap
- **Gráficos:** Chart.js
- **Backend:** Python HTTP Server
- **Dados:** JSON + GeoJSON
- **Coordenadas:** Sistema WGS84

---

## 📞 **Suporte e Contribuição**

### **Reportar Problemas**
- 🐛 Issues técnicos
- 📊 Inconsistências de dados
- 💡 Sugestões de melhorias

### **Contribuir**
1. Fork do repositório
2. Crie branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Abra Pull Request

---

## 📄 **Licença e Uso**

Este projeto é destinado ao monitoramento de escolas indígenas e quilombolas do Estado de São Paulo. Uso educacional e institucional permitido com devida atribuição.

---

## 🎉 **Changelog Recente**

### **Versão 2.0 (Agosto 2025)**
- ✅ Arquitetura modular implementada
- ✅ Sistema de coordenadas dinâmico
- ✅ Atualização para URE (91 unidades)
- ✅ Performance otimizada
- ✅ Mapas fullscreen funcionais
- ✅ Documentação completa

[Ver histórico completo em docs/CHANGELOG.md](docs/CHANGELOG.md)

---

<div align="center">

**🏫 Dashboard Escolas Indígenas e Quilombolas**  
*Monitoramento inteligente para educação inclusiva*

[![Estado de São Paulo](https://img.shields.io/badge/São%20Paulo-91%20URE-green.svg)]()
[![Escolas](https://img.shields.io/badge/Escolas-63%20Unidades-blue.svg)]()
[![Status](https://img.shields.io/badge/Sistema-Operacional-success.svg)]()

</div>
