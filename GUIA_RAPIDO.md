# 🚀 Guia Rápido de Uso

## Executar Todo o Processo (Primeira Vez)

### 1. Calcular Distâncias

```bash
python calcular_distancias.py
```

- ✅ Filtra escolas indígenas e quilombolas
- ✅ Geocodifica diretorias de ensino
- ✅ Calcula distâncias geodésicas
- ✅ Gera `distancias_escolas_diretorias.xlsx`

### 2. Gerar Relatórios

```bash
python gerar_relatorios.py
```

- 📊 Escolha Excel sucinto ou PDF detalhado
- 🎨 Relatórios com formatação profissional
- 📋 Dados organizados e analisados

### 3. Visualizar Online

```bash
python converter_dados.py
```

- 🌐 Atualiza página web interativa
- 🗺️ Abra `distancias_escolas.html` no navegador

## Estrutura Final dos Arquivos

```
📁 Projeto/
├── 📊 DADOS ORIGINAIS
│   ├── ENDERECO_ESCOLAS_062025 (1).csv
│   └── diretorias_ensino_completo.xlsx
│
├── 🔧 SCRIPTS
│   ├── calcular_distancias.py      # Principal - calcula tudo
│   ├── gerar_relatorios.py         # Menu para relatórios
│   ├── gerar_relatorio_excel.py    # Gera Excel
│   ├── gerar_relatorio_pdf.py      # Gera PDF
│   └── converter_dados.py          # Atualiza web
│
├── 🌐 VISUALIZAÇÃO WEB
│   ├── index.html                  # Mapa original (42 escolas)
│   └── distancias_escolas.html     # Mapa completo (59 escolas)
│
├── 📋 DADOS PROCESSADOS
│   ├── distancias_escolas_diretorias.xlsx      # Dados brutos
│   └── diretorias_com_coordenadas.xlsx         # Coordenadas
│
└── 📊 RELATÓRIOS FINAIS
    ├── Relatorio_Sucinto_Escolas_Diretorias.xlsx    # Excel organizado
    └── Relatorio_Detalhado_Escolas_20250807.pdf     # PDF elegante
```

## 📊 O que cada relatório contém:

### Excel Sucinto

- ✅ Planilha de resumo executivo
- ✅ Dados separados por tipo (Indígenas/Quilombolas)
- ✅ Formatação com cores e indicadores
- ✅ Observações automáticas (próxima/distante)

### PDF Detalhado

- ✅ Capa institucional com estatísticas
- ✅ Gráficos: pizza, histograma, rankings
- ✅ Tabelas formatadas por categoria
- ✅ Layout pronto para impressão/apresentação

## 🎯 Resultados Principais

**📊 Total encontrado: 59 escolas**

- 🔴 43 Escolas Indígenas (72.9%)
- 🟢 16 Escolas Quilombolas/Assentamentos (27.1%)

**📏 Distâncias:**

- ⭐ Média: 50.56 km
- 📍 Mínima: 12.63 km
- ⚠️ Máxima: 285.90 km

**🏆 Destaques:**

- 15 escolas com distância < 30 km (próximas)
- 8 escolas com distância > 100 km (requerem atenção)
- Distribuição por 45 diretorias de ensino diferentes

## 💡 Dicas de Uso

1. **Para análise rápida**: Use o Excel sucinto
2. **Para apresentações**: Use o PDF detalhado
3. **Para exploração interativa**: Use a página web
4. **Para dados brutos**: Use o arquivo principal Excel

## 🔄 Atualizar Dados

Quando receber novos dados:

1. Substitua os arquivos CSV/Excel originais
2. Execute novamente `calcular_distancias.py`
3. Gere novos relatórios com `gerar_relatorios.py`
4. Atualize a web com `converter_dados.py`
