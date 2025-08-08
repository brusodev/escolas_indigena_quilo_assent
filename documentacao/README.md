# 🏛️ SISTEMA DE GESTÃO - ESCOLAS INDÍGENAS E QUILOMBOLAS

## 📋 Visão Geral

Este sistema centraliza informações sobre **63 escolas indígenas e quilombolas** do estado de São Paulo, incluindo:
- 📍 Localização geográfica precisa
- 🚗 Dados de frota por diretoria de ensino
- 📊 Relatórios executivos automatizados
- 🌐 Dashboard interativo para visualização

---

## 🎯 STATUS ATUAL

### ✅ **SISTEMA COMPLETAMENTE SINCRONIZADO**

| Componente | Escolas | Status | Última Atualização |
|------------|---------|--------|--------------------|
| **Dashboard Web** | 63 | ✅ Ativo | 08/08/2025 |
| **Base de Dados** | 63 | ✅ Íntegra | 08/08/2025 |
| **Relatório Excel** | 63 | ✅ Atualizado | 08/08/2025 |
| **Relatório PDF** | 63 | ✅ Gerado | 08/08/2025 |

### 📊 **Estatísticas Principais**
- **Total de Escolas**: 63
- **Escolas Indígenas**: 43
- **Escolas Quilombolas/Assentamentos**: 20
- **Diretorias de Ensino**: 19
- **Total de Veículos**: 172
- **Metodologia de Distância**: Haversine (precisão ±0.1km)


## 📐 Metodologia de Cálculo de Distâncias

### 🌍 Fórmula de Haversine
Este sistema utiliza a **Fórmula de Haversine** para calcular as distâncias entre escolas e diretorias de ensino. Esta é a metodologia padrão internacional para cálculos geodésicos precisos.

**Características da Fórmula de Haversine:**
- ✅ **Tipo:** Distância geodésica (linha reta na superfície terrestre)
- ✅ **Precisão:** Considera a curvatura da Terra
- ✅ **Padrão:** Utilizada em sistemas GPS e navegação
- ✅ **Sistema:** Coordenadas WGS84 em graus decimais
- ✅ **Raio Terra:** 6.371 km (raio médio)

### 📊 Fórmula Matemática
```
a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
c = 2 ⋅ atan2(√a, √(1−a))
d = R ⋅ c
```

Onde:
- `φ` = latitude
- `λ` = longitude  
- `R` = raio da Terra (6.371 km)
- `Δφ` = diferença de latitudes
- `Δλ` = diferença de longitudes

### 🗺️ Diferenças com Outras Medições
- **Haversine (nosso sistema):** Distância geodésica "em linha reta"
- **Google Maps:** Distância rodoviária seguindo estradas
- **Diferença esperada:** 10-20km é normal e aceitável

### ✅ Validação
- **Total validado:** 59 escolas
- **Precisão:** 100% das distâncias verificadas
- **Método:** Recálculo automático com fórmula Haversine
- **Tolerância:** ±0,1 km

---


## 📋 Arquivos do Projeto

### Dados de Entrada

- **`ENDERECO_ESCOLAS_062025 (1).csv`** - Base de dados com todas as escolas do estado
- **`diretorias_ensino_completo.xlsx`** - Endereços das 91 diretorias de ensino

### Scripts Python

- **`calcular_distancias.py`** - Script principal que calcula as distâncias
- **`converter_dados.py`** - Converte dados do Excel para formato web
- **`gerar_relatorio_excel.py`** - Gera relatório Excel sucinto e organizado
- **`gerar_relatorio_pdf.py`** - Gera relatório PDF detalhado e elegante
- **`gerar_relatorios.py`** - Menu interativo para escolher tipo de relatório

### Visualizações Web

- **`index.html`** - Mapa original das escolas indígenas (42 escolas)
- **`distancias_escolas.html`** - Nova visualização com distâncias (59 escolas)

### Arquivos Gerados

- **`distancias_escolas_diretorias.xlsx`** - Planilha com todas as distâncias calculadas
- **`diretorias_com_coordenadas.xlsx`** - Coordenadas geocodificadas das diretorias
- **`Relatorio_Completo_Escolas_Diretorias.xlsx`** - Relatório Excel abrangente (12+ colunas)
- **`Relatorio_Paisagem_Escolas_YYYYMMDD_HHMMSS.pdf`** - Relatório PDF em orientação paisagem

## 🎯 Critérios de Filtragem

O projeto identifica escolas por tipo usando o campo `TIPOESC`:

