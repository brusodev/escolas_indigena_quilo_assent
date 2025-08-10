// ===================================================
// MÓDULO: MAPAS (PRINCIPAL E TELA CHEIA)
// ===================================================

let fullscreenMap = null;

// Função para gerar abreviação da diretoria
function getDiretoriaAbbreviation(nome) {
  if (!nome) return "URE";
  
  const nomeUpper = nome.toUpperCase();
  
  // Mapeamentos específicos - incluindo variações com e sem "DE ENSINO"
  const mapeamentos = {
    'ADAMANTINA': 'ADA',
    'AMERICANA': 'AME', 
    'ANDRADINA': 'AND',
    'APIAÍ': 'API',
    'APIAI': 'API',
    'ARAÇATUBA': 'ARC',
    'ARACATUBA': 'ARC',
    'ARARAQUARA': 'ARA',
    'ASSIS': 'ASS',
    'AVARÉ': 'AVA',
    'AVARE': 'AVA',
    'BARRETOS': 'BAT',
    'BAURU': 'BAU',
    'BIRIGUI': 'BIR',
    'BOTUCATU': 'BOT',
    'BRAGANÇA PAULISTA': 'BPT',
    'BRAGANCA PAULISTA': 'BPT',
    'CAIEIRAS': 'CAI',
    'CAMPINAS LESTE': 'CLT',
    'CAMPINAS OESTE': 'COE',
    'CAPIVARI': 'CAP',
    'CARAGUATATUBA': 'CGT',
    'CARAPICUÍBA': 'CAR',
    'CARAPICUIBA': 'CAR',
    'CATANDUVA': 'CAT',
    'CENTRO': 'CTR',
    'CENTRO OESTE': 'CTO',
    'CENTRO SUL': 'CTS',
    'DIADEMA': 'DIA',
    'FERNANDÓPOLIS': 'FER',
    'FERNANDOPOLIS': 'FER',
    'FRANCA': 'FRA',
    'GUARATINGUETÁ': 'GTG',
    'GUARATINGUETA': 'GTG',
    'GUARULHOS NORTE': 'GNO',
    'GUARULHOS SUL': 'GSU',
    'ITAPECERICA DA SERRA': 'ITS',
    'ITAPETININGA': 'ITN',
    'ITAPEVA': 'ITV',
    'ITAPEVI': 'ITP',
    'ITAQUAQUECETUBA': 'ITQ',
    'ITARARÉ': 'ITR',
    'ITARARE': 'ITR',
    'ITU': 'ITU',
    'JABOTICABAL': 'JAB',
    'JACAREÍ': 'JAC',
    'JACAREI': 'JAC',
    'JALES': 'JAL',
    'JAÚ': 'JAU',
    'JAU': 'JAU',
    'JOSÉ BONIFÁCIO': 'JBO',
    'JOSE BONIFACIO': 'JBO',
    'JUNDIAÍ': 'JND',
    'JUNDIAI': 'JND',
    'LESTE 1': 'LT1',
    'LESTE 2': 'LT2',
    'LESTE 3': 'LT3',
    'LESTE 4': 'LT4',
    'LESTE 5': 'LT5',
    'LIMEIRA': 'LIM',
    'LINS': 'LIN',
    'MARÍLIA': 'MAR',
    'MARILIA': 'MAR',
    'MAUÁ': 'MAU',
    'MAUA': 'MAU',
    'MIRACATU': 'MIR',
    'MIRANTE DO PARANAPANEMA': 'MPA',
    'MOGI DAS CRUZES': 'MGC',
    'MOGI MIRIM': 'MGM',
    'NORTE 1': 'NT1',
    'NORTE 2': 'NT2',
    'OSASCO': 'OSC',
    'OURINHOS': 'OUR',
    'PENÁPOLIS': 'PEN',
    'PENAPOLIS': 'PEN',
    'PINDAMONHANGABA': 'PDM',
    'PIRACICABA': 'PIR',
    'PIRAJU': 'PJU',
    'PIRASSUNUNGA': 'PRS',
    'PRESIDENTE PRUDENTE': 'PPR',
    'REGISTRO': 'REG',
    'RIBEIRÃO PRETO': 'RPT',
    'RIBEIRAO PRETO': 'RPT',
    'SANTO ANASTÁCIO': 'SAT',
    'SANTO ANASTACIO': 'SAT',
    'SANTO ANDRÉ': 'STA',
    'SANTO ANDRE': 'STA',
    'SANTOS': 'SAN',
    'SÃO BERNARDO DO CAMPO': 'SBC',
    'SAO BERNARDO DO CAMPO': 'SBC',
    'SÃO CARLOS': 'SCL',
    'SAO CARLOS': 'SCL',
    'SÃO JOÃO DA BOA VISTA': 'SJV',
    'SAO JOAO DA BOA VISTA': 'SJV',
    'SÃO JOAQUIM DA BARRA': 'SJB',
    'SAO JOAQUIM DA BARRA': 'SJB',
    'SÃO JOSÉ DO RIO PRETO': 'SJR',
    'SAO JOSE DO RIO PRETO': 'SJR',
    'SÃO JOSÉ DOS CAMPOS': 'SJC',
    'SAO JOSE DOS CAMPOS': 'SJC',
    'SÃO ROQUE': 'SRQ',
    'SAO ROQUE': 'SRQ',
    'SÃO VICENTE': 'SVI',
    'SAO VICENTE': 'SVI',
    'SERTÃOZINHO': 'SER',
    'SERTAOZINHO': 'SER',
    'SOROCABA': 'SOR',
    'SUL 1': 'SU1',
    'SUL 2': 'SU2',
    'SUL 3': 'SU3',
    'SUMARÉ': 'SUM',
    'SUMARE': 'SUM',
    'SUZANO': 'SUZ',
    'TABOÃO DA SERRA': 'TAB',
    'TABOAO DA SERRA': 'TAB',
    'TAQUARITINGA': 'TAQ',
    'TAUBATÉ': 'TAU',
    'TAUBATE': 'TAU',
    'TUPÃ': 'TUP',
    'TUPA': 'TUP',
    'VOTORANTIM': 'VOT',
    'VOTUPORANGA': 'VTP'
  };
  
  
  // Verificar mapeamentos específicos com correspondência exata ou contém todas as palavras-chave
  for (const [chave, abrev] of Object.entries(mapeamentos)) {
    // Primeiro, tentar correspondência exata
    if (nomeUpper.includes(chave)) {
      return abrev;
    }
  }
  
  // Busca mais específica para casos especiais
  if (nomeUpper.includes('CAMPINAS') && nomeUpper.includes('LESTE')) return 'CLT';
  if (nomeUpper.includes('CAMPINAS') && nomeUpper.includes('OESTE')) return 'COE';
  if (nomeUpper.includes('GUARULHOS') && nomeUpper.includes('NORTE')) return 'GNO';
  if (nomeUpper.includes('GUARULHOS') && nomeUpper.includes('SUL')) return 'GSU';
  
  // Fallback: pegar primeiras letras das palavras principais
  const palavrasIgnorar = ['DE', 'DIRETORIA', 'ENSINO', 'UNIDADE', 'REGIONAL', 'EDUCACAO'];
  const palavras = nomeUpper
    .split(' ')
    .filter(palavra => !palavrasIgnorar.includes(palavra) && palavra.length > 2);
  
  if (palavras.length === 0) return "URE";
  if (palavras.length === 1) return palavras[0].substring(0, 3);
  
  return palavras.slice(0, 2)
    .map(palavra => palavra.substring(0, 2))
    .join('');
}

