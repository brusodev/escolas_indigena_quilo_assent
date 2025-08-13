# -*- coding: utf-8 -*-
"""
Modelos SQLAlchemy - Sistema de Gestão Escolar
"""

from app import db
from datetime import datetime
from sqlalchemy import Index


class Escola(db.Model):
    """Modelo para Escolas"""
    __tablename__ = 'escolas'

    id = db.Column(db.Integer, primary_key=True)
    codigo_mec = db.Column(db.String(20), unique=True, index=True)
    codigo = db.Column(db.String(20), index=True)
    nome = db.Column(db.String(255), nullable=False, index=True)
    tipo = db.Column(db.String(50), nullable=False, index=True)
    endereco = db.Column(db.Text)
    cidade = db.Column(db.String(100), index=True)
    uf = db.Column(db.String(2), default='SP')
    cep = db.Column(db.String(10))
    zona = db.Column(db.String(20), default='Urbana')
    situacao = db.Column(db.Integer, default=1)

    # Coordenadas geográficas
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)

    # Relacionamento com Diretoria
    diretoria_id = db.Column(db.Integer, db.ForeignKey('diretorias.id'),
                             nullable=True, index=True)
    diretoria_nome = db.Column(db.String(100), index=True)

    # Dados adicionais
    codigo_ibge = db.Column(db.String(20))
    tipo_original = db.Column(db.String(100))
    distancia_diretoria = db.Column(db.Float)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Relacionamentos
    distancias = db.relationship('Distancia', backref='escola',
                                 lazy='dynamic', cascade='all, delete-orphan')

    # Índices compostos para consultas otimizadas
    __table_args__ = (
        Index('ix_escola_tipo_cidade', 'tipo', 'cidade'),
        Index('ix_escola_coords', 'latitude', 'longitude'),
        Index('ix_escola_diretoria_tipo', 'diretoria_id', 'tipo'),
    )

    def __repr__(self):
        return f'<Escola {self.nome}>'

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'codigo_mec': self.codigo_mec,
            'codigo': self.codigo,
            'nome': self.nome,
            'tipo': self.tipo,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'uf': self.uf,
            'zona': self.zona,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'diretoria_id': self.diretoria_id,
            'diretoria_nome': self.diretoria_nome,
            'distancia_diretoria': self.distancia_diretoria
        }

    @classmethod
    def get_by_tipo(cls, tipo):
        """Buscar escolas por tipo"""
        return cls.query.filter_by(tipo=tipo).all()

    @classmethod
    def get_by_diretoria(cls, diretoria_id):
        """Buscar escolas por diretoria"""
        return cls.query.filter_by(diretoria_id=diretoria_id).all()

    @classmethod
    def get_in_radius(cls, lat, lng, radius_km=50):
        """Buscar escolas em um raio específico"""
        # Fórmula aproximada para distância em graus
        lat_diff = radius_km / 111.0  # 1 grau lat ≈ 111 km
        lng_diff = radius_km / (111.0 * abs(lat))  # Ajustar por latitude

        return cls.query.filter(
            cls.latitude.between(lat - lat_diff, lat + lat_diff),
            cls.longitude.between(lng - lng_diff, lng + lng_diff)
        ).all()
