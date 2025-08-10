// ===================================================
// MÓDULO: GRÁFICOS
// ===================================================

// Gerar gráficos
function generateCharts() {
  const schoolsData = window.dataModule.schoolsData();
  const getVehicleDataForDiretoria = window.dataModule.getVehicleDataForDiretoria;
  
  if (!schoolsData.length) {
    console.warn("⚠️ Dados das escolas não carregados para gráficos");
    return;
  }

  // Gráfico de Veículos vs Demanda
  const diretorias_escolas = [...new Set(schoolsData.map((s) => s.diretoria))];
  
  const labels = [];
  const veiculosData = [];
  const escolasData = [];

  diretorias_escolas.forEach((diretoria) => {
    const dadosVeiculos = getVehicleDataForDiretoria(diretoria);
    const escolasDiretoria = schoolsData.filter(s => s.diretoria === diretoria).length;
    
    labels.push(diretoria.length > 15 ? diretoria.substring(0, 15) + '...' : diretoria);
    veiculosData.push(dadosVeiculos.total);
    escolasData.push(escolasDiretoria);
  });

  // Gráfico 1: Veículos vs Demanda
  const vehicleChart = document.getElementById('vehicleChart');
  if (vehicleChart) {
    new Chart(vehicleChart.getContext('2d'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Veículos Disponíveis',
            data: veiculosData,
            backgroundColor: '#3498db',
            borderColor: '#2980b9',
            borderWidth: 1
          },
          {
            label: 'Escolas Atendidas',
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

  // Gráfico 2: Prioridade por Distância
  const distancias = schoolsData.map(s => s.distance || 0);
  const priorityChart = document.getElementById('priorityChart');
  if (priorityChart) {
    new Chart(priorityChart.getContext('2d'), {
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

  // Gráfico 3: Distribuição por Tipo
  const vehicleDistributionChart = document.getElementById('vehicleDistributionChart');
  if (vehicleDistributionChart) {
    new Chart(vehicleDistributionChart.getContext('2d'), {
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

// Exportar funções
window.chartsModule = {
  generateCharts
};
