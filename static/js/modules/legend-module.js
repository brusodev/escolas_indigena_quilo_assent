// ===================================================
// MÓDULO: LEGENDA DINÂMICA
// ===================================================

// Função para contar escolas por tipo
function countSchoolsByType(schools) {
  if (!schools || !schools.length) {
    return {};
  }

  const counts = {};
  schools.forEach(school => {
    const type = school.type || 'sem_tipo';
    counts[type] = (counts[type] || 0) + 1;
  });

  return counts;
}

// Função para contar diretorias únicas
function countUniqueDirectorias(schools) {
  if (!schools || !schools.length) {
    return 0;
  }

  const diretorias = new Set(schools.map(school => school.diretoria).filter(Boolean));
  return diretorias.size;
}

// Função para atualizar contadores na legenda
function updateLegendCounts(schools) {
  if (!schools || !schools.length) {
    console.warn('⚠️ Dados de escolas não disponíveis para legenda');
    return;
  }

  const typeCounts = countSchoolsByType(schools);
  const totalDirectorias = countUniqueDirectorias(schools);

  // Atualizar contadores específicos
  const updates = [
    { id: 'indigena-count', value: typeCounts.indigena || 0 },
    { id: 'quilombola-count', value: typeCounts.quilombola || 0 },
    { id: 'regular-count', value: typeCounts.regular || 0 },
    { id: 'diretorias-count', value: totalDirectorias }
  ];

  updates.forEach(update => {
    const element = document.getElementById(update.id);
    if (element) {
      element.textContent = update.value.toLocaleString();
    }
  });

  // Atualizar contadores de outros tipos
  const otherTypes = Object.keys(typeCounts).filter(
    type => !['indigena', 'quilombola', 'regular'].includes(type)
  );
  
  const otherCount = otherTypes.reduce((sum, type) => sum + typeCounts[type], 0);
  const otherCountElement = document.getElementById('outros-count');
  if (otherCountElement) {
    otherCountElement.textContent = otherCount.toLocaleString();
  }

  console.log(`📊 Legenda atualizada:`, {
    indigena: typeCounts.indigena || 0,
    quilombola: typeCounts.quilombola || 0,
    regular: typeCounts.regular || 0,
    outros: otherCount,
    diretorias: totalDirectorias
  });
}

// Função para criar lista detalhada de tipos
function createDetailedTypeLegend(schools) {
  if (!schools || !schools.length) {
    return '';
  }

  const typeCounts = countSchoolsByType(schools);
  const getSchoolEmoji = window.schoolMarkersModule?.getSchoolEmoji || (() => '📚');
  const getSchoolTypeName = window.schoolMarkersModule?.getSchoolTypeName || (type => type);

  let html = '<div class="detailed-type-legend">';
  
  // Ordenar tipos por quantidade
  const sortedTypes = Object.entries(typeCounts)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 6); // Mostrar apenas os 6 principais

  sortedTypes.forEach(([type, count]) => {
    const emoji = getSchoolEmoji(type);
    const name = getSchoolTypeName(type);
    const percentage = ((count / schools.length) * 100).toFixed(1);
    
    html += `
      <div class="legend-type-item" style="margin: 5px 0; display: flex; justify-content: space-between;">
        <span>${emoji} ${name}</span>
        <span style="font-weight: bold;">${count.toLocaleString()} (${percentage}%)</span>
      </div>
    `;
  });

  // Mostrar outros tipos agrupados se houver
  const otherTypes = Object.entries(typeCounts).slice(6);
  if (otherTypes.length > 0) {
    const otherCount = otherTypes.reduce((sum, [,count]) => sum + count, 0);
    const otherPercentage = ((otherCount / schools.length) * 100).toFixed(1);
    
    html += `
      <div class="legend-type-item" style="margin: 5px 0; display: flex; justify-content: space-between;">
        <span>📚 Outros</span>
        <span style="font-weight: bold;">${otherCount.toLocaleString()} (${otherPercentage}%)</span>
      </div>
    `;
  }

  html += '</div>';
  return html;
}

// Função para atualizar estatísticas gerais
function updateGeneralStats(schools) {
  if (!schools || !schools.length) {
    console.warn('⚠️ Dados de escolas não disponíveis para estatísticas');
    return;
  }

  const totalSchools = schools.length;
  const totalDirectorias = countUniqueDirectorias(schools);
  
  // Calcular escolas de alta prioridade (distância > 50km)
  const highPrioritySchools = schools.filter(school => 
    school.distance && school.distance > 50
  ).length;

  // Calcular distância média
  const schoolsWithDistance = schools.filter(school => school.distance && school.distance > 0);
  const avgDistance = schoolsWithDistance.length > 0 
    ? schoolsWithDistance.reduce((sum, school) => sum + school.distance, 0) / schoolsWithDistance.length
    : 0;

  // Atualizar elementos na página
  const updates = [
    { id: 'total-schools', value: totalSchools.toLocaleString() },
    { id: 'total-diretorias', value: totalDirectorias },
    { id: 'high-priority', value: highPrioritySchools.toLocaleString() },
    { id: 'avg-distance', value: avgDistance.toFixed(1) }
  ];

  updates.forEach(update => {
    const element = document.getElementById(update.id);
    if (element) {
      element.textContent = update.value;
    }
  });

  console.log(`📈 Estatísticas gerais atualizadas:`, {
    totalSchools,
    totalDirectorias,
    highPrioritySchools,
    avgDistance: avgDistance.toFixed(1)
  });
}

// Função principal para atualizar toda a legenda
function updateCompleteLegend(schools) {
  if (!schools || !schools.length) {
    console.warn('⚠️ Não é possível atualizar legenda sem dados');
    return;
  }

  updateLegendCounts(schools);
  updateGeneralStats(schools);
  
  console.log(`✅ Legenda completa atualizada para ${schools.length} escolas`);
}

// Exportar funções
window.legendModule = {
  countSchoolsByType,
  countUniqueDirectorias,
  updateLegendCounts,
  createDetailedTypeLegend,
  updateGeneralStats,
  updateCompleteLegend
};

console.log('📊 Módulo de legenda carregado');
