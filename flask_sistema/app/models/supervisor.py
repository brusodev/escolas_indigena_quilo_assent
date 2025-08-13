# -*- coding: utf-8 -*-
"""
Modelo Supervisor - Sistema de Gestão Escolar
"""

from app import db
from datetime import datetime


class Supervisor(db.Model):
    """Modelo para Supervisores do GEP"""
    __tablename__ = 'supervisores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False, index=True)
    cargo = db.Column(db.String(100), index=True)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, index=True)

    # Relacionamento com Diretoria
    diretoria_id = db.Column(db.Integer, db.ForeignKey('diretorias.id'),
                             nullable=False, index=True)

    # Área de responsabilidade
    area_responsabilidade = db.Column(db.String(200))
    ativo = db.Column(db.Boolean, default=True, index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Supervisor {self.nome}>'

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'cargo': self.cargo,
            'telefone': self.telefone,
            'email': self.email,
            'diretoria_id': self.diretoria_id,
            'diretoria_nome': self.diretoria.nome if self.diretoria else None,
            'area_responsabilidade': self.area_responsabilidade,
            'ativo': self.ativo
        }

    @classmethod
    def get_by_diretoria(cls, diretoria_id):
        """Buscar supervisores por diretoria"""
        return cls.query.filter_by(diretoria_id=diretoria_id, ativo=True).all()

    @classmethod
    def get_ativos(cls):
        """Buscar apenas supervisores ativos"""
        return cls.query.filter_by(ativo=True).all()
