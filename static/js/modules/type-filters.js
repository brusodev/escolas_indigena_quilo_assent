// ===================================================
// MÓDULO: FILTROS POR TIPO DE ESCOLA - CITEM COMPLETO
// ===================================================

// Configuração de cores por tipo de escola
const ESCOLA_COLORS = {
  'indigena': '#8B4513',
  'quilombola': '#800080',
  'assentamento': '#228B22',
  'regular': '#4169E1',
  'ceeja': '#FF6347',
  'cel_jto': '#FF8C00',
  'hospitalar': '#DC143C',
  'penitenciaria': '#2F4F4F',
  'socioeduc': '#9932CC',
  'socioeduc_adolesc': '#8A2BE2'
};

// Estado atual dos filtros
let currentFilter = 'all';
let filteredSchools = [];

// Inicializar filtros por tipo
function initializeTypeFilters() {
  console.log('🎛️ Inicializando filtros por tipo de escola...');
  
  const filterButtons = document.querySelectorAll('.type-filter-btn');
  
  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      const filterType = this.dataset.type;
      
      // Atualizar botões ativos
      filterButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      
      // Aplicar filtro
      applyTypeFilter(filterType);
      
      // Atualizar mapa
      updateMapMarkers(filterType);
      
      // Atualizar lista de escolas
      updateSchoolList(filterType);
      
      // Atualizar contadores
      updateFilterCounters(filterType);
    });
  });
}

// Aplicar filtro por tipo de escola
function applyTypeFilter(filterType) {
  currentFilter = filterType;
  
  if (filterType === 'all') {
    filteredSchools = schoolsData;
  } else {
    filteredSchools = schoolsData.filter(school => {
      // Agrupar tipos socioeducativos
      if (filterType === 'socioeduc') {
        return school.type === 'socioeduc' || school.type === 'socioeduc_adolesc';
      }
      return school.type === filterType;
    });
  }
  
  console.log(`🔍 Filtro aplicado: ${filterType} - ${filteredSchools.length} escolas`);
}

// Atualizar marcadores no mapa
function updateMapMarkers(filterType) {
  if (!map) return;
  
  // Limpar marcadores existentes
  if (window.schoolMarkers) {
    window.schoolMarkers.forEach(marker => {
      map.removeLayer(marker);
    });
  }
  
  window.schoolMarkers = [];
  
  // Adicionar marcadores filtrados
  filteredSchools.forEach(school => {
    if (school.lat && school.lng) {
      const color = ESCOLA_COLORS[school.type] || '#666666';
      
      const marker = L.circleMarker([school.lat, school.lng], {
        radius: 6,
        fillColor: color,
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.8
      });
      
      // Popup com informações da escola
      const popupContent = `
        <div class="school-popup">
          <h4>${school.name}</h4>
          <p><strong>Tipo:</strong> ${school.tipo_original || school.type}</p>
          <p><strong>Município:</strong> ${school.city}</p>
          <p><strong>Unidade Regional:</strong> ${school.diretoria}</p>
          <p><strong>Código MEC:</strong> ${school.codigo_mec}</p>
          <p><strong>Zona:</strong> ${school.zona}</p>
        </div>
      `;
      
      marker.bindPopup(popupContent);
      marker.addTo(map);
      window.schoolMarkers.push(marker);
    }
  });
  
  // Atualizar contador de escolas visíveis
  const visibleCount = document.getElementById('visible-schools-count');
  if (visibleCount) {
    visibleCount.textContent = `${filteredSchools.length.toLocaleString('pt-BR')} escolas visíveis`;
  }
}

