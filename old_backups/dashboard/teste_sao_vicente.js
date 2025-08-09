
    // Teste para o console do browser
    console.log('=== TESTE SÃO VICENTE ===');
    console.log('Diretorias no vehicleData:', Object.keys(vehicleData).length);
    console.log('Total de veículos:', Object.values(vehicleData).reduce((sum, v) => sum + v.total, 0));
    
    // Testar São Vicente
    const testKeys = ['SAO VICENTE', 'SÃO VICENTE', 'São Vicente'.toUpperCase()];
    testKeys.forEach(key => {
        if (vehicleData[key]) {
            console.log(`✅ ${key}:`, vehicleData[key]);
        } else {
            console.log(`❌ ${key}: não encontrado`);
        }
    });
    
    // Mostrar todas as chaves que contêm 'VICENTE'
    const vicenteKeys = Object.keys(vehicleData).filter(k => k.includes('VICENTE'));
    console.log('Chaves contendo VICENTE:', vicenteKeys);
    