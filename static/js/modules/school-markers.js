// ===================================================
// MÓDULO: MARCADORES DE ESCOLAS
// ===================================================

// Função para obter cor do marcador baseado no tipo de escola
function getSchoolMarkerColor(type) {
  const colorMap = {
    'indigena': '#e74c3c',        // Vermelho
    'quilombola': '#f39c12',      // Laranja  
    'regular': '#27ae60',         // Verde
    'cel_jto': '#3498db',         // Azul
    'escola_penitenciaria': '#34495e',  // Cinza escuro
    'centro_atend_soc_educ_adolesc': '#9b59b6', // Roxo
    'hospitalar': '#95a5a6',      // Cinza claro
    'ceeja': '#f1c40f',           // Amarelo
    'centro_atend_socioeduc': '#8b4513'  // Marrom
  };
  
  return colorMap[type] || '#7f8c8d'; // Cinza padrão
}

// Função para obter emoji do tipo de escola
function getSchoolEmoji(type) {
  const emojiMap = {
    'indigena': '🔴',
    'quilombola': '🟠',
    'regular': '🟢',
    'cel_jto': '🔵',
    'escola_penitenciaria': '⚫',
    'centro_atend_soc_educ_adolesc': '🟣',
    'hospitalar': '⚪',
    'ceeja': '🟡',
    'centro_atend_socioeduc': '🟤'
  };
  
  return emojiMap[type] || '📚';
}

// Função para obter nome limpo do tipo
function getSchoolTypeName(type) {
  const nameMap = {
    'indigena': 'Indígena',
    'quilombola': 'Quilombola',
    'regular': 'Regular',
    'cel_jto': 'CEL/JTO',
    'escola_penitenciaria': 'Penitenciária',
    'centro_atend_soc_educ_adolesc': 'Centro Atend. Adolesc.',
    'hospitalar': 'Hospitalar',
    'ceeja': 'CEEJA',
    'centro_atend_socioeduc': 'Centro Socioeducativo'
  };
  
  return nameMap[type] || type;
}

// Função para criar marcador de escola
function createSchoolMarker(school) {
  if (!school.lat || !school.lng) {
    console.warn('⚠️ Escola sem coordenadas:', school.name);
    return null;
  }

  const color = getSchoolMarkerColor(school.type);
  const emoji = getSchoolEmoji(school.type);
  const typeName = getSchoolTypeName(school.type);
  
  // Criar ícone customizado
  const icon = L.divIcon({
    className: 'school-marker',
    html: `<div style="
      background: ${color};
      color: white;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      border: 2px solid white;
      box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [12, 12],
    iconAnchor: [6, 6]
  });

  // Criar marcador
  const marker = L.marker([school.lat, school.lng], { icon });
  
  // Popup com informações da escola
  const popupContent = `
    <div style="min-width: 200px;">
      <h4 style="margin: 0 0 10px 0; color: ${color};">
        ${emoji} ${school.name}
      </h4>
      <p style="margin: 5px 0;"><strong>Tipo:</strong> ${typeName}</p>
      <p style="margin: 5px 0;"><strong>Cidade:</strong> ${school.city}</p>
      <p style="margin: 5px 0;"><strong>Diretoria:</strong> ${school.diretoria}</p>
      ${school.distance ? `<p style="margin: 5px 0;"><strong>Distância:</strong> ${school.distance.toFixed(1)} km</p>` : ''}
      <p style="margin: 5px 0; font-size: 0.9em; color: #666;">
        Coord: ${school.lat.toFixed(4)}, ${school.lng.toFixed(4)}
      </p>
    </div>
  `;
  
  marker.bindPopup(popupContent);
  
  // Adicionar dados da escola ao marcador
  marker.schoolData = school;
  
  return marker;
}

// Função para adicionar todas as escolas ao mapa
function addSchoolsToMap(map, schools) {
  if (!map || !schools || !schools.length) {
    console.warn('⚠️ Mapa ou dados de escolas inválidos');
    return [];
  }

  const markers = [];
  let validMarkers = 0;
  let invalidMarkers = 0;

  schools.forEach(school => {
    const marker = createSchoolMarker(school);
    if (marker) {
      marker.addTo(map);
      markers.push(marker);
      validMarkers++;
    } else {
      invalidMarkers++;
    }
  });

  console.log(`📍 Marcadores de escolas: ${validMarkers} válidos, ${invalidMarkers} inválidos`);
  
  return markers;
}

// Exportar funções
window.schoolMarkersModule = {
  getSchoolMarkerColor,
  getSchoolEmoji,
  getSchoolTypeName,
  createSchoolMarker,
  addSchoolsToMap
};

console.log('📍 Módulo de marcadores de escolas carregado');