// Atualizar lista de escolas
function updateSchoolList(filterType) {
  const schoolList = document.getElementById('school-list');
  if (!schoolList) return;
  
  schoolList.innerHTML = '';
  
  // Limitar número de escolas exibidas na lista para performance
  const maxDisplay = 100;
  const schoolsToShow = filteredSchools.slice(0, maxDisplay);
  
  if (filteredSchools.length > maxDisplay) {
    const notice = document.createElement('div');
    notice.className = 'list-notice';
    notice.innerHTML = `
      <p>📋 Mostrando ${maxDisplay} de ${filteredSchools.length.toLocaleString('pt-BR')} escolas</p>
      <small>Use os filtros ou a busca para refinar os resultados</small>
    `;
    schoolList.appendChild(notice);
  }
  
  schoolsToShow.forEach(school => {
    const schoolItem = document.createElement('div');
    schoolItem.className = 'school-item';
    
    const typeColor = ESCOLA_COLORS[school.type] || '#666666';
    
    schoolItem.innerHTML = `
      <div class="school-header">
        <span class="school-type-indicator" style="background-color: ${typeColor}"></span>
        <h4 class="school-name">${school.name}</h4>
      </div>
      <div class="school-details">
        <p><strong>Tipo:</strong> ${school.tipo_original || school.type}</p>
        <p><strong>Município:</strong> ${school.city}</p>
        <p><strong>Unidade Regional:</strong> ${school.diretoria}</p>
        <p><strong>Código:</strong> ${school.codigo_mec}</p>
      </div>
    `;
    
    // Adicionar evento de clique para centralizar no mapa
    schoolItem.addEventListener('click', () => {
      if (school.lat && school.lng) {
        map.setView([school.lat, school.lng], 12);
        
        // Destacar marcador correspondente
        const marker = window.schoolMarkers.find(m => 
          m.getLatLng().lat === school.lat && 
          m.getLatLng().lng === school.lng
        );
        
        if (marker) {
          marker.openPopup();
        }
      }
    });
    
    schoolList.appendChild(schoolItem);
  });
}

// Atualizar contadores nos filtros
function updateFilterCounters(filterType) {
  const stats = {
    all: schoolsData.length,
    regular: schoolsData.filter(s => s.type === 'regular').length,
    indigena: schoolsData.filter(s => s.type === 'indigena').length,
    quilombola: schoolsData.filter(s => s.type === 'quilombola').length,
    assentamento: schoolsData.filter(s => s.type === 'assentamento').length,
    ceeja: schoolsData.filter(s => s.type === 'ceeja').length,
    cel_jto: schoolsData.filter(s => s.type === 'cel_jto').length,
    hospitalar: schoolsData.filter(s => s.type === 'hospitalar').length,
    penitenciaria: schoolsData.filter(s => s.type === 'penitenciaria').length,
    socioeduc: schoolsData.filter(s => s.type === 'socioeduc' || s.type === 'socioeduc_adolesc').length
  };
  
  // Atualizar contadores na legenda
  Object.keys(stats).forEach(type => {
    const counter = document.getElementById(`${type}-count`);
    if (counter) {
      counter.textContent = stats[type].toLocaleString('pt-BR');
    }
  });
  
  // Atualizar estatísticas principais
  const totalSchools = document.getElementById('total-schools');
  if (totalSchools) {
    totalSchools.textContent = filteredSchools.length.toLocaleString('pt-BR');
  }
}

// Busca dinâmica
function initializeSearch() {
  const searchInput = document.getElementById('search-input');
  if (!searchInput) return;
  
  searchInput.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase().trim();
    
    if (searchTerm === '') {
      applyTypeFilter(currentFilter);
    } else {
      // Filtrar por termo de busca dentro do filtro atual
      const baseSchools = currentFilter === 'all' ? schoolsData : 
        schoolsData.filter(school => {
          if (currentFilter === 'socioeduc') {
            return school.type === 'socioeduc' || school.type === 'socioeduc_adolesc';
          }
          return school.type === currentFilter;
        });
      
      filteredSchools = baseSchools.filter(school => 
        school.name.toLowerCase().includes(searchTerm) ||
        school.city.toLowerCase().includes(searchTerm) ||
        school.diretoria.toLowerCase().includes(searchTerm) ||
        (school.tipo_original && school.tipo_original.toLowerCase().includes(searchTerm))
      );
    }
    
    updateMapMarkers(currentFilter);
    updateSchoolList(currentFilter);
    updateFilterCounters(currentFilter);
  });
}

// Exportar funções para uso global
window.initializeTypeFilters = initializeTypeFilters;
window.initializeSearch = initializeSearch;
window.applyTypeFilter = applyTypeFilter;
window.updateMapMarkers = updateMapMarkers;
window.ESCOLA_COLORS = ESCOLA_COLORS;
