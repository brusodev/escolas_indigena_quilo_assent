// ===================================================
// DASHBOARD PRINCIPAL - VERSÃO CORRIGIDA
// ===================================================

// Variáveis globais
let schoolsData = [];
let vehicleData = null;
let schoolMarkers = [];
let diretoriaMarkers = [];
let connectionLines = [];

// Função principal de inicialização
async function initializeDashboard() {
  try {
    console.log("🚀 Inicializando dashboard corrigido...");
    
    // 1. Carregar dados
    await loadAllData();
    
    // 2. Inicializar mapa
    initializeMap();
    
    // 3. Adicionar marcadores e conexões
    addAllMarkersToMap();
    
    // 4. Atualizar interface
    updateAllInterface();
    
    // 5. Configurar eventos
    setupAllEvents();
    
    console.log("✅ Dashboard inicializado com sucesso!");
    
  } catch (error) {
    console.error("❌ Erro ao inicializar dashboard:", error);
    showErrorMessage("Erro ao carregar o dashboard. Verifique os dados.");
  }
}

// Função para carregar todos os dados
async function loadAllData() {
  try {
    // Carregar dados das escolas
    console.log("📊 Carregando dados das escolas...");
    const schoolsResponse = await fetch("dados/json/dados_escolas_atualizados.json");
    if (!schoolsResponse.ok) throw new Error(`HTTP ${schoolsResponse.status}`);
    schoolsData = await schoolsResponse.json();
    console.log(`✅ ${schoolsData.length} escolas carregadas`);
    
    // Carregar dados de veículos
    console.log("🚗 Carregando dados de veículos...");
    const vehiclesResponse = await fetch("dados_veiculos_diretorias.json");
    if (!vehiclesResponse.ok) throw new Error(`HTTP ${vehiclesResponse.status}`);
    vehicleData = await vehiclesResponse.json();
    console.log(`✅ ${vehicleData.metadata.total_veiculos} veículos carregados`);
    
    // Disponibilizar dados globalmente
    window.dataModule = {
      schoolsData: () => schoolsData,
      vehicleData: () => vehicleData,
      getVehicleDataForDiretoria: (diretoriaName) => {
        if (!vehicleData) return { total: 0, s1: 0, s2: 0, s2_4x4: 0 };
        
        const normalizedName = window.diretoriaMarkersModule?.normalizeDiretoriaName(diretoriaName) || diretoriaName;
        
        for (const [key, data] of Object.entries(vehicleData.diretorias)) {
          const normalizedKey = window.diretoriaMarkersModule?.normalizeDiretoriaName(key) || key;
          if (normalizedKey === normalizedName) {
            return data;
          }
        }
        
        return { total: 0, s1: 0, s2: 0, s2_4x4: 0 };
      }
    };
    
  } catch (error) {
    console.error("❌ Erro ao carregar dados:", error);
    throw error;
  }
}

// Função para inicializar o mapa
function initializeMap() {
  try {
    console.log("🗺️ Inicializando mapa...");
    
    // Criar mapa centrado no estado de São Paulo
    window.map = L.map('map').setView([-23.5431, -46.6291], 7);
    
    // Adicionar camada base
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 18
    }).addTo(window.map);
    
    // Carregar coordenadas do estado se disponível
    if (window.coordinatesModule && window.coordinatesModule.loadCoordinates) {
      window.coordinatesModule.loadCoordinates();
    }
    
    console.log("✅ Mapa inicializado");
    
  } catch (error) {
    console.error("❌ Erro ao inicializar mapa:", error);
    throw error;
  }
}

// Função para adicionar todos os marcadores ao mapa
function addAllMarkersToMap() {
  try {
    console.log("📍 Adicionando marcadores ao mapa...");
    
    if (!window.map || !schoolsData.length) {
      console.warn("⚠️ Mapa ou dados não disponíveis");
      return;
    }
    
    // Adicionar marcadores de escolas
    if (window.schoolMarkersModule) {
      schoolMarkers = window.schoolMarkersModule.addSchoolsToMap(window.map, schoolsData);
      console.log(`✅ ${schoolMarkers.length} marcadores de escolas adicionados`);
    }
    
    // Adicionar marcadores de diretorias
    if (window.diretoriaMarkersModule) {
      diretoriaMarkers = window.diretoriaMarkersModule.addDiretoriasToMap(window.map, schoolsData, vehicleData);
      console.log(`✅ ${diretoriaMarkers.length} marcadores de diretorias adicionados`);
    }
    
    // Adicionar linhas de conexão
    if (window.connectionLinesModule) {
      connectionLines = window.connectionLinesModule.addConnectionLinesToMap(window.map, schoolsData);
      console.log(`✅ ${connectionLines.length} linhas de conexão adicionadas`);
    }
    
  } catch (error) {
    console.error("❌ Erro ao adicionar marcadores:", error);
  }
}