// Função para inicializar mapa principal
function initializeMaps() {
  const schoolsData = window.dataModule.schoolsData();
  const getVehicleDataForDiretoria = window.dataModule.getVehicleDataForDiretoria;
  
  if (!schoolsData.length) {
    console.warn("⚠️ Dados das escolas não carregados para o mapa");
    return;
  }

  try {
    const map = L.map("map", {
      center: [-23.5, -46.6],
      zoom: 7,
      minZoom: 6,
      maxZoom: 18,
    });

    window.map = map;

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    // Adicionar contorno do estado se disponível
    const toggleBtn = document.getElementById('toggle-coordinates-btn');
    const currentMode = toggleBtn ? toggleBtn.getAttribute('data-mode') : 'simple';
    
    if (window.coordinatesReady) {
      const geoData = currentMode === 'simple' ? window.mapasp_simples : window.mapasp_completo;
      if (geoData) {
        L.geoJSON(geoData, {
          style: {
            fillColor: '#3498db',
            weight: 2,
            opacity: 1,
            color: '#2980b9',
            fillOpacity: 0.1,
            interactive: false // Não capturar eventos de mouse
          },
          pane: 'tilePane' // Colocar atrás dos marcadores
        }).addTo(map);
        console.log("✅ Contorno do estado adicionado ao mapa principal");
      }
    }

    // Adicionar marcadores das escolas
    schoolsData.forEach((school) => {
      if (school.lat && school.lng && !isNaN(school.lat) && !isNaN(school.lng)) {
        const color = school.type === 'indigena' ? '#e74c3c' : '#f39c12';
        const marker = L.circleMarker([school.lat, school.lng], {
          radius: 8,
          fillColor: color,
          color: '#fff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.8
        }).addTo(map);

        marker.bindPopup(`
          <div class="popup-escola">
            <h4>${school.name}</h4>
            <p><strong>Tipo:</strong> ${school.type === 'indigena' ? 'Indígena' : 'Quilombola'}</p>
            <p><strong>Cidade:</strong> ${school.city}</p>
            <p><strong>Distância:</strong> ${school.distance} km</p>
            <p><strong>Diretoria:</strong> ${school.diretoria}</p>
          </div>
        `);
      }
    });

    // Adicionar marcadores das diretorias
    const diretorias_escolas = [...new Set(schoolsData.map((s) => s.diretoria))];
    diretorias_escolas.forEach((diretoriaNome) => {
      const escolaRef = schoolsData.find(s => s.diretoria === diretoriaNome);
      if (escolaRef && escolaRef.de_lat && escolaRef.de_lng) {
        const veiculosInfo = getVehicleDataForDiretoria(diretoriaNome);
        const abreviacao = getDiretoriaAbbreviation(diretoriaNome);
        
        const diretoriaMarker = L.marker([escolaRef.de_lat, escolaRef.de_lng], {
          icon: L.divIcon({
            className: 'custom-div-icon',
            html: `<div style="background-color: #3498db; color: white; border-radius: 8px; width: auto; min-width: 35px; height: 25px; display: flex; align-items: center; justify-content: center; border: 2px solid white; font-weight: bold; font-size: 10px; padding: 2px 4px; white-space: nowrap;">${abreviacao}</div>`,
            iconSize: [35, 25],
            iconAnchor: [17, 12]
          })
        }).addTo(map);

        diretoriaMarker.bindPopup(`
          <div class="popup-diretoria">
            <h4>🏛️ ${diretoriaNome}</h4>
            <p><strong>Veículos:</strong> ${veiculosInfo.total}</p>
            <p><strong>Escolas atendidas:</strong> ${schoolsData.filter(s => s.diretoria === diretoriaNome).length}</p>
            <p><strong>Tipos de veículos:</strong></p>
            <ul>
              <li>S-1: ${veiculosInfo.s1 || 0}</li>
              <li>S-2: ${veiculosInfo.s2 || 0}</li>
              <li>S-2 4x4: ${veiculosInfo.s2_4x4 || 0}</li>
            </ul>
          </div>
        `);

        // Linhas conectando escolas às diretorias
        schoolsData.filter(s => s.diretoria === diretoriaNome).forEach(escola => {
          if (escola.lat && escola.lng) {
            L.polyline([
              [escola.lat, escola.lng],
              [escolaRef.de_lat, escolaRef.de_lng]
            ], {
              color: escola.type === 'indigena' ? '#e74c3c' : '#f39c12',
              weight: 2,
              opacity: 0.6,
              dashArray: '5, 10'
            }).addTo(map);
          }
        });
      }
    });

    console.log("✅ Mapa principal inicializado");
  } catch (error) {
    console.error("❌ Erro ao inicializar mapa:", error);
  }
}

