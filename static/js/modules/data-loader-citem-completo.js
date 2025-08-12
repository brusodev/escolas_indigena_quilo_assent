// ===================================================
// MÓDULO: CARREGAMENTO DE DADOS - VERSÃO CITEM COMPLETA
// ===================================================
// ATUALIZADO: 11/08/2025 - Integração das 5.582 escolas
// FONTE: Base completa CITEM com todos os tipos de escola
// TIPOS DISPONÍVEIS: regular, indigena, quilombola, assentamento, ceeja, cel_jto, hospitalar, escola_penitenciaria, centro_atend_socioeduc, centro_atend_soc_educ_adolesc
// ===================================================

// Variáveis globais para dados
let schoolsData = [];
let vehicleData = null;

// Função para normalizar nomes de diretorias
function normalizeDiretoriaName(name) {
  if (!name) return "";

  let normalized = name.toUpperCase().trim();

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

  for (const [original, replacement] of Object.entries(mappings)) {
    if (normalized.includes(original)) {
      normalized = normalized.replace(original, replacement);
    }
  }

  return normalized;
}

// Função para carregar dados das escolas
async function loadSchoolsData() {
  try {
    console.log("🔄 Carregando dados das escolas...");
    const response = await fetch("dados/json/dados_escolas_atualizados_completo.json");
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    schoolsData = await response.json();
    console.log(`✅ ${schoolsData.length} escolas carregadas`);
    
    return schoolsData;
  } catch (error) {
    console.error("❌ Erro ao carregar dados das escolas:", error);
    schoolsData = [{
      name: "ERRO - Dados não carregados",
      type: "erro",
      city: "N/A",
      diretoria: "N/A",
      distance: 0,
      lat: -23.5,
      lng: -46.6
    }];
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

  for (const [key, data] of Object.entries(vehicleData.diretorias)) {
    const normalizedKey = normalizeDiretoriaName(key);
    if (normalizedKey === normalizedName) {
      return data;
    }
  }

  console.warn(`⚠️ Diretoria não encontrada: ${diretoriaNome}`);
  return { total: 0, s1: 0, s2: 0, s2_4x4: 0 };
}

// Exportar funções
window.dataModule = {
  schoolsData: () => schoolsData,
  vehicleData: () => vehicleData,
  loadSchoolsData,
  loadVehicleData,
  getVehicleDataForDiretoria,
  normalizeDiretoriaName
};