// Função para atualizar toda a interface
function updateAllInterface() {
  try {
    console.log("🔄 Atualizando interface...");
    
    // Atualizar legenda
    if (window.legendModule) {
      window.legendModule.updateCompleteLegend(schoolsData);
    }
    
    // Gerar gráficos
    if (window.chartsModule) {
      window.chartsModule.generateCharts();
    }
    
    // Atualizar lista de escolas
    if (window.filtersModule) {
      window.filtersModule.updateDisplayWithFilters(schoolsData);
    }
    
    console.log("✅ Interface atualizada");
    
  } catch (error) {
    console.error("❌ Erro ao atualizar interface:", error);
  }
}

// Função para configurar todos os eventos
function setupAllEvents() {
  try {
    console.log("⚙️ Configurando eventos...");
    
    // Configurar eventos de filtros
    if (window.filtersModule) {
      window.filtersModule.setupFilterEvents(schoolsData);
    }
    
    // Configurar eventos de mapa
    setupMapEvents();
    
    // Configurar controles de mapa
    setupMapControls();
    
    console.log("✅ Eventos configurados");
    
  } catch (error) {
    console.error("❌ Erro ao configurar eventos:", error);
  }
}

// Função para configurar eventos específicos do mapa
function setupMapEvents() {
  if (!window.map) return;
  
  // Evento de clique no mapa
  window.map.on('click', function(e) {
    console.log(`📍 Clique no mapa: ${e.latlng.lat.toFixed(4)}, ${e.latlng.lng.toFixed(4)}`);
  });
  
  // Evento de zoom
  window.map.on('zoomend', function() {
    const zoom = window.map.getZoom();
    console.log(`🔍 Zoom alterado para: ${zoom}`);
    
    // Ajustar opacidade das linhas baseado no zoom
    if (connectionLines.length > 0) {
      const opacity = zoom > 10 ? 0.8 : zoom > 8 ? 0.6 : 0.4;
      connectionLines.forEach(line => {
        line.setStyle({ opacity: opacity });
      });
    }
  });
}

// Função para configurar controles do mapa
function setupMapControls() {
  // Botão de tela cheia
  const fullscreenBtn = document.getElementById('fullscreen-btn');
  if (fullscreenBtn) {
    fullscreenBtn.addEventListener('click', toggleMapFullscreen);
  }
  
  // Botão de coordenadas
  const coordBtn = document.getElementById('toggle-coordinates-btn');
  if (coordBtn) {
    coordBtn.addEventListener('click', toggleCoordinatesDisplay);
  }
}

// Função para alternar tela cheia do mapa
function toggleMapFullscreen() {
  const overlay = document.getElementById('map-fullscreen-overlay');
  if (!overlay) return;
  
  if (overlay.classList.contains('hidden')) {
    // Entrar em tela cheia
    overlay.classList.remove('hidden');
    
    // Criar mapa de tela cheia se não existir
    if (!window.fullscreenMap) {
      const container = document.getElementById('map-fullscreen-container');
      window.fullscreenMap = L.map(container).setView(window.map.getCenter(), window.map.getZoom());
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18
      }).addTo(window.fullscreenMap);
      
      // Copiar marcadores para o mapa de tela cheia
      if (window.schoolMarkersModule) {
        window.schoolMarkersModule.addSchoolsToMap(window.fullscreenMap, schoolsData);
      }
      if (window.diretoriaMarkersModule) {
        window.diretoriaMarkersModule.addDiretoriasToMap(window.fullscreenMap, schoolsData, vehicleData);
      }
    }
    
    setTimeout(() => window.fullscreenMap.invalidateSize(), 100);
  } else {
    // Sair da tela cheia
    overlay.classList.add('hidden');
  }
}

// Função para alternar exibição de coordenadas
function toggleCoordinatesDisplay() {
  if (window.coordinatesModule && window.coordinatesModule.toggleCoordinates) {
    window.coordinatesModule.toggleCoordinates();
  }
}

// Função para mostrar mensagem de erro
function showErrorMessage(message) {
  const errorDiv = document.createElement('div');
  errorDiv.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #e74c3c;
    color: white;
    padding: 15px 20px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    z-index: 10000;
    max-width: 400px;
  `;
  errorDiv.innerHTML = `
    <strong>❌ Erro</strong><br>
    ${message}
  `;
  
  document.body.appendChild(errorDiv);
  
  setTimeout(() => {
    if (errorDiv.parentNode) {
      errorDiv.parentNode.removeChild(errorDiv);
    }
  }, 5000);
}

// Configurar eventos de saída da tela cheia
document.addEventListener('DOMContentLoaded', function() {
  const exitBtn = document.getElementById('exit-fullscreen-btn');
  if (exitBtn) {
    exitBtn.addEventListener('click', () => {
      const overlay = document.getElementById('map-fullscreen-overlay');
      if (overlay) overlay.classList.add('hidden');
    });
  }
});

// Aguardar carregamento do DOM
document.addEventListener('DOMContentLoaded', initializeDashboard);

// Exportar função principal
window.dashboard = {
  initialize: initializeDashboard,
  schoolsData: () => schoolsData,
  vehicleData: () => vehicleData
};

console.log("📜 Dashboard principal corrigido carregado!");
