# -*- coding: utf-8 -*-
"""
Modelo Distancia - Sistema de Gestão Escolar
"""

from app import db
from datetime import datetime


class Distancia(db.Model):
    """Modelo para Distâncias entre Escolas e Diretorias"""
    __tablename__ = 'distancias'

    id = db.Column(db.Integer, primary_key=True)

    # Relacionamentos
    escola_id = db.Column(db.Integer, db.ForeignKey('escolas.id'),
                          nullable=False, index=True)
    diretoria_id = db.Column(db.Integer, db.ForeignKey('diretorias.id'),
                             nullable=False, index=True)

    # Dados da distância
    distancia_km = db.Column(db.Float, nullable=False, index=True)
    metodo_calculo = db.Column(db.String(50), default='Haversine')

    # Dados adicionais
    tempo_estimado_min = db.Column(db.Integer)  # Em minutos
    via_preferencial = db.Column(db.String(200))
    observacoes = db.Column(db.Text)

    # Timestamps
    data_calculo = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Índice único para evitar duplicatas
    __table_args__ = (
        db.UniqueConstraint('escola_id', 'diretoria_id',
                            name='uq_escola_diretoria'),
    )

    def __repr__(self):
        return f'<Distancia Escola:{self.escola_id} -> Diretoria:{self.diretoria_id}: {self.distancia_km}km>'

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'escola_id': self.escola_id,
            'diretoria_id': self.diretoria_id,
            'distancia_km': self.distancia_km,
            'metodo_calculo': self.metodo_calculo,
            'tempo_estimado_min': self.tempo_estimado_min,
            'data_calculo': self.data_calculo.isoformat() if self.data_calculo else None,
            'escola_nome': self.escola.nome if self.escola else None,
            'diretoria_nome': self.diretoria_rel.nome if self.diretoria_rel else None
        }

    @classmethod
    def get_by_escola(cls, escola_id):
        """Buscar distâncias por escola"""
        return cls.query.filter_by(escola_id=escola_id).all()

    @classmethod
    def get_by_diretoria(cls, diretoria_id):
        """Buscar distâncias por diretoria"""
        return cls.query.filter_by(diretoria_id=diretoria_id).all()

    @classmethod
    def get_menor_distancia_escola(cls, escola_id):
        """Buscar a menor distância para uma escola"""
        return cls.query.filter_by(escola_id=escola_id).order_by(cls.distancia_km.asc()).first()

    @classmethod
    def get_estatisticas_diretoria(cls, diretoria_id):
        """Estatísticas de distância para uma diretoria"""
        from sqlalchemy import func

        result = db.session.query(
            func.count(cls.id).label('total_escolas'),
            func.avg(cls.distancia_km).label('distancia_media'),
            func.min(cls.distancia_km).label('distancia_minima'),
            func.max(cls.distancia_km).label('distancia_maxima')
        ).filter_by(diretoria_id=diretoria_id).first()

        return {
            'total_escolas': result.total_escolas or 0,
            'distancia_media': round(result.distancia_media or 0, 2),
            'distancia_minima': result.distancia_minima or 0,
            'distancia_maxima': result.distancia_maxima or 0
        }
