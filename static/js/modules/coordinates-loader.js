// ===================================================
// COORDENADAS GLOBAIS PARA COMPATIBILIDADE
// ===================================================

// Função para carregar coordenadas dinamicamente
async function loadCoordinates() {
  try {
    // Carregar módulo simples
    const simplesModule = await import('../coordenadas_simples.js');
    if (simplesModule.mapasp_simples) {
      let coordsSimples = {};
      window.mapasp_simples = simplesModule.mapasp_simples(coordsSimples);
      console.log("✅ Coordenadas simples carregadas");
    }
    
    // Carregar módulo completo
    const completoModule = await import('../coordenadas_completa.js');
    if (completoModule.mapasp_completo) {
      let coordsCompleto = {};
      window.mapasp_completo = completoModule.mapasp_completo(coordsCompleto);
      console.log("✅ Coordenadas completas carregadas");
    }
    
    // Notificar que as coordenadas estão prontas
    window.coordinatesReady = true;
    document.dispatchEvent(new Event('coordinatesLoaded'));
    
  } catch (error) {
    console.error("❌ Erro ao carregar coordenadas:", error);
    window.coordinatesReady = false;
  }
}

// Carregar coordenadas quando o script for carregado
loadCoordinates();
