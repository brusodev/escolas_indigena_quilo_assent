# 🎯 INSTRUÇÕES DE USO - DASHBOARD CITEM COMPLETO

## 🚀 Como Usar o Dashboard

### 1. Abrir o Dashboard
- Abra o arquivo `dashboard_citem_completo.html` no navegador
- Certifique-se de que está em um servidor local (não arquivo:// direto)

### 2. Funcionalidades Disponíveis

#### 🗺️ Mapa Interativo
- **5.582 escolas** plotadas com coordenadas precisas
- **Cores diferentes** para cada tipo de escola:
  - 🏫 Regular (azul) - 4.964 escolas
  - 👥 Indígena (marrom) - 43 escolas
  - 🏛️ Quilombola (roxo) - 16 escolas
  - 🚜 Assentamento (verde) - 4 escolas
  - 📚 CEEJA (vermelho) - 43 escolas
  - 🎓 CEL JTO (laranja) - 165 escolas
  - 🏥 Hospitalar (vermelho escuro) - 71 escolas
  - 🏢 Penitenciária (cinza) - 163 escolas
  - 👦 Socioeducativo (violeta) - 113 escolas

#### 🎛️ Filtros por Tipo
- Clique nos botões de filtro para mostrar apenas um tipo
- Filtro "Todas" mostra todas as 5.582 escolas
- Contadores atualizam automaticamente

#### 🔍 Busca Inteligente
- Busque por nome da escola, município ou unidade regional
- Busca funciona dentro do filtro ativo
- Resultados em tempo real

#### 📋 Lista de Escolas
- Até 100 escolas exibidas por vez (performance)
- Clique em uma escola para centralizar no mapa
- Informações completas de cada escola

### 3. Controles do Mapa
- **Tela Cheia**: Expandir mapa para tela inteira
- **Zoom**: Use mouse ou controles do mapa
- **Popup**: Clique em marcador para ver detalhes

### 4. Dados Técnicos
- **Fonte**: Sistema CITEM oficial
- **Coordenadas**: WGS84 com precisão geodésica
- **Atualização**: 11/08/2025
- **Encoding**: UTF-8 com coordenadas decimais brasileiras

## 🔧 Solução de Problemas

### Mapa não carrega
- Verifique conexão com internet (Leaflet CDN)
- Use servidor local (não abra arquivo diretamente)

### Filtros não funcionam
- Verifique console do navegador (F12)
- Certifique-se de que todos os arquivos JS estão carregados

### Performance lenta
- Com 5.582 escolas, o carregamento pode demorar alguns segundos
- Use filtros para reduzir número de marcadores visíveis

## 📊 Estatísticas Importantes
- **Total**: 5.582 escolas mapeadas
- **Cobertura**: 100% com coordenadas válidas
- **Unidades Regionais**: 89 diretorias mapeadas
- **Tipos de Escola**: 10 categorias diferentes

## 🎯 Casos de Uso
1. **Análise Regional**: Filtrar por tipo e ver distribuição geográfica
2. **Planejamento**: Identificar concentrações de escolas especiais
3. **Busca Específica**: Localizar escolas por nome ou município
4. **Visualização**: Compreender rede estadual completa

---
*Dashboard desenvolvido para análise completa do sistema educacional paulista*
