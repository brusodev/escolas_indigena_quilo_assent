# RELATÓRIO EXCEL - VEÍCULOS POR DIRETORIA (DADOS REAIS)

## ✅ **Arquivo Corrigido Gerado**

**Relatório com dados REAIS:** `relatorios/excel/Relatorio_Veiculos_por_Diretoria_20250808_121805.xlsx`

---

## 📊 **Estatísticas Reais dos Dados**

### 🎯 **Correspondência de Dados**

- **Taxa de correspondência:** 100% ✅
- **Total de diretorias analisadas:** 19
- **Todas as diretorias encontradas** nos dados reais de veículos

### 🚗 **Distribuição Real de Veículos**

- **Total de veículos REAIS:** 28 veículos
- **Veículos S1 (pequenos):** 3 veículos
- **Veículos S2 (médios):** 25 veículos
- **Veículos S2 4x4 (terreno):** 0 veículos

### 🏫 **Escolas Atendidas**

- **Total de escolas:** 63
- **Escolas indígenas:** 43
- **Escolas quilombolas/assentamento:** 20
- **Diretorias com escolas indígenas:** 12
- **Diretorias com escolas quilombolas/assentamento:** 10

---

## 🏆 **Top 5 Diretorias com Mais Veículos (DADOS REAIS)**

| Posição | Diretoria                 | Veículos Reais | Escolas |
| ------- | ------------------------- | -------------- | ------- |
| 1º      | **Andradina**             | 2              | 1       |
| 2º      | **Avare**                 | 2              | 1       |
| 3º      | **Lins**                  | 2              | 1       |
| 4º      | **São Bernardo do Campo** | 2              | 1       |
| 5º      | **Penápolis**             | 2              | 1       |

---

## 📋 **Distribuição Detalhada por Diretoria**

### 🚗 **Diretorias com 2 Veículos (7 diretorias)**

- **Andradina:** 2 veículos (1 S1 + 1 S2)
- **Avare:** 2 veículos (2 S2)
- **Lins:** 2 veículos (2 S2)
- **Penápolis:** 2 veículos (1 S1 + 1 S2)
- **Registro:** 2 veículos (2 S2)
- **Santo Anastácio:** 2 veículos (1 S1 + 1 S2)
- **Santos:** 2 veículos (2 S2)
- **São Bernardo do Campo:** 2 veículos (1 S1 + 1 S2)
- **São Vicente:** 2 veículos (2 S2)

### 🚙 **Diretorias com 1 Veículo (10 diretorias)**

- **Apiaí:** 1 veículo (1 S2)
- **Bauru:** 1 veículo (1 S2)
- **Caraguatatuba:** 1 veículo (1 S2)
- **Itapeva:** 1 veículo (1 S2)
- **Itararé:** 1 veículo (1 S2)
- **Miracatu:** 1 veículo (1 S2)
- **Mirante do Paranapanema:** 1 veículo (1 S2)
- **Norte 1:** 1 veículo (1 S2)
- **Sul 3:** 1 veículo (1 S2)
- **Tupã:** 1 veículo (1 S2)

---

## 💡 **Principais Insights dos Dados Reais**

### 🔍 **Análise de Eficiência**

- **Média de veículos por diretoria:** 1,5 veículos
- **Média de escolas por diretoria:** 3,3 escolas
- **Proporção média veículos/escola:** 0,45

### ⚠️ **Desafios Identificados**

- **Baixa proporção de veículos por escola** (menos de 1 veículo por 2 escolas)
- **Concentração em veículos S2** (89% do total)
- **Ausência de veículos 4x4** para terrenos difíceis

### 🎯 **Diretorias de Maior Demanda**

Baseado na combinação de número de escolas e distâncias:

1. **Mirante do Paranapanema** - 10 escolas, 1 veículo
2. **Registro** - 10 escolas, 2 veículos
3. **São Vicente** - 9 escolas, 2 veículos

---

## 📈 **Recomendações Baseadas nos Dados Reais**

### 🚨 **Prioridade ALTA**

- **Mirante do Paranapanema**: 10 escolas com apenas 1 veículo
- Necessita aumento significativo da frota

### 🟡 **Prioridade MÉDIA**

- **Registro**: 10 escolas com 2 veículos
- **São Vicente**: 9 escolas com 2 veículos
- Considerar aumento moderado da frota

### ✅ **Situação Adequada**

- Diretorias com 1-2 escolas e proporção similar de veículos

---

## 📁 **Estrutura do Relatório Excel**

### 📊 **4 Abas Principais:**

1. **"Resumo Executivo"** - Estatísticas gerais com dados reais
2. **"Veículos por Diretoria"** - Tabela principal com todos os tipos de veículos
3. **"Diretorias Indígenas"** - Foco nas 12 diretorias com escolas indígenas
4. **"Diretorias Quilombolas"** - Foco nas 10 diretorias com escolas quilombolas/assentamento

### 🔢 **Novas Colunas Incluídas:**

- **Veículos S1** (pequenos)
- **Veículos S2** (médios)
- **Veículos S2 4x4** (terreno)
- **Proporção real veículos/escola**

---

## 🔄 **Como Atualizar o Relatório**

Para gerar nova versão com dados atualizados:

```bash
python scripts/geracao/gerar_relatorio_veiculos_diretorias.py
```

Para verificar correspondência de dados:

```bash
python scripts/diagnosticar_correspondencia_veiculos.py
```

---

**Gerado em:** 08/08/2025 12:18:05  
**Fonte de dados:** `dados/json/dados_veiculos_corrigidos.json` (dados reais)  
**Sistema:** Gestão de Escolas Indígenas, Quilombolas e Assentamentos  
**Versão:** 2.0 (com dados reais)