// Função para mapa em tela cheia
function initializeFullscreenMap() {
  const schoolsData = window.dataModule.schoolsData();
  const getVehicleDataForDiretoria = window.dataModule.getVehicleDataForDiretoria;
  
  const fullscreenMapContainer = document.getElementById('map-fullscreen-container');
  if (!fullscreenMapContainer) {
    console.warn("⚠️ Container do mapa em tela cheia não encontrado");
    return;
  }

  if (fullscreenMap) {
    fullscreenMap.remove();
  }

  fullscreenMap = L.map('map-fullscreen-container').setView([-23.5505, -46.6333], 6);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(fullscreenMap);

  // Salvar referência global para uso nas funções de coordenadas
  window.fullscreenMap = fullscreenMap;

  // Adicionar contorno do estado se disponível
  const toggleBtn = document.getElementById('toggle-coordinates-btn');
  const currentMode = toggleBtn ? toggleBtn.getAttribute('data-mode') : 'simple';
  
  if (window.coordinatesReady) {
    const geoData = currentMode === 'simple' ? window.mapasp_simples : window.mapasp_completo;
    if (geoData) {
      window.currentFullscreenCoordinateLayer = L.geoJSON(geoData, {
        style: {
          fillColor: '#3498db',
          weight: 2,
          opacity: 1,
          color: '#2980b9',
          fillOpacity: 0.1,
          interactive: false // Não capturar eventos de mouse
        },
        pane: 'tilePane' // Colocar atrás dos marcadores
      }).addTo(fullscreenMap);
      console.log("✅ Contorno do estado adicionado ao mapa fullscreen");
    }
  }

  // Escolas
  schoolsData.forEach(school => {
    if (school.lat && school.lng) {
      const color = school.type === 'indigena' ? '#e74c3c' : '#f39c12';
      
      const marker = L.circleMarker([school.lat, school.lng], {
        radius: 8,
        fillColor: color,
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.8
      }).addTo(fullscreenMap);

      marker.bindPopup(`
        <div class="popup-escola">
          <h4>${school.name}</h4>
          <p><strong>Tipo:</strong> ${school.type === 'indigena' ? 'Indígena' : 'Quilombola'}</p>
          <p><strong>Cidade:</strong> ${school.city}</p>
          <p><strong>Distância:</strong> ${school.distance} km</p>
          <p><strong>Diretoria:</strong> ${school.diretoria}</p>
        </div>
      `);
    }
  });

  // Diretorias e linhas
  const diretorias_escolas = [...new Set(schoolsData.map((s) => s.diretoria))];
  diretorias_escolas.forEach((diretoriaNome) => {
    const escolaRef = schoolsData.find(s => s.diretoria === diretoriaNome);
    if (escolaRef && escolaRef.de_lat && escolaRef.de_lng) {
      const veiculosInfo = getVehicleDataForDiretoria(diretoriaNome);
      const abreviacao = getDiretoriaAbbreviation(diretoriaNome);
      
      const diretoriaMarker = L.marker([escolaRef.de_lat, escolaRef.de_lng], {
        icon: L.divIcon({
          className: 'custom-div-icon',
          html: `<div style="background-color: #3498db; color: white; border-radius: 8px; width: auto; min-width: 35px; height: 25px; display: flex; align-items: center; justify-content: center; border: 2px solid white; font-weight: bold; font-size: 10px; padding: 2px 4px; white-space: nowrap;">${abreviacao}</div>`,
          iconSize: [35, 25],
          iconAnchor: [17, 12]
        })
      }).addTo(fullscreenMap);

      diretoriaMarker.bindPopup(`
        <div class="popup-diretoria">
          <h4>🏛️ ${diretoriaNome}</h4>
          <p><strong>Veículos:</strong> ${veiculosInfo.total}</p>
          <p><strong>Escolas atendidas:</strong> ${schoolsData.filter(s => s.diretoria === diretoriaNome).length}</p>
          <p><strong>Tipos de veículos:</strong></p>
          <ul>
            <li>S-1: ${veiculosInfo.s1 || 0}</li>
            <li>S-2: ${veiculosInfo.s2 || 0}</li>
            <li>S-2 4x4: ${veiculosInfo.s2_4x4 || 0}</li>
          </ul>
        </div>
      `);

      // Linhas conectando
      schoolsData.filter(s => s.diretoria === diretoriaNome).forEach(escola => {
        if (escola.lat && escola.lng) {
          L.polyline([
            [escola.lat, escola.lng],
            [escolaRef.de_lat, escolaRef.de_lng]
          ], {
            color: escola.type === 'indigena' ? '#e74c3c' : '#f39c12',
            weight: 2,
            opacity: 0.6,
            dashArray: '5, 10'
          }).addTo(fullscreenMap);
        }
      });
    }
  });

  setTimeout(() => {
    fullscreenMap.invalidateSize();
  }, 100);

  console.log("🔍 Mapa tela cheia inicializado");
}

