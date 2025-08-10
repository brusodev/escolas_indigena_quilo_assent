import { mapasp_completo } from "./coordenadas_completa.js";
import { mapasp_simples } from "./coordenadas_simples.js";

// Função para normalizar nomes de diretorias
function normalizeDiretoriaName(name) {
  if (!name) return "";

  // Converter para maiúsculo e remover espaços extras (manter acentos)
  let normalized = name.toUpperCase().trim();

  // Mapeamentos específicos para casos especiais
  const mappings = {
    "SAO VICENTE": "SÃO VICENTE ",
    "SÃO VICENTE": "SÃO VICENTE ",
    "SAO BERNARDO DO CAMPO": "SÃO BERNARDO DO CAMPO",
    "SANTO ANASTACIO": "SANTO ANASTÁCIO",
    PENAPOLIS: "PENÁPOLIS",
    TUPA: "TUPÃ",
    ITARARE: "ITARARÉ",
    "LESTE 5": "LESTE 5",
  };

  // Aplicar mapeamentos
  for (const [original, replacement] of Object.entries(mappings)) {
    if (normalized.includes(original)) {
      normalized = normalized.replace(original, replacement);
    }
  }

  return normalized;
}

// ===================================================
// CARREGAMENTO DINÂMICO DE DADOS
// ===================================================

// Variáveis globais para dados
let schoolsData = [];
let vehicleData = null;

// Função para carregar dados das escolas do JSON
async function loadSchoolsData() {
  try {
    console.log("🔄 Carregando dados das escolas do JSON...");
    const response = await fetch("dados/json/dados_escolas_atualizados.json");
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    schoolsData = await response.json();
    console.log(`✅ ${schoolsData.length} escolas carregadas do JSON`);
    
    // Verificar tipos
    const indigenas = schoolsData.filter(s => s.type === 'indigena').length;
    const quilombolas = schoolsData.filter(s => s.type === 'quilombola').length;
    console.log(`📊 Tipos: ${indigenas} indígenas + ${quilombolas} quilombolas`);
    
    return schoolsData;
  } catch (error) {
    console.error("❌ Erro ao carregar dados das escolas:", error);
    
    // Fallback: dados mínimos em caso de erro
    schoolsData = [
      {
        name: "ERRO - Dados não carregados",
        type: "erro",
        city: "N/A",
        diretoria: "N/A",
        distance: 0,
        lat: -23.5,
        lng: -46.6
      }
    ];
    
    return schoolsData;
  }
}

// Função para carregar dados de veículos
async function loadVehicleData() {
  try {
    console.log("🔄 Carregando dados de veículos...");
    const response = await fetch("dados_veiculos_diretorias.json");
    const data = await response.json();
    
    vehicleData = data;
    console.log(`✅ Dados de veículos carregados: ${data.metadata.total_veiculos} veículos`);
    
    return data;
  } catch (error) {
    console.error("❌ Erro ao carregar dados de veículos:", error);
    return null;
  }
}

// Função para obter dados de veículos de uma diretoria
function getVehicleDataForDiretoria(diretoriaNome) {
  if (!vehicleData) {
    return { total: 0, s1: 0, s2: 0, s2_4x4: 0 };
  }

  const normalizedName = normalizeDiretoriaName(diretoriaNome);

  // Buscar diretamente na estrutura de dados
  for (const [key, data] of Object.entries(vehicleData.diretorias)) {
    const normalizedKey = normalizeDiretoriaName(key);
    if (normalizedKey === normalizedName) {
      return data;
    }
  }

  console.warn(`⚠️ Diretoria não encontrada: ${diretoriaNome}`);
  return { total: 0, s1: 0, s2: 0, s2_4x4: 0 };
}

// ===================================================
// FUNÇÕES DE INICIALIZAÇÃO
// ===================================================

// Função para gerar lista de escolas
function generateSchoolList() {
  const schoolList = document.getElementById('school-list');
  if (!schoolList) {
    console.warn("⚠️ Elemento school-list não encontrado");
    return;
  }

  // Ordenar escolas por distância (prioridade)
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
        <span class="priority-badge priority-${priorityClass}">
          ${priorityText}
        </span>
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
    
    // Adicionar evento de clique para focar no mapa
    schoolItem.addEventListener('click', function() {
      focusSchoolOnMap(school);
    });
    
    schoolList.appendChild(schoolItem);
  });

  console.log(`📋 Lista de escolas gerada: ${sortedSchools.length} escolas`);
}

