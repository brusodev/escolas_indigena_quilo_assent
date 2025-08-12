// ===================================================
// MÓDULO: MARCADORES DE DIRETORIAS
// ===================================================

// Coordenadas das diretorias (baseado nos dados existentes)
const DIRETORIAS_COORDENADAS = {
  'Adamantina': { lat: -21.6838, lng: -51.0713 },
  'Americana': { lat: -22.7394, lng: -47.3314 },
  'Andradina': { lat: -20.8957, lng: -51.3790 },
  'Apiai': { lat: -24.5095, lng: -48.8426 },
  'Aracatuba': { lat: -21.2088, lng: -50.4329 },
  'Araraquara': { lat: -21.7947, lng: -48.1756 },
  'Assis': { lat: -22.6616, lng: -50.4122 },
  'Avare': { lat: -23.0984, lng: -48.9267 },
  'Barretos': { lat: -20.5570, lng: -48.5681 },
  'Bauru': { lat: -22.3144, lng: -49.0608 },
  'Birigui': { lat: -21.2886, lng: -50.3403 },
  'Botucatu': { lat: -22.8853, lng: -48.4450 },
  'Braganca Paulista': { lat: -22.9530, lng: -46.5441 },
  'Caieiras': { lat: -23.3619, lng: -46.7419 },
  'Campinas Leste': { lat: -22.9056, lng: -47.0608 },
  'Campinas Oeste': { lat: -22.9056, lng: -47.0808 },
  'Capivari': { lat: -22.9952, lng: -47.5078 },
  'Caraguatatuba': { lat: -23.6203, lng: -45.4133 },
  'Carapicuiba': { lat: -23.5225, lng: -46.8356 },
  'Catanduva': { lat: -21.1378, lng: -48.9722 },
  'Centro': { lat: -23.5431, lng: -46.6291 },
  'Centro Oeste': { lat: -23.5331, lng: -46.6791 },
  'Centro Sul': { lat: -23.5631, lng: -46.6291 },
  'Diadema': { lat: -23.6864, lng: -46.6208 },
  'Fernandopolis': { lat: -20.2836, lng: -50.2458 },
  'Franca': { lat: -20.5386, lng: -47.4006 },
  'Guaratingueta': { lat: -22.8161, lng: -45.1928 },
  'Guarulhos Norte': { lat: -23.4628, lng: -46.5333 },
  'Guarulhos Sul': { lat: -23.4828, lng: -46.5333 },
  'Itapecerica Da Serra': { lat: -23.7178, lng: -46.8497 },
  'Itapetininga': { lat: -23.5917, lng: -48.0528 },
  'Itapeva': { lat: -23.9825, lng: -48.8761 },
  'Itapevi': { lat: -23.5489, lng: -46.9319 },
  'Itaquaquecetuba': { lat: -23.4864, lng: -46.3478 },
  'Itarare': { lat: -24.1133, lng: -49.3303 },
  'Itu': { lat: -23.2642, lng: -47.2997 },
  'Jaboticabal': { lat: -21.2544, lng: -48.3228 },
  'Jacarei': { lat: -23.3056, lng: -45.9658 },
  'Jales': { lat: -20.2694, lng: -50.5456 },
  'Jau': { lat: -22.2958, lng: -48.5578 },
  'Jose Bonifacio': { lat: -21.0544, lng: -49.6889 },
  'Jundiai': { lat: -23.1864, lng: -46.8842 },
  'Leste 1': { lat: -23.5431, lng: -46.5791 },
  'Leste 2': { lat: -23.5531, lng: -46.5691 },
  'Leste 3': { lat: -23.5631, lng: -46.5591 },
  'Leste 4': { lat: -23.5731, lng: -46.5491 },
  'Leste 5': { lat: -23.5831, lng: -46.5391 },
  'Limeira': { lat: -22.5647, lng: -47.4019 },
  'Lins': { lat: -21.6758, lng: -49.7464 },
  'Marilia': { lat: -22.2139, lng: -49.9456 },
  'Maua': { lat: -23.6672, lng: -46.4619 },
  'Miracatu': { lat: -24.2806, lng: -47.4597 },
  'Mirante Do Paranapanema': { lat: -22.2881, lng: -51.9103 },
  'Mogi Das Cruzes': { lat: -23.5228, lng: -46.1881 },
  'Mogi Mirim': { lat: -22.4319, lng: -46.9578 },
  'Norte 1': { lat: -23.5031, lng: -46.6291 },
  'Norte 2': { lat: -23.4931, lng: -46.6191 },
  'Osasco': { lat: -23.5322, lng: -46.7917 },
  'Ourinhos': { lat: -22.9789, lng: -49.8706 },
  'Penapolis': { lat: -21.4206, lng: -50.0775 },
  'Pindamonhangaba': { lat: -22.9244, lng: -45.4619 },
  'Piracicaba': { lat: -22.7342, lng: -47.6492 },
  'Piraju': { lat: -23.1944, lng: -49.3839 },
  'Pirassununga': { lat: -21.9961, lng: -47.4258 },
  'Presidente Prudente': { lat: -22.1256, lng: -51.3889 },
  'Registro': { lat: -24.4892, lng: -47.8431 },
  'Ribeirao Preto': { lat: -21.1797, lng: -47.8106 },
  'Santo Anastacio': { lat: -21.9697, lng: -51.6753 },
  'Santo Andre': { lat: -23.6636, lng: -46.5331 },
  'Santos': { lat: -23.9608, lng: -46.3331 },
  'Sao Bernardo Do Campo': { lat: -23.6939, lng: -46.5650 },
  'Sao Carlos': { lat: -22.0178, lng: -47.8908 },
  'Sao Joao Da Boa Vista': { lat: -21.9697, lng: -46.7978 },
  'Sao Joaquim Da Barra': { lat: -20.5844, lng: -47.8575 },
  'Sao Jose Do Rio Preto': { lat: -20.8197, lng: -49.3794 },
  'Sao Jose Dos Campos': { lat: -23.2237, lng: -45.9009 },
  'Sao Roque': { lat: -23.5283, lng: -47.1356 },
  'Sao Vicente': { lat: -23.9631, lng: -46.3911 },
  'Sertaozinho': { lat: -21.1394, lng: -47.9911 },
  'Sorocaba': { lat: -23.5014, lng: -47.4581 },
  'Sul 1': { lat: -23.5831, lng: -46.6291 },
  'Sul 2': { lat: -23.5931, lng: -46.6191 },
  'Sul 3': { lat: -23.6031, lng: -46.6091 },
  'Sumare': { lat: -22.8219, lng: -47.2669 },
  'Suzano': { lat: -23.5425, lng: -46.3106 },
  'Taboao Da Serra': { lat: -23.6086, lng: -46.7581 },
  'Taquaritinga': { lat: -21.4081, lng: -48.5078 },
  'Taubate': { lat: -23.0264, lng: -45.5553 },
  'Tupa': { lat: -21.9347, lng: -50.5133 },
  'Votorantim': { lat: -23.5392, lng: -47.4378 },
  'Votuporanga': { lat: -20.4228, lng: -49.9731 }
};

