// ===================================================
// MÓDULO: INTERFACE E UI
// ===================================================

// Função para atualizar contadores da legenda
function updateLegendCounts() {
  const schoolsData = window.dataModule.schoolsData();
  const getVehicleDataForDiretoria = window.dataModule.getVehicleDataForDiretoria;
  
  const indigenas = schoolsData.filter(s => s.type === 'indigena').length;
  const quilombolas = schoolsData.filter(s => s.type === 'quilombola').length;
  const diretorias = [...new Set(schoolsData.map(s => s.diretoria))].length;
  
  // Calcular veículos relevantes
  const diretorias_escolas = [...new Set(schoolsData.map((s) => s.diretoria))];
  let totalVehiclesRelevantes = 0;
  diretorias_escolas.forEach((diretoria) => {
    const dados = getVehicleDataForDiretoria(diretoria);
    totalVehiclesRelevantes += dados.total;
  });

  // Atualizar contadores na legenda
  const indigenaCount = document.getElementById('indigena-count');
  const quilombolaCount = document.getElementById('quilombola-count');
  const diretoriasCount = document.getElementById('diretorias-count');
  const veiculosLegendCount = document.getElementById('veiculos-legend-count');

  if (indigenaCount) indigenaCount.textContent = indigenas;
  if (quilombolaCount) quilombolaCount.textContent = quilombolas;
  if (diretoriasCount) diretoriasCount.textContent = diretorias;
  if (veiculosLegendCount) veiculosLegendCount.textContent = totalVehiclesRelevantes;

  console.log(`📊 Legenda atualizada: ${indigenas} indígenas, ${quilombolas} quilombolas`);
}

// Função para calcular estatísticas
function calculateStats() {
  const schoolsData = window.dataModule.schoolsData();
  const getVehicleDataForDiretoria = window.dataModule.getVehicleDataForDiretoria;
  
  if (!schoolsData.length) {
    console.warn("⚠️ Dados das escolas não carregados");
    return;
  }

  const diretorias_escolas = [...new Set(schoolsData.map((s) => s.diretoria))];
  let totalVehiclesRelevantes = 0;

  diretorias_escolas.forEach((diretoria) => {
    const dados = getVehicleDataForDiretoria(diretoria);
    totalVehiclesRelevantes += dados.total;
  });

  const highPrioritySchools = schoolsData.filter((s) => s.distance > 50).length;
  const uniqueDiretorias = [...new Set(schoolsData.map((s) => s.diretoria))].length;

  const totalVehiclesElement = document.getElementById("total-vehicles");
  const highPriorityElement = document.getElementById("high-priority");
  const diretoriasElement = document.getElementById("total-diretorias");

  if (totalVehiclesElement) totalVehiclesElement.textContent = totalVehiclesRelevantes;
  if (highPriorityElement) highPriorityElement.textContent = highPrioritySchools;
  if (diretoriasElement) diretoriasElement.textContent = uniqueDiretorias;

  console.log(`🔢 Estatísticas: ${totalVehiclesRelevantes} veículos, ${uniqueDiretorias} diretorias`);
}

// Função para focar uma escola no mapa
function focusSchoolOnMap(school) {
  if (!school.lat || !school.lng) {
    console.warn("⚠️ Coordenadas da escola não encontradas:", school.name);
    return;
  }

  if (window.map) {
    window.map.setView([school.lat, school.lng], 12);
    
    window.map.eachLayer(function(layer) {
      if (layer.getLatLng && layer.getPopup) {
        const latlng = layer.getLatLng();
        if (Math.abs(latlng.lat - school.lat) < 0.001 && Math.abs(latlng.lng - school.lng) < 0.001) {
          layer.openPopup();
        }
      }
    });
    
    console.log(`📍 Focando escola: ${school.name}`);
  }
}

// Função para gerar lista de escolas
function generateSchoolList() {
  const schoolsData = window.dataModule.schoolsData();
  const schoolList = document.getElementById('school-list');
  
  if (!schoolList) {
    console.warn("⚠️ Elemento school-list não encontrado");
    return;
  }

  const sortedSchools = [...schoolsData].sort((a, b) => b.distance - a.distance);
  schoolList.innerHTML = '';

  sortedSchools.forEach(school => {
    const priorityClass = school.distance > 50 ? 'high' : school.distance > 25 ? 'medium' : 'low';
    const priorityText = school.distance > 50 ? 'Alta' : school.distance > 25 ? 'Média' : 'Baixa';
    const typeClass = school.type === 'indigena' ? 'indigena' : 'quilombola';
    
    const schoolItem = document.createElement('div');
    schoolItem.className = `school-item ${typeClass} priority-${priorityClass}`;
    schoolItem.style.cursor = 'pointer';
    schoolItem.innerHTML = `
      <div class="school-header">
        <h4 class="school-name">${school.name}</h4>
        <span class="priority-badge priority-${priorityClass}">${priorityText}</span>
      </div>
      <div class="school-details">
        <p><strong>Tipo:</strong> ${school.type === 'indigena' ? 'Indígena' : 'Quilombola'}</p>
        <p><strong>Cidade:</strong> ${school.city}</p>
        <p><strong>Distância:</strong> ${school.distance} km</p>
        <p><strong>Diretoria:</strong> ${school.diretoria}</p>
      </div>
      <div class="school-action">
        <small>🗺️ Clique para localizar no mapa</small>
      </div>
    `;
    
    schoolItem.addEventListener('click', function() {
      focusSchoolOnMap(school);
    });
    
    schoolList.appendChild(schoolItem);
  });

  console.log(`📋 Lista gerada: ${sortedSchools.length} escolas`);
}

// Exportar funções
window.uiModule = {
  updateLegendCounts,
  calculateStats,
  generateSchoolList,
  focusSchoolOnMap
};
