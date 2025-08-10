// ===================================================
// DASHBOARD PRINCIPAL - VERSÃO MODULAR
// ===================================================

// Função principal de inicialização
async function initializeDashboard() {
  try {
    console.log("🚀 Inicializando dashboard modular...");
    
    // 1. Carregar dados
    await window.dataModule.loadSchoolsData();
    await window.dataModule.loadVehicleData();
    
    // 2. Atualizar interface
    window.uiModule.calculateStats();
    window.uiModule.updateLegendCounts();
    
    // 3. Inicializar componentes
    window.mapModule.initializeMaps();
    window.uiModule.generateSchoolList();
    window.chartsModule.generateCharts();
    
    // 4. Configurar eventos
    window.eventsModule.setupEventListeners();
    
    console.log("✅ Dashboard inicializado com sucesso!");
    
  } catch (error) {
    console.error("❌ Erro ao inicializar dashboard:", error);
  }
}

// Aguardar carregamento do DOM
document.addEventListener('DOMContentLoaded', initializeDashboard);

// Exportar função principal
window.dashboard = {
  initialize: initializeDashboard
};

console.log("📜 Dashboard modular carregado!");
