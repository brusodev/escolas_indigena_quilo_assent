# 📁 ESTRUTURA ORGANIZADA DO PROJETO

## Sistema de Gestão de Escolas Indígenas, Quilombolas e Assentamentos

🗂️ **Organização criada em**: 08/08/2025

---

## 📂 **ESTRUTURA DE PASTAS**

### 🏠 **Raiz do Projeto**

```
escolas_indigina_quilo_assent/
├── main.py                     # Script principal do projeto
├── ESTRUTURA_PROJETO.md        # Este arquivo (guia da estrutura)
├── .git/                       # Controle de versão Git
├── .venv/                      # Ambiente virtual Python
├── backup_20250808_092534/     # Backup automático
└── [pastas organizadas abaixo]
```

---

## 📊 **dados/** - Fontes de Dados Centralizadas

```
dados/
├── excel/                      # Planilhas Excel (.xlsx)
│   ├── distancias_escolas_diretorias_completo_63_corrigido.xlsx  # 🎯 FONTE PRINCIPAL (63 escolas)
│   ├── diretorias_com_coordenadas.xlsx
│   ├── diretorias_ensino_completo.xlsx
│   ├── GEP.xlsx
│   ├── QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx
│   └── [outros arquivos Excel...]
├── json/                       # Dados estruturados JSON
│   ├── config_sistema.json     # 🔧 Configuração central do sistema
│   ├── dados_veiculos_diretorias.json  # 🚗 Dados de veículos (172 total)
│   ├── dados_escolas_atualizados.json
│   ├── comparacao_dashboard_excel.json
│   └── [outros arquivos JSON...]
└── ENDERECO_ESCOLAS_062025 (1).csv  # Dados originais CSV
```

---

## 🛠️ **scripts/** - Scripts Python Organizados

```
scripts/
├── geracao/                    # Scripts de Geração de Relatórios
│   ├── gerar_relatorio_excel.py     # Gera relatórios Excel
│   ├── gerar_relatorio_pdf.py       # Gera relatórios PDF
│   ├── gerar_relatorios.py          # Gerador geral
│   ├── gerar_graficos_frota.py      # Gráficos de frota
│   └── gerar_dados_embebidos.py     # Dados para dashboard
├── validacao/                  # Scripts de Validação
│   ├── verificar_dados.py           # Validação geral
│   ├── verificar_dashboard_completo.py
│   ├── verificar_excel.py
│   ├── verificar_veiculos_detalhado.py
│   └── [outros verificadores...]
├── correcao/                   # Scripts de Correção
│   ├── corrigir_distancias.py       # Correção com Haversine
│   ├── corrigir_dados_escolas.py
│   ├── corrigir_coordenadas.py
│   └── [outros corretores...]
├── atualizar_relatorios_completos.py  # 🚀 SCRIPT PRINCIPAL - Atualização
├── atualizar_dashboard_completo.py
├── repositorio_central.py            # 🔍 VALIDAÇÃO CENTRAL
├── resumo_executivo_centralizacao.py
├── calcular_distancias.py
├── menu_integrado.py
└── [outros scripts diversos...]
```

---

## 📋 **relatorios/** - Relatórios Gerados

```
relatorios/
├── excel/                      # Relatórios Excel gerados
│   ├── Relatorio_Completo_Atualizado_20250807_213305.xlsx
│   ├── Relatorio_Completo_Distancias_Haversine.xlsx
│   ├── Analise_Integrada_Escolas_Frota_Supervisao.xlsx
│   └── [outros relatórios Excel...]
├── pdf/                        # Relatórios PDF gerados
│   ├── Relatorio_Paisagem_Escolas_20250808_091826.pdf  # 📄 Mais recente
│   ├── Relatorio_Detalhado_Escolas_20250807.pdf
│   └── [outros relatórios PDF...]
└── graficos/                   # Gráficos e visualizações
    ├── Graficos_Analise_Frota.png
    ├── Mapa_Calor_Necessidade_Veiculos.png
    └── [outros gráficos...]
```

---

## 🌐 **dashboard/** - Interface Web

```
dashboard/
├── dashboard_integrado.html           # 🎯 DASHBOARD PRINCIPAL (63 escolas)
├── dashboard_integrado_backup.html    # Backup do dashboard
├── distancias_escolas.html           # Visualização de distâncias
├── index.html                        # Página inicial
├── dados_embebidos.js               # Dados JavaScript embebidos
└── teste_sao_vicente.js            # Scripts de teste
```

---

## 📚 **documentacao/** - Documentação Completa

```
documentacao/
├── DOCUMENTACAO_COMPLETA.md           # 📖 DOCUMENTAÇÃO PRINCIPAL
├── DOCUMENTACAO_VERSOES.md           # Histórico de versões
├── GUIA_RAPIDO.md                    # Guia rápido de uso
├── README.md                         # Readme do projeto
├── relatorio_bruno.md               # Relatório específico
├── RELATORIO_FINAL_ATUALIZACAO_20250807.md
├── Metodologia_Calculo_Distancias_Haversine.txt  # 📐 Metodologia técnica
├── Metodologia_Relatorio_PDF.txt
├── relatorio_final_completo.txt
└── [outros arquivos de documentação...]
```

---

## 🔧 **ARQUIVOS PRINCIPAIS DE EXECUÇÃO**

### 📊 **Para Gerar Relatórios Atualizados:**

```bash
# No diretório raiz do projeto:
python scripts/atualizar_relatorios_completos.py
```

### 🔍 **Para Validar Integridade do Sistema:**

```bash
python scripts/repositorio_central.py
```

### 🌐 **Para Acessar Dashboard:**

```
Abrir: dashboard/dashboard_integrado.html
```

### 📋 **Para Visualizar Documentação:**

```
Ler: documentacao/DOCUMENTACAO_COMPLETA.md
```

---

## ⭐ **ARQUIVOS CRÍTICOS - NÃO MOVER**

### 🎯 **Fontes de Dados Principais:**

- `dados/excel/distancias_escolas_diretorias_completo_63_corrigido.xlsx`
- `dados/json/config_sistema.json`
- `dados/json/dados_veiculos_diretorias.json`

### 🚀 **Scripts Essenciais:**

- `scripts/atualizar_relatorios_completos.py`
- `scripts/repositorio_central.py`
- `main.py`

### 🌐 **Dashboard Principal:**

- `dashboard/dashboard_integrado.html`

### 📚 **Documentação Central:**

- `documentacao/DOCUMENTACAO_COMPLETA.md`

---

## 🎯 **BENEFÍCIOS DA ORGANIZAÇÃO**

✅ **Facilidade de Navegação**: Arquivos organizados por função  
✅ **Manutenção Simplificada**: Cada tipo de arquivo em sua pasta  
✅ **Backup Organizado**: Estrutura clara para backups  
✅ **Desenvolvimento Ágil**: Localização rápida de componentes  
✅ **Documentação Centralizada**: Informações em local único  
✅ **Escalabilidade**: Estrutura preparada para crescimento

---

## 🔄 **VERSIONAMENTO**

📅 **Criação**: 08/08/2025  
🎯 **Objetivo**: Organizar 100+ arquivos do projeto  
✅ **Status**: Estrutura organizada e funcional  
🚀 **Próximo**: Manter organização em novas adições

---

_📋 Estrutura criada automaticamente pelo sistema de organização_  
_🔧 Mantida sincronizada com o repositório central_
