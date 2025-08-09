# RELATÓRIO EXCEL - VEÍCULOS POR DIRETORIA

## 📊 Resumo Executivo

**Arquivo gerado:** `relatorios/excel/Relatorio_Veiculos_por_Diretoria_20250808_120945.xlsx`

### 🎯 Objetivo

Análise detalhada da distribuição de veículos pelas **19 diretorias** que atendem escolas **indígenas**, **quilombolas** e **assentamentos**.

### 📈 Dados Principais

- **Total de Diretorias Analisadas:** 19
- **Total de Veículos Distribuídos:** 174 (note: pequena diferença devido ao arredondamento na distribuição proporcional)
- **Total de Escolas Atendidas:** 63
  - 43 Escolas Indígenas
  - 20 Escolas Quilombolas/Assentamento

---

## 📋 Estrutura do Relatório (4 Abas)

### 🟦 **Aba 1: "Resumo Executivo"**

- Estatísticas gerais do sistema
- Distribuição de veículos
- Prioridades logísticas
- Informações de contexto

### 🟩 **Aba 2: "Veículos por Diretoria"** ⭐ **PRINCIPAL**

Tabela completa com **todas as 19 diretorias** contendo:

| Coluna                               | Descrição                                         |
| ------------------------------------ | ------------------------------------------------- |
| **Diretoria**                        | Nome da Diretoria de Ensino                       |
| **Total Veículos**                   | Quantidade de veículos alocados                   |
| **Total Escolas**                    | Número total de escolas atendidas                 |
| **Escolas Indígenas**                | Quantidade de escolas indígenas                   |
| **Escolas Quilombolas/Assentamento** | Quantidade de escolas quilombolas e assentamentos |
| **Escolas Rurais**                   | Escolas em zona rural                             |
| **Escolas Urbanas**                  | Escolas em zona urbana                            |
| **Distância Média (km)**             | Média das distâncias das escolas                  |
| **Distância Máxima (km)**            | Maior distância entre as escolas                  |
| **Veículos/Escola**                  | Proporção de veículos por escola                  |
| **Prioridade Logística**             | Classificação: ALTA/MÉDIA/BAIXA                   |
| **Código DE**                        | Código oficial da Diretoria                       |

### 🟨 **Aba 3: "Diretorias Indígenas"**

Foco específico nas **12 diretorias** que atendem escolas indígenas:

- Ordenadas por quantidade de escolas indígenas
- Percentual de escolas indígenas por diretoria
- Análise de veículos destinados a atendimento indígena

### 🟪 **Aba 4: "Diretorias Quilombolas"**

Foco específico nas **10 diretorias** que atendem escolas quilombolas e assentamentos:

- Ordenadas por quantidade de escolas quilombolas/assentamento
- Percentual de escolas quilombolas por diretoria
- Análise de veículos destinados a atendimento quilombola

---

## 🏆 TOP 5 Diretorias com Mais Veículos

| Posição | Diretoria                   | Veículos | Escolas |
| ------- | --------------------------- | -------- | ------- |
| 1º      | **Mirante do Paranapanema** | 27       | 10      |
| 2º      | **Registro**                | 27       | 10      |
| 3º      | **São Vicente**             | 25       | 9       |
| 4º      | **Miracatu**                | 22       | 8       |
| 5º      | **Itararé**                 | 14       | 5       |

---

## 🎯 Classificação de Prioridades

O sistema classifica automaticamente as diretorias em:

### 🔴 **ALTA Prioridade**

- Distância média ≥ 60 km **E** ≥ 3 escolas
- _Observação: Nenhuma diretoria atingiu esse critério no atual dataset_

### 🟡 **MÉDIA Prioridade**

- Distância média ≥ 40 km **OU** ≥ 5 escolas
- Foco em diretorias com desafios logísticos significativos

### 🟢 **BAIXA Prioridade**

- Demais diretorias
- Menor complexidade logística

---

## 📊 Destaques da Análise

### 🏛️ **Escolas Indígenas**

- **12 diretorias** atendem escolas indígenas
- Distribuição geográfica ampla
- Necessidades específicas de transporte

### 🏡 **Escolas Quilombolas/Assentamento**

- **10 diretorias** atendem escolas quilombolas e assentamentos
- Muitas em zonas rurais com distâncias consideráveis
- Importante foco na equidade de acesso

### 🚗 **Distribuição de Veículos**

- Média de **9,2 veículos** por diretoria
- Distribuição proporcional ao número de escolas
- Consideração das distâncias para otimização logística

---

## 💡 **Como Usar Este Relatório**

1. **Visão Geral:** Comece pela aba "Resumo Executivo"
2. **Análise Completa:** Use a aba "Veículos por Diretoria" para visão geral
3. **Foco Específico:** Use as abas "Diretorias Indígenas" ou "Diretorias Quilombolas" conforme necessidade
4. **Planejamento:** Use a coluna "Prioridade Logística" para tomada de decisões
5. **Otimização:** Analise as colunas de distância para otimização de rotas

---

## 🔄 **Atualizações**

Para gerar uma versão atualizada deste relatório:

```bash
python scripts/geracao/gerar_relatorio_veiculos_diretorias.py
```

O relatório é gerado automaticamente com timestamp para controle de versões.

---

**Gerado em:** 08/08/2025 12:09:45  
**Sistema:** Gestão de Escolas Indígenas, Quilombolas e Assentamentos  
**Versão:** 1.0