// Função para atualizar mapa principal com coordenadas
function updateMapWithCoordinates() {
  if (!window.map || !window.coordinatesReady) return;
  
  // Remover camadas existentes de coordenadas se houver
  if (window.currentCoordinateLayer) {
    window.map.removeLayer(window.currentCoordinateLayer);
  }
  
  const toggleBtn = document.getElementById('toggle-coordinates-btn');
  const currentMode = toggleBtn ? toggleBtn.getAttribute('data-mode') : 'simple';
  
  const geoData = currentMode === 'simple' ? window.mapasp_simples : window.mapasp_completo;
  
  if (geoData) {
    window.currentCoordinateLayer = L.geoJSON(geoData, {
      style: {
        fillColor: '#3498db',
        weight: 2,
        opacity: 1,
        color: '#2980b9',
        fillOpacity: 0.1,
        interactive: false // Não capturar eventos de mouse
      },
      pane: 'tilePane' // Colocar atrás dos marcadores
    }).addTo(window.map);
    console.log(`✅ Contorno ${currentMode} atualizado no mapa principal`);
  }
}

// Função para atualizar mapa fullscreen com coordenadas
function updateFullscreenMapWithCoordinates() {
  if (!window.fullscreenMap || !window.coordinatesReady) return;
  
  // Remover camadas existentes de coordenadas se houver
  if (window.currentFullscreenCoordinateLayer) {
    window.fullscreenMap.removeLayer(window.currentFullscreenCoordinateLayer);
  }
  
  const toggleBtn = document.getElementById('toggle-coordinates-btn');
  const currentMode = toggleBtn ? toggleBtn.getAttribute('data-mode') : 'simple';
  
  const geoData = currentMode === 'simple' ? window.mapasp_simples : window.mapasp_completo;
  
  if (geoData) {
    window.currentFullscreenCoordinateLayer = L.geoJSON(geoData, {
      style: {
        fillColor: '#3498db',
        weight: 2,
        opacity: 1,
        color: '#2980b9',
        fillOpacity: 0.1,
        interactive: false // Não capturar eventos de mouse
      },
      pane: 'tilePane' // Colocar atrás dos marcadores
    }).addTo(window.fullscreenMap);
    console.log(`✅ Contorno ${currentMode} atualizado no mapa fullscreen`);
  }
}

// Escutar evento de coordenadas carregadas
document.addEventListener('coordinatesLoaded', () => {
  console.log("🎯 Coordenadas carregadas, atualizando mapas...");
  updateMapWithCoordinates();
  updateFullscreenMapWithCoordinates();
});

// Função para alternar coordenadas
function toggleCoordinates() {
  const toggleBtn = document.getElementById('toggle-coordinates-btn');
  if (!toggleBtn) return;
  
  const currentMode = toggleBtn.getAttribute('data-mode');
  const newMode = currentMode === 'simple' ? 'complete' : 'simple';
  
  toggleBtn.setAttribute('data-mode', newMode);
  toggleBtn.textContent = newMode === 'simple' ? 'Coordenadas Simples' : 'Coordenadas Completas';
  
  // Atualizar ambos os mapas se disponíveis
  updateMapWithCoordinates();
  updateFullscreenMapWithCoordinates();
  
  console.log(`🔄 Coordenadas alteradas para modo: ${newMode}`);
}

// Exportar funções
window.mapModule = {
  initializeMaps,
  initializeFullscreenMap,
  toggleCoordinates
};
