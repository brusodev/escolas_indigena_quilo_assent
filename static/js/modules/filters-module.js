// ===================================================
// MÓDULO: FILTROS E BUSCA
// ===================================================

// Estado dos filtros
let currentFilters = {
  type: 'all',
  searchText: '',
  priority: 'all'
};

// Dados filtrados atuais
let filteredSchools = [];

// Função para filtrar escolas por tipo
function filterSchoolsByType(schools, type) {
  if (!schools || !schools.length) return [];
  
  if (type === 'all') {
    return schools;
  }
  
  return schools.filter(school => school.type === type);
}

// Função para filtrar escolas por texto de busca
function filterSchoolsBySearch(schools, searchText) {
  if (!schools || !schools.length || !searchText) return schools;
  
  const search = searchText.toLowerCase().trim();
  
  return schools.filter(school => {
    const name = (school.name || '').toLowerCase();
    const city = (school.city || '').toLowerCase();
    const diretoria = (school.diretoria || '').toLowerCase();
    
    return name.includes(search) || 
           city.includes(search) || 
           diretoria.includes(search);
  });
}

// Função para filtrar escolas por prioridade
function filterSchoolsByPriority(schools, priority) {
  if (!schools || !schools.length) return [];
  
  switch (priority) {
    case 'all':
      return schools;
    case 'priority-high':
      return schools.filter(school => school.distance && school.distance > 50);
    case 'priority-medium':
      return schools.filter(school => school.distance && school.distance > 25 && school.distance <= 50);
    case 'priority-low':
      return schools.filter(school => !school.distance || school.distance <= 25);
    case 'indigena':
      return schools.filter(school => school.type === 'indigena');
    case 'quilombola':
      return schools.filter(school => school.type === 'quilombola');
    default:
      return schools;
  }
}

// Função para aplicar todos os filtros
function applyAllFilters(schools, filters = currentFilters) {
  if (!schools || !schools.length) return [];
  
  let filtered = schools;
  
  // Aplicar filtro de tipo
  filtered = filterSchoolsByType(filtered, filters.type);
  
  // Aplicar filtro de busca
  filtered = filterSchoolsBySearch(filtered, filters.searchText);
  
  // Aplicar filtro de prioridade
  filtered = filterSchoolsByPriority(filtered, filters.priority);
  
  return filtered;
}

// Função para atualizar a exibição baseada nos filtros
function updateDisplayWithFilters(allSchools) {
  if (!allSchools || !allSchools.length) {
    console.warn('⚠️ Dados de escolas não disponíveis para filtros');
    return;
  }

  // Aplicar filtros
  filteredSchools = applyAllFilters(allSchools, currentFilters);
  
  // Atualizar mapa
  updateMapWithFilters(filteredSchools);
  
  // Atualizar lista de escolas
  updateSchoolListWithFilters(filteredSchools);
  
  // Atualizar contadores
  updateFilterCounters(filteredSchools, allSchools);
  
  console.log(`🔍 Filtros aplicados: ${filteredSchools.length}/${allSchools.length} escolas`);
}

// Função para atualizar o mapa com escolas filtradas
function updateMapWithFilters(schools) {
  if (!window.map) return;
  
  // Remover marcadores existentes (exceto diretorias)
  window.map.eachLayer(layer => {
    if (layer.schoolData) {
      window.map.removeLayer(layer);
    }
  });
  
  // Adicionar marcadores filtrados
  if (window.schoolMarkersModule) {
    window.schoolMarkersModule.addSchoolsToMap(window.map, schools);
  }
}