// Função para focar uma escola no mapa
function focusSchoolOnMap(school) {
  if (!school.lat || !school.lng) {
    console.warn("⚠️ Coordenadas da escola não encontradas:", school.name);
    return;
  }

  // Verificar se existe mapa principal
  const mapContainer = document.getElementById('map-container');
  if (mapContainer && window.map) {
    // Focar no mapa principal
    window.map.setView([school.lat, school.lng], 12);
    
    // Encontrar e abrir popup da escola
    window.map.eachLayer(function(layer) {
      if (layer.getLatLng && layer.getPopup) {
        const latlng = layer.getLatLng();
        if (Math.abs(latlng.lat - school.lat) < 0.001 && Math.abs(latlng.lng - school.lng) < 0.001) {
          layer.openPopup();
        }
      }
    });
    
    console.log(`📍 Focando escola no mapa: ${school.name}`);
  } else {
    console.warn("⚠️ Mapa principal não encontrado");
  }
}

// Função para atualizar contadores da legenda
function updateLegendCounts() {
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

  console.log(`📊 Legenda atualizada: ${indigenas} indígenas, ${quilombolas} quilombolas, ${diretorias} diretorias, ${totalVehiclesRelevantes} veículos`);
}

// Calcular estatísticas
function calculateStats() {
  if (!schoolsData.length) {
    console.warn("⚠️ Dados das escolas não carregados");
    return;
  }

  // Calcular veículos relevantes - apenas das diretorias que atendem as escolas
  const diretorias_escolas = [...new Set(schoolsData.map((s) => s.diretoria))];
  let totalVehiclesRelevantes = 0;

  diretorias_escolas.forEach((diretoria) => {
    const dados = getVehicleDataForDiretoria(diretoria);
    totalVehiclesRelevantes += dados.total;
  });

  const highPrioritySchools = schoolsData.filter((s) => s.distance > 50).length;
  const uniqueDiretorias = [...new Set(schoolsData.map((s) => s.diretoria))].length;

  // Atualizar interface
  const totalVehiclesElement = document.getElementById("total-vehicles");
  const highPriorityElement = document.getElementById("high-priority");
  const diretoriasElement = document.getElementById("total-diretorias");

  if (totalVehiclesElement) totalVehiclesElement.textContent = totalVehiclesRelevantes;
  if (highPriorityElement) highPriorityElement.textContent = highPrioritySchools;
  if (diretoriasElement) diretoriasElement.textContent = uniqueDiretorias;

  console.log(
    `🔢 Estatísticas calculadas: ${totalVehiclesRelevantes} veículos relevantes, ${uniqueDiretorias} diretorias`
  );
}