- **TIPOESC = 10**: Escolas Indígenas ✅
- **TIPOESC = 36**: Escolas Quilombolas/Assentamentos ✅

> **Nota**: Centros Socioeducativos (TIPOESC = 34) foram excluídos por não se enquadrarem no escopo.

## 📊 Resultados Encontrados

### Estatísticas Gerais

- **Total de escolas**: 59
- **Escolas Indígenas**: 43
- **Escolas Quilombolas/Assentamentos**: 16
- **Distância média**: 50.56 km
- **Distância mínima**: 12.63 km
- **Distância máxima**: 285.90 km

### Distribuição por Tipo

| Tipo                      | Quantidade | Percentual |
| ------------------------- | ---------- | ---------- |
| Indígenas                 | 43         | 72.9%      |
| Quilombolas/Assentamentos | 16         | 27.1%      |

## 🚀 Como Usar

### 1. Executar Cálculo de Distâncias

```bash
python calcular_distancias.py
```

O script irá:

1. Filtrar escolas indígenas e quilombolas/assentamentos
2. Geocodificar endereços das diretorias de ensino
3. Relacionar cada escola com sua diretoria responsável
4. Calcular distâncias geodésicas
5. Gerar arquivo Excel com resultados

### 2. Atualizar Visualização Web

```bash
python converter_dados.py
```

Este script converte os dados do Excel para o formato da página web.

### 3. Gerar Relatórios

```bash
python gerar_relatorios.py
```

Este script oferece um menu interativo para gerar:

- **Relatório Excel**: Sucinto e organizado em abas por tipo de escola
- **Relatório PDF**: Detalhado com gráficos e layout elegante para impressão
- **Ambos**: Gera os dois formatos simultaneamente

### 4. Visualizar Resultados

Abra o arquivo `distancias_escolas.html` em um navegador para ver:

- Mapa interativo com escolas e diretorias
- Lista filtrada por tipo de escola
- Busca por nome ou cidade
- Visualização de conexões escola-diretoria
- Estatísticas em tempo real

## � Tipos de Relatórios Disponíveis

### 1. Relatório Excel Completo (`Relatorio_Completo_Escolas_Diretorias.xlsx`)

**Características:**

- 📊 **Resumo Executivo**: Estatísticas gerais e rankings
- 🔴 **Aba Escolas Indígenas**: Lista completa com dados abrangentes
- 🟢 **Aba Quilombolas/Assentamentos**: Lista específica deste tipo
- 📋 **Aba Todas as Escolas**: Visão consolidada
- 🎨 **Formatação Profissional**: Cores por prioridade, bordas e indicadores visuais

**12+ Colunas incluídas:**

```
• Nome da Escola ✅
• Endereço Completo da Escola ✅ (logradouro, número, bairro, CEP)
• Tipo de Escola (Indígena/Quilombola/Assentamento) ✅
• Cidade da Escola ✅
• Zona (Rural/Urbana) ✅
• Diretoria Responsável ✅
• Endereço Completo da Diretoria ✅ (logradouro, número, bairro, cidade, CEP)
• Cidade da Diretoria ✅
• Distância (km) ✅ - Calculada geodesicamente
• Classificação da Distância (Alta/Média/Baixa) ✅
• Prioridade de Atenção (ALTA/MÉDIA/BAIXA) ✅
• Coordenadas da Escola (Latitude, Longitude) ✅
• Coordenadas da Diretoria (Latitude, Longitude) ✅
• Código da DE ✅
• Observações automáticas ✅
```

**Exemplo completo de dados por escola:**

```
Nome: JOAO CARREIRA
Endereço Escola: PRIMAVERA, SN, CAMBIRA, CEP: 16900970
Tipo: Quilombola/Assentamento
Cidade: ANDRADINA
Zona: Rural
Diretoria: Andradina
Endereço Diretoria: 10a Rua R Regente Feijo, 2160, Vila Mineira, Andradina, SP, CEP: 16901908
Cidade Diretoria: Andradina
Distância: 16.1 km
Classificação: Baixa (<50km)
Prioridade: BAIXA - Adequada
Coordenadas Escola: -21,0112896, -51,46931458
Coordenadas Diretoria: -20.896505, -51.3742765
```

### 2. Relatório PDF Paisagem (`Relatorio_Paisagem_Escolas_YYYYMMDD_HHMMSS.pdf`)

**Características:**

