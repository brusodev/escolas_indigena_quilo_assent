// ===================================================
// MÓDULO: LINHAS DE CONEXÃO ESCOLA-DIRETORIA
// ===================================================

// Função para calcular distância usando Haversine
function calculateDistance(lat1, lng1, lat2, lng2) {
  const R = 6371; // Raio da Terra em km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLng = (lng2 - lng1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
            Math.sin(dLng/2) * Math.sin(dLng/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

// Função para obter cor da linha baseada na distância
function getConnectionLineColor(distance) {
  if (distance <= 25) return '#27ae60';      // Verde - perto
  if (distance <= 50) return '#f39c12';      // Laranja - médio
  return '#e74c3c';                          // Vermelho - longe
}

// Função para obter opacidade baseada na distância
function getConnectionLineOpacity(distance) {
  if (distance <= 25) return 0.8;
  if (distance <= 50) return 0.6;
  return 0.9; // Mais visível para distâncias grandes
}

// Função para criar linha de conexão entre escola e diretoria
function createConnectionLine(school, diretoriaCoords) {
  if (!school.lat || !school.lng || !diretoriaCoords) {
    return null;
  }

  // Calcular distância
  const distance = calculateDistance(school.lat, school.lng, diretoriaCoords.lat, diretoriaCoords.lng);
  
  // Atualizar distância na escola se não existir
  if (!school.distance || school.distance === 0) {
    school.distance = distance;
  }

  const color = getConnectionLineColor(distance);
  const opacity = getConnectionLineOpacity(distance);
  
  // Criar linha
  const line = L.polyline([
    [school.lat, school.lng],
    [diretoriaCoords.lat, diretoriaCoords.lng]
  ], {
    color: color,
    weight: 2,
    opacity: opacity,
    dashArray: distance > 50 ? '5, 5' : null // Linha tracejada para distâncias grandes
  });

  // Popup para a linha
  const popupContent = `
    <div style="min-width: 200px;">
      <h4 style="margin: 0 0 10px 0; color: ${color};">
        📏 Conexão
      </h4>
      <p style="margin: 5px 0;"><strong>Escola:</strong> ${school.name}</p>
      <p style="margin: 5px 0;"><strong>Diretoria:</strong> ${school.diretoria}</p>
      <p style="margin: 5px 0;"><strong>Distância:</strong> ${distance.toFixed(1)} km</p>
      <p style="margin: 5px 0; font-size: 0.9em; color: #666;">
        ${distance <= 25 ? '🟢 Proximidade adequada' : 
          distance <= 50 ? '🟡 Distância moderada' : 
          '🔴 Alta prioridade de atenção'}
      </p>
    </div>
  `;
  
  line.bindPopup(popupContent);
  
  // Adicionar dados à linha
  line.connectionData = {
    school: school,
    diretoria: school.diretoria,
    distance: distance
  };
  
  return line;
}

// Função para adicionar todas as linhas de conexão ao mapa
function addConnectionLinesToMap(map, schools) {
  if (!map || !schools || !schools.length) {
    console.warn('⚠️ Mapa ou dados de escolas inválidos');
    return [];
  }

  const lines = [];
  const getDiretoriaCoordinates = window.diretoriaMarkersModule?.getDiretoriaCoordinates;
  
  if (!getDiretoriaCoordinates) {
    console.warn('⚠️ Módulo de diretorias não carregado');
    return [];
  }

  let validLines = 0;
  let invalidLines = 0;

  schools.forEach(school => {
    if (!school.diretoria) {
      invalidLines++;
      return;
    }

    const diretoriaCoords = getDiretoriaCoordinates(school.diretoria);
    
    if (diretoriaCoords) {
      const line = createConnectionLine(school, diretoriaCoords);
      
      if (line) {
        line.addTo(map);
        lines.push(line);
        validLines++;
      } else {
        invalidLines++;
      }
    } else {
      console.warn('⚠️ Coordenadas não encontradas para diretoria:', school.diretoria);
      invalidLines++;
    }
  });

  console.log(`📏 Linhas de conexão: ${validLines} válidas, ${invalidLines} inválidas`);
  
  return lines;
}

// Função para alternar visibilidade das linhas
function toggleConnectionLines(lines, visible) {
  if (!lines || !lines.length) return;
  
  lines.forEach(line => {
    if (visible) {
      line.setStyle({ opacity: line.options.opacity || 0.6 });
    } else {
      line.setStyle({ opacity: 0 });
    }
  });
  
  console.log(`📏 Linhas de conexão ${visible ? 'mostradas' : 'ocultadas'}`);
}

// Função para filtrar linhas por distância
function filterLinesByDistance(lines, minDistance = 0, maxDistance = Infinity) {
  if (!lines || !lines.length) return;
  
  lines.forEach(line => {
    const distance = line.connectionData?.distance || 0;
    const visible = distance >= minDistance && distance <= maxDistance;
    
    if (visible) {
      line.setStyle({ opacity: line.options.opacity || 0.6 });
    } else {
      line.setStyle({ opacity: 0 });
    }
  });
  
  console.log(`📏 Filtro aplicado: ${minDistance}-${maxDistance} km`);
}

// Exportar funções
window.connectionLinesModule = {
  calculateDistance,
  getConnectionLineColor,
  getConnectionLineOpacity,
  createConnectionLine,
  addConnectionLinesToMap,
  toggleConnectionLines,
  filterLinesByDistance
};

console.log('📏 Módulo de linhas de conexão carregado');
