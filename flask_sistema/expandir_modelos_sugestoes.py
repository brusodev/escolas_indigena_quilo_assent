# -*- coding: utf-8 -*-
"""
Script para atualizar modelos Flask com campos expandidos
"""

# Campos adicionais para o modelo Diretoria:
campos_diretoria = """
    # Informações geográficas
    cidade = db.Column(db.String(100))
    cep = db.Column(db.String(10))
    codigo = db.Column(db.String(20))
    
    # Estatísticas
    total_escolas = db.Column(db.Integer, default=0)
    escolas_indigenas = db.Column(db.Integer, default=0)
    escolas_quilombolas = db.Column(db.Integer, default=0)
    escolas_regulares = db.Column(db.Integer, default=0)
    
    # Supervisão
    supervisor = db.Column(db.String(200))
    regiao_supervisao = db.Column(db.String(100))
"""

# Campos adicionais para o modelo Veiculo:
campos_veiculo = """
    # Detalhamento do veículo
    categoria = db.Column(db.String(50))  # pequeno, medio_grande, medio_grande_4x4
    descricao_completa = db.Column(db.Text)
    capacidade_estimada = db.Column(db.Integer)
    necessidade_especial = db.Column(db.Boolean, default=False)
"""

# Campos adicionais para o modelo Escola:
campos_escola = """
    # Códigos identificadores
    codigo = db.Column(db.Integer)
    codigo_mec = db.Column(db.String(20))
    codigo_ibge = db.Column(db.Integer)
    
    # Informações administrativas
    zona = db.Column(db.String(20))  # Urbana, Rural
    situacao = db.Column(db.Integer)  # 1=Ativa, etc
    
    # Campos extras para relatórios
    tipo_original = db.Column(db.String(50))
"""

print("📋 Campos sugeridos para expansão dos modelos:")
print("\n1. DIRETORIA:")
print(campos_diretoria)
print("\n2. VEICULO:")
print(campos_veiculo)
print("\n3. ESCOLA:")
print(campos_escola)
