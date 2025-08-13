# -*- coding: utf-8 -*-
"""
Modelo Veiculo - Sistema de Gestão Escolar
"""

from app import db
from datetime import datetime


class Veiculo(db.Model):
    """Modelo para Veículos de Transporte Escolar"""
    __tablename__ = 'veiculos'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False,
                     index=True)  # S-1, S-2, S-2 4X4
    descricao = db.Column(db.String(200))
    placa = db.Column(db.String(10), unique=True, index=True)
    modelo = db.Column(db.String(100))
    ano = db.Column(db.Integer)
    capacidade = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Ativo', index=True)

    # Relacionamento com Diretoria
    diretoria_id = db.Column(db.Integer, db.ForeignKey('diretorias.id'),
                             nullable=False, index=True)

    # Dados operacionais
    km_atual = db.Column(db.Integer, default=0)
    ultima_revisao = db.Column(db.Date)
    proxima_revisao = db.Column(db.Date)
    observacoes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Veiculo {self.placa} ({self.tipo})>'

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'tipo': self.tipo,
            'descricao': self.descricao,
            'placa': self.placa,
            'modelo': self.modelo,
            'ano': self.ano,
            'capacidade': self.capacidade,
            'status': self.status,
            'diretoria_id': self.diretoria_id,
            'diretoria_nome': self.diretoria.nome if self.diretoria else None,
            'km_atual': self.km_atual
        }

    @classmethod
    def get_by_diretoria(cls, diretoria_id):
        """Buscar veículos por diretoria"""
        return cls.query.filter_by(diretoria_id=diretoria_id).all()

    @classmethod
    def get_by_tipo(cls, tipo):
        """Buscar veículos por tipo"""
        return cls.query.filter_by(tipo=tipo).all()

    @classmethod
    def get_ativos(cls):
        """Buscar apenas veículos ativos"""
        return cls.query.filter_by(status='Ativo').all()

    @property
    def precisa_revisao(self):
        """Verifica se o veículo precisa de revisão"""
        if not self.proxima_revisao:
            return False
        return datetime.now().date() >= self.proxima_revisao