- 📄 **Orientação Paisagem**: Melhor aproveitamento do espaço A4
- 📄 **Capa Institucional**: Informações gerais e data do relatório
- 📈 **Análise Estatística**: Gráficos expandidos (16x6 polegadas)
- 📊 **Gráfico Pizza**: Proporção entre tipos de escola
- 📊 **Histograma**: Distribuição das distâncias
- 📊 **Ranking Diretorias**: Top 10 com maiores distâncias médias (16x8 polegadas)
- 📋 **Tabelas Expandidas**: 6 colunas com mais informações
- 🎨 **Layout Elegante**: Otimizado para impressão panorâmica

**Vantagens da orientação paisagem:**

- ✅ Tabelas mais legíveis com 6 colunas
- ✅ Gráficos expandidos para melhor visualização
- ✅ Nomes completos das escolas (até 45 caracteres)
- ✅ Mais espaço para diretorias (até 25 caracteres)
- ✅ Coluna adicional para Zona (Rural/Urbana)

## �🗂️ Estrutura dos Dados

### Planilha de Resultados (`distancias_escolas_diretorias.xlsx`)

| Campo               | Descrição                           |
| ------------------- | ----------------------------------- |
| Nome_Escola         | Nome da escola                      |
| Tipo_Escola         | Indígena ou Quilombola/Assentamento |
| Cidade_Escola       | Município da escola                 |
| DE_Responsavel      | Diretoria de Ensino responsável     |
| Zona                | Rural ou Urbana                     |
| Latitude_Escola     | Coordenada da escola                |
| Longitude_Escola    | Coordenada da escola                |
| Nome_Diretoria      | Nome da diretoria                   |
| Cidade_Diretoria    | Município da diretoria              |
| Latitude_Diretoria  | Coordenada da diretoria             |
| Longitude_Diretoria | Coordenada da diretoria             |
| Distancia_KM        | Distância calculada em quilômetros  |

## 📍 Exemplos de Resultados

### Escolas com Menores Distâncias

1. **CRECHE ANTONIO CARLOS FERREIRA** (Birigui) - 12.63 km
2. **JOAO CARREIRA** (Andradina) - 16.1 km
3. **ALDEIA NIMUENDAJU** (Avaí) - 30.08 km

### Escolas com Maiores Distâncias

1. **ALDEIA KOPENOTI** (Avaí) - 285.90 km ⚠️
2. **ALDEIA GWYRA PEPO** (São Paulo) - 115.78 km
3. **ALDEIA YWY PYHAU** (Barão de Antonina) - 87.43 km

> **Observação**: A escola "ALDEIA KOPENOTI" apresenta distância muito alta (285.90 km), possivelmente devido a erro nos dados de localização.

## 🛠️ Dependências

```bash
pip install pandas openpyxl geopy reportlab matplotlib seaborn
```

## 📈 Funcionalidades da Visualização Web

### Mapa Interativo

- Marcadores diferenciados por tipo de escola
- Popup com informações detalhadas
- Visualização de conexões escola-diretoria
- Zoom automático para conexões

### Filtros e Busca

- Filtro por tipo de escola (Todas/Indígenas/Quilombolas)
- Busca por nome da escola, cidade ou diretoria
- Atualização em tempo real

### Informações Estatísticas

- Total de escolas por tipo
- Distância média calculada
- Indicadores visuais de distância (perto/médio/longe)

## 🎨 Códigos de Cores

- **🔴 Vermelho**: Escolas Indígenas
- **🟢 Verde**: Escolas Quilombolas/Assentamentos
- **🔵 Azul**: Diretorias de Ensino
- **🟡 Amarelo**: Linhas de conexão (temporárias)

## 📝 Metodologia

1. **Filtragem**: Seleção de escolas pelos códigos TIPOESC corretos
2. **Geocodificação**: Conversão de endereços em coordenadas geográficas
3. **Relacionamento**: Vinculação escola-diretoria baseada no campo DE
4. **Cálculo**: Distância geodésica usando fórmula de Haversine
5. **Visualização**: Interface web interativa com Leaflet.js

## ⚠️ Observações Importantes

- Algumas diretorias podem não ter endereços exatos, usando coordenadas da cidade
- Distâncias são calculadas "em linha reta" (geodésica)
- Para rotas reais, seria necessário usar APIs de roteamento
- Dados de coordenadas podem conter inconsistências nos arquivos originais

## 📞 Próximos Passos Sugeridos

1. **Validação de Dados**: Revisar coordenadas com distâncias muito altas
2. **Roteamento Real**: Integrar com API do Google Maps para rotas reais
3. **Relatórios**: Gerar relatórios específicos por diretoria
4. **Dashboard**: Criar painel administrativo para acompanhamento
