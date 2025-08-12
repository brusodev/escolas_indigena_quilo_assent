# -*- coding: utf-8 -*-
"""
Modelos Flask Expandidos com Informações Completas
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Diretoria(db.Model):
    """Modelo expandido para Diretorias de Ensino"""
    __tablename__ = 'diretorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    
    # Informações geográficas
    endereco = db.Column(db.Text)
    cidade = db.Column(db.String(100))
    cep = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    codigo = db.Column(db.String(20))
    
    # Estatísticas de escolas
    total_escolas = db.Column(db.Integer, default=0)
    escolas_indigenas = db.Column(db.Integer, default=0)
    escolas_quilombolas = db.Column(db.Integer, default=0)
    escolas_regulares = db.Column(db.Integer, default=0)
    
    # Supervisão
    supervisor = db.Column(db.String(200))
    regiao_supervisao = db.Column(db.String(100))
    
    # Veículos
    total_veiculos = db.Column(db.Integer, default=0)
    
    # Relacionamentos
    escolas = db.relationship('Escola', backref='diretoria_obj', lazy=True)
    veiculos = db.relationship('Veiculo', backref='diretoria_obj', lazy=True)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'cep': self.cep,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'codigo': self.codigo,
            'total_escolas': self.total_escolas,
            'escolas_indigenas': self.escolas_indigenas,
            'escolas_quilombolas': self.escolas_quilombolas,
            'escolas_regulares': self.escolas_regulares,
            'supervisor': self.supervisor,
            'regiao_supervisao': self.regiao_supervisao,
            'total_veiculos': self.total_veiculos,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
        }
    
    def to_dict_completo(self):
        """Retorna dados completos incluindo escolas e veículos"""
        data = self.to_dict()
        data['escolas'] = [escola.to_dict() for escola in self.escolas]
        data['veiculos'] = [veiculo.to_dict() for veiculo in self.veiculos]
        return data

class Escola(db.Model):
    """Modelo expandido para Escolas"""
    __tablename__ = 'escolas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    
    # Códigos identificadores
    codigo = db.Column(db.Integer, index=True)
    codigo_mec = db.Column(db.String(20), index=True)
    codigo_ibge = db.Column(db.Integer)
    
    # Tipo e características
    tipo = db.Column(db.String(20), nullable=False)  # indigena, quilombola, regular
    tipo_original = db.Column(db.String(50))
    zona = db.Column(db.String(20))  # Urbana, Rural
    situacao = db.Column(db.Integer, default=1)  # 1=Ativa
    
    # Localização
    cidade = db.Column(db.String(100))
    endereco = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Relacionamento com diretoria
    diretoria_id = db.Column(db.Integer, db.ForeignKey('diretorias.id'), nullable=False)
    diretoria_nome = db.Column(db.String(100))  # Nome da diretoria para facilitar consultas
    
    # Distância até a diretoria
    distancia_diretoria = db.Column(db.Float)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'codigo': self.codigo,
            'codigo_mec': self.codigo_mec,
            'codigo_ibge': self.codigo_ibge,
            'tipo': self.tipo,
            'tipo_original': self.tipo_original,
            'zona': self.zona,
            'situacao': self.situacao,
            'cidade': self.cidade,
            'endereco': self.endereco,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'diretoria_id': self.diretoria_id,
            'diretoria_nome': self.diretoria_nome,
            'distancia_diretoria': self.distancia_diretoria,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
        }

class Veiculo(db.Model):
    """Modelo expandido para Veículos"""
    __tablename__ = 'veiculos'
    
    id = db.Column(db.Integer, primary_key=True)
    diretoria_id = db.Column(db.Integer, db.ForeignKey('diretorias.id'), nullable=False)
    diretoria_nome = db.Column(db.String(100))
    
    # Tipo e categoria
    tipo = db.Column(db.String(20), nullable=False)  # S-1, S-2, S-2 4X4
    categoria = db.Column(db.String(50))  # pequeno, medio_grande, medio_grande_4x4
    descricao = db.Column(db.Text)
    
    # Capacidades
    capacidade_estimada = db.Column(db.Integer)
    necessidade_especial = db.Column(db.Boolean, default=False)  # Tração 4x4
    
    # Quantidade (para este modelo, sempre será 1 por registro)
    quantidade = db.Column(db.Integer, default=1)
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'diretoria_id': self.diretoria_id,
            'diretoria_nome': self.diretoria_nome,
            'tipo': self.tipo,
            'categoria': self.categoria,
            'descricao': self.descricao,
            'capacidade_estimada': self.capacidade_estimada,
            'necessidade_especial': self.necessidade_especial,
            'quantidade': self.quantidade,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
        }

class Supervisor(db.Model):
    """Modelo expandido para Supervisores"""
    __tablename__ = 'supervisores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    regiao = db.Column(db.String(100), nullable=False)
    
    # Diretorias sob supervisão
    diretorias_supervisionadas = db.Column(db.Text)  # Lista de diretorias separadas por vírgula
    quantidade_diretorias = db.Column(db.Integer, default=0)
    
    # Estatísticas consolidadas
    total_escolas = db.Column(db.Integer, default=0)
    total_veiculos = db.Column(db.Integer, default=0)
    
    # Contato (se disponível)
    email = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'regiao': self.regiao,
            'diretorias_supervisionadas': self.diretorias_supervisionadas,
            'quantidade_diretorias': self.quantidade_diretorias,
            'total_escolas': self.total_escolas,
            'total_veiculos': self.total_veiculos,
            'email': self.email,
            'telefone': self.telefone,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
        }

class Distancia(db.Model):
    """Modelo para Distâncias entre Escolas e Diretorias"""
    __tablename__ = 'distancias'
    
    id = db.Column(db.Integer, primary_key=True)
    escola_id = db.Column(db.Integer, db.ForeignKey('escolas.id'), nullable=False)
    diretoria_id = db.Column(db.Integer, db.ForeignKey('diretorias.id'), nullable=False)
    
    # Distância calculada
    distancia_km = db.Column(db.Float, nullable=False)
    metodo_calculo = db.Column(db.String(50), default='haversine')
    
    # Coordenadas para referência
    escola_lat = db.Column(db.Float)
    escola_lng = db.Column(db.Float)
    diretoria_lat = db.Column(db.Float)
    diretoria_lng = db.Column(db.Float)
    
    # Timestamps
    calculado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    escola = db.relationship('Escola', backref='distancias_calculadas')
    diretoria = db.relationship('Diretoria', backref='distancias_escolas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'escola_id': self.escola_id,
            'diretoria_id': self.diretoria_id,
            'distancia_km': self.distancia_km,
            'metodo_calculo': self.metodo_calculo,
            'escola_lat': self.escola_lat,
            'escola_lng': self.escola_lng,
            'diretoria_lat': self.diretoria_lat,
            'diretoria_lng': self.diretoria_lng,
            'calculado_em': self.calculado_em.isoformat() if self.calculado_em else None
        }

class EstatisticasGerais(db.Model):
    """Modelo para Estatísticas Gerais do Sistema"""
    __tablename__ = 'estatisticas_gerais'
    
    id = db.Column(db.Integer, primary_key=True)
    data_referencia = db.Column(db.Date, nullable=False)
    
    # Totais gerais
    total_diretorias = db.Column(db.Integer, default=0)
    total_escolas = db.Column(db.Integer, default=0)
    total_veiculos = db.Column(db.Integer, default=0)
    total_supervisores = db.Column(db.Integer, default=0)
    
    # Por tipo de escola
    escolas_indigenas = db.Column(db.Integer, default=0)
    escolas_quilombolas = db.Column(db.Integer, default=0)
    escolas_regulares = db.Column(db.Integer, default=0)
    
    # Por tipo de veículo
    veiculos_s1 = db.Column(db.Integer, default=0)
    veiculos_s2 = db.Column(db.Integer, default=0)
    veiculos_s2_4x4 = db.Column(db.Integer, default=0)
    
    # Capacidade total estimada
    capacidade_total_veiculos = db.Column(db.Integer, default=0)
    
    # Maior e menor diretoria
    diretoria_mais_escolas = db.Column(db.String(100))
    quantidade_maior = db.Column(db.Integer, default=0)
    diretoria_menos_escolas = db.Column(db.String(100))
    quantidade_menor = db.Column(db.Integer, default=0)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'data_referencia': self.data_referencia.isoformat() if self.data_referencia else None,
            'total_diretorias': self.total_diretorias,
            'total_escolas': self.total_escolas,
            'total_veiculos': self.total_veiculos,
            'total_supervisores': self.total_supervisores,
            'escolas_indigenas': self.escolas_indigenas,
            'escolas_quilombolas': self.escolas_quilombolas,
            'escolas_regulares': self.escolas_regulares,
            'veiculos_s1': self.veiculos_s1,
            'veiculos_s2': self.veiculos_s2,
            'veiculos_s2_4x4': self.veiculos_s2_4x4,
            'capacidade_total_veiculos': self.capacidade_total_veiculos,
            'diretoria_mais_escolas': self.diretoria_mais_escolas,
            'quantidade_maior': self.quantidade_maior,
            'diretoria_menos_escolas': self.diretoria_menos_escolas,
            'quantidade_menor': self.quantidade_menor,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
        }