// Inicializar mapas
function initializeMaps() {
  if (!schoolsData.length) {
    console.warn("⚠️ Dados das escolas não carregados para o mapa");
    return;
  }

  try {
    // Configuração do mapa
    const mapConfig = {
      center: [-23.5, -46.6],
      zoom: 7,
      minZoom: 6,
      maxZoom: 18,
    };

    // Inicializar mapa
    const map = L.map("map", {
      center: mapConfig.center,
      zoom: mapConfig.zoom,
      minZoom: mapConfig.minZoom,
      maxZoom: mapConfig.maxZoom,
    });

    // Tornar mapa acessível globalmente
    window.map = map;

    // Adicionar camada base
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    // Adicionar marcadores das escolas com cores corretas da legenda
    schoolsData.forEach((school) => {
      if (school.lat && school.lng && !isNaN(school.lat) && !isNaN(school.lng)) {
        // Cores conforme a legenda: vermelha para indígena, laranja para quilombola
        const color = school.type === 'indigena' ? '#e74c3c' : '#f39c12';
        const marker = L.circleMarker([school.lat, school.lng], {
          radius: 8,
          fillColor: color,
          color: '#fff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.8
        }).addTo(map);

        // Popup com informações
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
      // Pegar primeira escola da diretoria para obter coordenadas da DE
      const escolaRef = schoolsData.find(s => s.diretoria === diretoriaNome);
      if (escolaRef && escolaRef.de_lat && escolaRef.de_lng) {
        const veiculosInfo = getVehicleDataForDiretoria(diretoriaNome);
        
        // Marcador azul para diretorias
        const diretoriaMarker = L.marker([escolaRef.de_lat, escolaRef.de_lng], {
          icon: L.divIcon({
            className: 'custom-div-icon',
            html: `<div style="background-color: #3498db; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border: 2px solid white; font-weight: bold;">DE</div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
          })
        }).addTo(map);

        // Popup da diretoria
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

        // Adicionar linhas conectando escolas às diretorias
        schoolsData.filter(s => s.diretoria === diretoriaNome).forEach(escola => {
          if (escola.lat && escola.lng) {
            const linha = L.polyline([
              [escola.lat, escola.lng],
              [escolaRef.de_lat, escolaRef.de_lng]
            ], {
              color: escola.type === 'indigena' ? '#e74c3c' : '#f39c12',
              weight: 2,
              opacity: 0.6,
              dashArray: '5, 5'
            }).addTo(map);
          }
        });
      }
    });

    // Gerar lista de escolas na sidebar
    generateSchoolList();

    console.log("✅ Mapa inicializado com sucesso");

  } catch (error) {
    console.error("❌ Erro ao inicializar mapa:", error);
    // Continuar sem o mapa em caso de erro
  }
}

// Gerar gráficos
function generateCharts() {
  if (!schoolsData.length) {
    console.warn("⚠️ Dados das escolas não carregados para gráficos");
    return;
  }

  // Obter diretorias únicas das escolas
  const diretorias_escolas = [...new Set(schoolsData.map((s) => s.diretoria))];
  
  // Calcular dados para gráfico de veículos vs demanda
  const diretoriasData = [];
  const veiculosData = [];
  const escolasData = [];

  diretorias_escolas.forEach((diretoria) => {
    const escolasDiretoria = schoolsData.filter(s => s.diretoria === diretoria).length;
    const veiculosDiretoria = getVehicleDataForDiretoria(diretoria).total;
    
    diretoriasData.push(diretoria);
    veiculosData.push(veiculosDiretoria);
    escolasData.push(escolasDiretoria);
  });

  // Gráfico 1: Veículos vs Demanda por Diretoria
  const ctx1 = document.getElementById('vehicleChart');
  if (ctx1) {
    new Chart(ctx1, {
      type: 'bar',
      data: {
        labels: diretoriasData,
        datasets: [
          {
            label: 'Veículos',
            data: veiculosData,
            backgroundColor: '#3498db',
            borderColor: '#2980b9',
            borderWidth: 1
          },
          {
            label: 'Escolas',
            data: escolasData,
            backgroundColor: '#e74c3c',
            borderColor: '#c0392b',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top'
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }

  // Gráfico 2: Prioridade de Atendimento (por distância)
  const distancias = schoolsData.map(s => s.distance || 0);
  const ctx2 = document.getElementById('priorityChart');
  if (ctx2) {
    new Chart(ctx2, {
      type: 'doughnut',
      data: {
        labels: ['0-25 km', '25-50 km', '50+ km'],
        datasets: [{
          data: [
            distancias.filter(d => d <= 25).length,
            distancias.filter(d => d > 25 && d <= 50).length,
            distancias.filter(d => d > 50).length
          ],
          backgroundColor: ['#27ae60', '#f39c12', '#e74c3c'],
          borderWidth: 2,
          borderColor: '#fff'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    });
  }

  // Gráfico 3: Distribuição de Veículos (tipos)
  const ctx3 = document.getElementById('vehicleDistributionChart');
  if (ctx3) {
    new Chart(ctx3, {
      type: 'pie',
      data: {
        labels: ['Indígenas', 'Quilombolas'],
        datasets: [{
          data: [
            schoolsData.filter(s => s.type === 'indigena').length,
            schoolsData.filter(s => s.type === 'quilombola').length
          ],
          backgroundColor: ['#e74c3c', '#f39c12'],
          borderWidth: 2,
          borderColor: '#fff'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    });
  }

  console.log("📊 Gráficos gerados com sucesso!");
}

// ===================================================
// EVENT LISTENERS E INTERAÇÕES
// ===================================================

function setupEventListeners() {
  // Filtros de escola
  const filterButtons = document.querySelectorAll('.filter-btn');
  filterButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      // Remover active de todos
      filterButtons.forEach(b => b.classList.remove('active'));
      // Adicionar active ao clicado
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
        // Recriar mapa em tela cheia
        initializeFullscreenMap();
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

  // Controle de coordenadas
  const toggleCoordinatesBtn = document.getElementById('toggle-coordinates-btn');
  if (toggleCoordinatesBtn) {
    toggleCoordinatesBtn.addEventListener('click', function() {
      const currentMode = this.getAttribute('data-mode');
      const newMode = currentMode === 'simple' ? 'complete' : 'simple';
      
      this.setAttribute('data-mode', newMode);
      this.querySelector('.btn-text').textContent = 
        newMode === 'simple' ? 'Mostrar Municípios' : 'Ocultar Municípios';
      
      // Atualizar info
      const coordinatesInfo = document.getElementById('coordinates-info');
      if (coordinatesInfo) {
        coordinatesInfo.textContent = 
          newMode === 'simple' ? 'Modo: Contorno do Estado' : 'Modo: Municípios Visíveis';
      }
      
      // Recriar mapa com novo modo
      initializeMaps();
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

let fullscreenMap = null;

function initializeFullscreenMap() {
  const fullscreenMapContainer = document.getElementById('map-fullscreen-container');
  if (!fullscreenMapContainer) {
    console.warn("⚠️ Container do mapa em tela cheia não encontrado");
    return;
  }

  // Limpar mapa anterior se existir
  if (fullscreenMap) {
    fullscreenMap.remove();
  }

  // Criar novo mapa
  fullscreenMap = L.map('map-fullscreen-container').setView([-23.5505, -46.6333], 6);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(fullscreenMap);

  // Adicionar polígono do estado de São Paulo
  const toggleBtn = document.getElementById('toggle-coordinates-btn');
  const currentMode = toggleBtn ? toggleBtn.getAttribute('data-mode') : 'simple';
  
  let geoData = currentMode === 'simple' ? mapasp_simples : mapasp_completo;
  
  // Adicionar polígono do estado com estilo
  L.geoJSON(geoData, {
    style: {
      fillColor: '#3498db',
      weight: 2,
      opacity: 1,
      color: '#2980b9',
      fillOpacity: 0.1
    }
  }).addTo(fullscreenMap);

  // Adicionar marcadores das escolas
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

  // Adicionar marcadores das diretorias
  const diretorias_escolas = [...new Set(schoolsData.map((s) => s.diretoria))];
  diretorias_escolas.forEach((diretoriaNome) => {
    const escolaRef = schoolsData.find(s => s.diretoria === diretoriaNome);
    if (escolaRef && escolaRef.de_lat && escolaRef.de_lng) {
      const veiculosInfo = getVehicleDataForDiretoria(diretoriaNome);
      
      // Marcador azul para diretorias
      const diretoriaMarker = L.marker([escolaRef.de_lat, escolaRef.de_lng], {
        icon: L.divIcon({
          className: 'custom-div-icon',
          html: `<div style="background-color: #3498db; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border: 2px solid white; font-weight: bold;">DE</div>`,
          iconSize: [30, 30],
          iconAnchor: [15, 15]
        })
      }).addTo(fullscreenMap);

      // Popup da diretoria
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

      // Adicionar linhas conectando escolas às diretorias
      schoolsData.filter(s => s.diretoria === diretoriaNome).forEach(escola => {
        if (escola.lat && escola.lng) {
          const linha = L.polyline([
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

  // Redimensionar mapa após pequeno delay
  setTimeout(() => {
    fullscreenMap.invalidateSize();
  }, 100);

  console.log("🔍 Mapa em tela cheia inicializado com todos os elementos");
}

// ===================================================
// INICIALIZAÇÃO PRINCIPAL
// ===================================================

// Função principal de inicialização
async function initializeDashboard() {
  try {
    console.log("🚀 Inicializando dashboard...");
    
    // Carregar dados
    await loadSchoolsData();
    await loadVehicleData();
    
    // Inicializar componentes
    calculateStats();
    updateLegendCounts();
    initializeMaps();
    generateSchoolList();
    generateCharts();
    setupEventListeners();
    
    console.log("✅ Dashboard inicializado com sucesso!");
    
  } catch (error) {
    console.error("❌ Erro ao inicializar dashboard:", error);
  }
}

// Aguardar carregamento do DOM e inicializar
document.addEventListener('DOMContentLoaded', initializeDashboard);

// Exportar funções para uso global
window.dashboard = {
  initialize: initializeDashboard,
  loadSchoolsData,
  loadVehicleData,
  calculateStats,
  initializeMaps,
  generateCharts
};

console.log("📜 Dashboard JavaScript carregado - versão dinâmica");