// Função para normalizar nome da diretoria
function normalizeDiretoriaName(name) {
  if (!name) return "";
  
  let normalized = name.trim();
  
  // Remover "DE ENSINO" se presente
  normalized = normalized.replace(/\s+DE\s+ENSINO\s*$/i, '');
  
  // Mapeamentos específicos para correções
  const mappings = {
    "SAO VICENTE": "Sao Vicente",
    "SÃO VICENTE": "Sao Vicente",
    "SAO BERNARDO DO CAMPO": "Sao Bernardo Do Campo",
    "SANTO ANASTACIO": "Santo Anastacio",
    "PENAPOLIS": "Penapolis",
    "TUPA": "Tupa",
    "ITARARE": "Itarare",
    "BRAGANCA PAULISTA": "Braganca Paulista",
    "APIAI": "Apiai",
    "ARACATUBA": "Aracatuba",
    "AVARE": "Avare",
    "CARAPICUIBA": "Carapicuiba",
    "FERNANDOPOLIS": "Fernandopolis",
    "GUARATINGUETA": "Guaratingueta",
    "ITAPECERICA DA SERRA": "Itapecerica Da Serra",
    "JACAREI": "Jacarei",
    "JAU": "Jau",
    "JOSE BONIFACIO": "Jose Bonifacio",
    "JUNDIAI": "Jundiai",
    "MARILIA": "Marilia",
    "MAUA": "Maua",
    "MIRANTE DO PARANAPANEMA": "Mirante Do Paranapanema",
    "PENAPOLIS": "Penapolis",
    "RIBEIRAO PRETO": "Ribeirao Preto",
    "SAO CARLOS": "Sao Carlos",
    "SAO JOAO DA BOA VISTA": "Sao Joao Da Boa Vista",
    "SAO JOAQUIM DA BARRA": "Sao Joaquim Da Barra",
    "SAO JOSE DO RIO PRETO": "Sao Jose Do Rio Preto",
    "SAO JOSE DOS CAMPOS": "Sao Jose Dos Campos",
    "SAO ROQUE": "Sao Roque",
    "SERTAOZINHO": "Sertaozinho",
    "SUMARE": "Sumare",
    "TABOAO DA SERRA": "Taboao Da Serra",
    "TAUBATE": "Taubate"
  };

  const upperName = normalized.toUpperCase();
  for (const [original, replacement] of Object.entries(mappings)) {
    if (upperName === original) {
      return replacement;
    }
  }

  return normalized;
}

