# -*- coding: utf-8 -*-
"""
Inicialização dos Modelos
"""

from .escola import Escola
from .diretoria import Diretoria
from .veiculo import Veiculo
from .supervisor import Supervisor
from .distancia import Distancia

# Modelos expandidos
try:
    from .models_expandidos import (
        Diretoria as DiretoriaExpandida,
        Escola as EscolaExpandida,
        Veiculo as VeiculoExpandido,
        Supervisor as SupervisorExpandido,
        Distancia as DistanciaExpandida,
        EstatisticasGerais
    )
    __all__ = [
        'Escola', 'Diretoria', 'Veiculo', 'Supervisor', 'Distancia',
        'DiretoriaExpandida', 'EscolaExpandida', 'VeiculoExpandido',
        'SupervisorExpandido', 'DistanciaExpandida', 'EstatisticasGerais'
    ]
except ImportError:
    __all__ = ['Escola', 'Diretoria', 'Veiculo', 'Supervisor', 'Distancia']