// Função para atualizar lista de escolas
function updateSchoolListWithFilters(schools) {
  const schoolList = document.getElementById('school-list');
  if (!schoolList) return;
  
  if (!schools || schools.length === 0) {
    schoolList.innerHTML = `
      <div style="text-align: center; padding: 20px; color: #666;">
        <p>📭 Nenhuma escola encontrada com os filtros atuais</p>
      </div>
    `;
    return;
  }
  
  // Ordenar escolas por distância (maiores primeiro)
  const sortedSchools = schools.sort((a, b) => (b.distance || 0) - (a.distance || 0));
  
  let html = '';
  sortedSchools.forEach(school => {
    const emoji = window.schoolMarkersModule?.getSchoolEmoji(school.type) || '📚';
    const typeName = window.schoolMarkersModule?.getSchoolTypeName(school.type) || school.type;
    const distance = school.distance ? `${school.distance.toFixed(1)} km` : 'N/A';
    const priorityClass = school.distance > 50 ? 'high-priority' : 
                         school.distance > 25 ? 'medium-priority' : 'low-priority';
    
    html += `
      <div class="school-item ${priorityClass}" data-school-name="${school.name}" 
           style="padding: 12px; margin: 8px 0; border-left: 4px solid ${window.schoolMarkersModule?.getSchoolMarkerColor(school.type) || '#ccc'}; 
                  background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); cursor: pointer;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div style="flex: 1;">
            <h4 style="margin: 0 0 5px 0; color: #2c3e50;">${emoji} ${school.name}</h4>
            <p style="margin: 3px 0; color: #666; font-size: 0.9em;">
              <strong>Tipo:</strong> ${typeName}
            </p>
            <p style="margin: 3px 0; color: #666; font-size: 0.9em;">
              <strong>Cidade:</strong> ${school.city}
            </p>
            <p style="margin: 3px 0; color: #666; font-size: 0.9em;">
              <strong>Diretoria:</strong> ${school.diretoria}
            </p>
          </div>
          <div style="text-align: right; margin-left: 15px;">
            <div style="font-weight: bold; color: ${school.distance > 50 ? '#e74c3c' : school.distance > 25 ? '#f39c12' : '#27ae60'};">
              ${distance}
            </div>
            <div style="font-size: 0.8em; color: #666;">
              ${school.distance > 50 ? '🔴 Alta' : school.distance > 25 ? '🟡 Média' : '🟢 Baixa'}
            </div>
          </div>
        </div>
      </div>
    `;
  });
  
  schoolList.innerHTML = html;
  
  // Adicionar eventos de clique
  schoolList.querySelectorAll('.school-item').forEach(item => {
    item.addEventListener('click', () => {
      const schoolName = item.dataset.schoolName;
      const school = schools.find(s => s.name === schoolName);
      if (school && window.map) {
        window.map.setView([school.lat, school.lng], 14);
      }
    });
  });
}

// Função para atualizar contadores de filtros
function updateFilterCounters(filteredSchools, allSchools) {
  // Atualizar botões de filtro com contadores
  const filterButtons = document.querySelectorAll('.filter-btn');
  filterButtons.forEach(btn => {
    const filter = btn.dataset.filter;
    let count = 0;
    
    switch (filter) {
      case 'all':
        count = allSchools.length;
        break;
      case 'indigena':
        count = allSchools.filter(s => s.type === 'indigena').length;
        break;
      case 'quilombola':
        count = allSchools.filter(s => s.type === 'quilombola').length;
        break;
      case 'priority-high':
        count = allSchools.filter(s => s.distance && s.distance > 50).length;
        break;
    }
    
    const text = btn.textContent.split('(')[0].trim();
    btn.textContent = `${text} (${count})`;
  });
}

// Função para configurar eventos de filtros
function setupFilterEvents(allSchools) {
  // Filtros de botão
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      currentFilters.priority = btn.dataset.filter;
      updateDisplayWithFilters(allSchools);
    });
  });
  
  // Filtros de tipo
  document.querySelectorAll('.type-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.type-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      currentFilters.type = btn.dataset.type;
      updateDisplayWithFilters(allSchools);
    });
  });
  
  // Campo de busca
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentFilters.searchText = e.target.value;
      updateDisplayWithFilters(allSchools);
    });
  }
  
  console.log('🔍 Eventos de filtros configurados');
}

// Função para resetar filtros
function resetFilters(allSchools) {
  currentFilters = {
    type: 'all',
    searchText: '',
    priority: 'all'
  };
  
  // Resetar botões ativos
  document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.type-filter-btn').forEach(btn => btn.classList.remove('active'));
  
  document.querySelector('.filter-btn[data-filter="all"]')?.classList.add('active');
  document.querySelector('.type-filter-btn[data-type="all"]')?.classList.add('active');
  
  // Limpar campo de busca
  const searchInput = document.getElementById('search-input');
  if (searchInput) searchInput.value = '';
  
  updateDisplayWithFilters(allSchools);
  
  console.log('🔄 Filtros resetados');
}

// Exportar funções
window.filtersModule = {
  filterSchoolsByType,
  filterSchoolsBySearch,
  filterSchoolsByPriority,
  applyAllFilters,
  updateDisplayWithFilters,
  setupFilterEvents,
  resetFilters,
  getCurrentFilters: () => currentFilters,
  getFilteredSchools: () => filteredSchools
};

console.log('🔍 Módulo de filtros carregado');