// Função para obter coordenadas de uma diretoria
function getDiretoriaCoordinates(diretoriaName) {
  const normalizedName = normalizeDiretoriaName(diretoriaName);
  return DIRETORIAS_COORDENADAS[normalizedName] || null;
}

// Função para criar marcador de diretoria
function createDiretoriaMarker(diretoriaName, schoolsCount, vehiclesData) {
  const coords = getDiretoriaCoordinates(diretoriaName);
  if (!coords) {
    console.warn('⚠️ Coordenadas não encontradas para diretoria:', diretoriaName);
    return null;
  }

  const totalVehicles = vehiclesData?.total || 0;
  
  // Criar ícone de diretoria
  const icon = L.divIcon({
    className: 'diretoria-marker',
    html: `<div style="
      background: #3498db;
      color: white;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 3px 6px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      font-weight: bold;
    ">${totalVehicles}</div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10]
  });

  // Criar marcador
  const marker = L.marker([coords.lat, coords.lng], { icon });
  
  // Popup com informações da diretoria
  const popupContent = `
    <div style="min-width: 220px;">
      <h4 style="margin: 0 0 10px 0; color: #3498db;">
        🏛️ ${diretoriaName}
      </h4>
      <p style="margin: 5px 0;"><strong>Escolas:</strong> ${schoolsCount}</p>
      <p style="margin: 5px 0;"><strong>Veículos:</strong> ${totalVehicles}</p>
      ${vehiclesData ? `
        <div style="margin: 10px 0; padding: 8px; background: #f8f9fa; border-radius: 4px;">
          <strong>Distribuição de Veículos:</strong><br>
          ${vehiclesData.s1 ? `S-1: ${vehiclesData.s1}<br>` : ''}
          ${vehiclesData.s2 ? `S-2: ${vehiclesData.s2}<br>` : ''}
          ${vehiclesData.s2_4x4 ? `S-2 4x4: ${vehiclesData.s2_4x4}` : ''}
        </div>
      ` : ''}
      <p style="margin: 5px 0; font-size: 0.9em; color: #666;">
        Coord: ${coords.lat.toFixed(4)}, ${coords.lng.toFixed(4)}
      </p>
    </div>
  `;
  
  marker.bindPopup(popupContent);
  
  // Adicionar dados da diretoria ao marcador
  marker.diretoriaData = {
    name: diretoriaName,
    schoolsCount,
    vehiclesData,
    coordinates: coords
  };
  
  return marker;
}

// Função para adicionar todas as diretorias ao mapa
function addDiretoriasToMap(map, schools, vehicleData) {
  if (!map || !schools || !schools.length) {
    console.warn('⚠️ Mapa ou dados de escolas inválidos');
    return [];
  }

  const markers = [];
  const getVehicleDataForDiretoria = window.dataModule?.getVehicleDataForDiretoria;
  
  // Agrupar escolas por diretoria
  const diretoriasGroup = {};
  schools.forEach(school => {
    const dir = school.diretoria;
    if (!diretoriasGroup[dir]) {
      diretoriasGroup[dir] = [];
    }
    diretoriasGroup[dir].push(school);
  });

  let validMarkers = 0;
  let invalidMarkers = 0;

  // Criar marcador para cada diretoria
  Object.keys(diretoriasGroup).forEach(diretoriaName => {
    const schoolsInDiretoria = diretoriasGroup[diretoriaName];
    const vehiclesData = getVehicleDataForDiretoria ? getVehicleDataForDiretoria(diretoriaName) : null;
    
    const marker = createDiretoriaMarker(diretoriaName, schoolsInDiretoria.length, vehiclesData);
    
    if (marker) {
      marker.addTo(map);
      markers.push(marker);
      validMarkers++;
    } else {
      invalidMarkers++;
    }
  });

  console.log(`🏛️ Marcadores de diretorias: ${validMarkers} válidos, ${invalidMarkers} inválidos`);
  
  return markers;
}

// Exportar funções
window.diretoriaMarkersModule = {
  normalizeDiretoriaName,
  getDiretoriaCoordinates,
  createDiretoriaMarker,
  addDiretoriasToMap,
  DIRETORIAS_COORDENADAS
};

console.log('🏛️ Módulo de marcadores de diretorias carregado');
