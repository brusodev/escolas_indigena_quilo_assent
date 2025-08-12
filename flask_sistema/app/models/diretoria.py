# -*- coding: utf-8 -*-
"""
Modelo Diretoria - Sistema de Gestão Escolar
"""

from app import db
from datetime import datetime
from sqlalchemy import Index


class Diretoria(db.Model):
    """Modelo para Diretorias de Ensino"""
    __tablename__ = 'diretorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False, unique=True, index=True)
    codigo = db.Column(db.String(20), unique=True, index=True)
    endereco = db.Column(db.Text)
    cidade = db.Column(db.String(100))
    uf = db.Column(db.String(2), default='SP')
    cep = db.Column(db.String(10))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    
    # Coordenadas geográficas
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)
    
    # Classificação
    regiao = db.Column(db.String(50), index=True)  # Capital, Interior
    
    # Dados de veículos
    total_veiculos = db.Column(db.Integer, default=0)
    veiculos_s1 = db.Column(db.Integer, default=0)
    veiculos_s2 = db.Column(db.Integer, default=0)
    veiculos_s2_4x4 = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    
    # Relacionamentos
    escolas = db.relationship('Escola', backref='diretoria', lazy='dynamic')
    veiculos = db.relationship('Veiculo', backref='diretoria', lazy='dynamic',
                              cascade='all, delete-orphan')
    supervisores = db.relationship('Supervisor', backref='diretoria',
                                  lazy='dynamic', cascade='all, delete-orphan')
    distancias = db.relationship('Distancia', backref='diretoria_rel',
                                lazy='dynamic', cascade='all, delete-orphan')
    
    # Índices
    __table_args__ = (
        Index('ix_diretoria_coords', 'latitude', 'longitude'),
        Index('ix_diretoria_regiao', 'regiao'),
    )
    
    def __repr__(self):
        return f'<Diretoria {self.nome}>'
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'codigo': self.codigo,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'uf': self.uf,
            'regiao': self.regiao,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'total_veiculos': self.total_veiculos,
            'veiculos_s1': self.veiculos_s1,
            'veiculos_s2': self.veiculos_s2,
            'veiculos_s2_4x4': self.veiculos_s2_4x4,
            'total_escolas': self.escolas.count()
        }
    
    @property
    def total_escolas(self):
        """Número total de escolas"""
        return self.escolas.count()
    
    @property
    def escolas_por_tipo(self):
        """Estatísticas de escolas por tipo"""
        from app.models.escola import Escola
        from sqlalchemy import func
        
        result = db.session.query(
            Escola.tipo,
            func.count(Escola.id).label('total')
        ).filter_by(diretoria_id=self.id).group_by(Escola.tipo).all()
        
        return {tipo: total for tipo, total in result}
    
    def atualizar_total_veiculos(self):
        """Atualiza o total de veículos baseado nos registros"""
        self.total_veiculos = (self.veiculos_s1 + 
                              self.veiculos_s2 + 
                              self.veiculos_s2_4x4)
        return self.total_veiculos
