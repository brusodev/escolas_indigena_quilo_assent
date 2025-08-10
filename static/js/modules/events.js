// ===================================================
// MÓDULO: EVENT LISTENERS E FILTROS
// ===================================================

function setupEventListeners() {
  // Filtros de escola
  const filterButtons = document.querySelectorAll('.filter-btn');
  filterButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      filterButtons.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      const filter = this.getAttribute('data-filter');
      filterSchools(filter);
    });
  });

  // Campo de busca
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      const searchTerm = this.value.toLowerCase();
      filterSchoolsBySearch(searchTerm);
    });
  }

  // Controle de tela cheia
  const fullscreenBtn = document.getElementById('fullscreen-btn');
  const exitFullscreenBtn = document.getElementById('exit-fullscreen-btn');
  const fullscreenOverlay = document.getElementById('map-fullscreen-overlay');

  if (fullscreenBtn) {
    fullscreenBtn.addEventListener('click', function() {
      if (fullscreenOverlay) {
        fullscreenOverlay.classList.remove('hidden');
        window.mapModule.initializeFullscreenMap();
      }
    });
  }

  // Botão para alternar coordenadas
  const toggleCoordinatesBtn = document.getElementById('toggle-coordinates-btn');
  if (toggleCoordinatesBtn) {
    toggleCoordinatesBtn.addEventListener('click', function() {
      if (window.mapModule && window.mapModule.toggleCoordinates) {
        window.mapModule.toggleCoordinates();
      }
    });
  }

  if (exitFullscreenBtn) {
    exitFullscreenBtn.addEventListener('click', function() {
      if (fullscreenOverlay) {
        fullscreenOverlay.classList.add('hidden');
      }
    });
  }

  console.log("🎛️ Event listeners configurados");
}

function filterSchools(filter) {
  const schoolItems = document.querySelectorAll('.school-item');
  
  schoolItems.forEach(item => {
    let show = false;
    
    switch(filter) {
      case 'all':
        show = true;
        break;
      case 'indigena':
        show = item.classList.contains('indigena');
        break;
      case 'quilombola':
        show = item.classList.contains('quilombola');
        break;
      case 'priority-high':
        show = item.classList.contains('priority-high');
        break;
    }
    
    item.style.display = show ? 'block' : 'none';
  });
  
  console.log(`🔍 Filtro aplicado: ${filter}`);
}

function filterSchoolsBySearch(searchTerm) {
  const schoolItems = document.querySelectorAll('.school-item');
  
  schoolItems.forEach(item => {
    const text = item.textContent.toLowerCase();
    const show = text.includes(searchTerm);
    item.style.display = show ? 'block' : 'none';
  });
  
  console.log(`🔍 Busca aplicada: ${searchTerm}`);
}

// Exportar funções
window.eventsModule = {
  setupEventListeners,
  filterSchools,
  filterSchoolsBySearch
};
