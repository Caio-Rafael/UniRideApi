from app import db
from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

carona_passageiros = db.Table(
    'carona_passageiros',
    db.Column('carona_id', db.Integer, db.ForeignKey('carona.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

    caronas_participando = db.relationship(
        'Carona',
        secondary=carona_passageiros,
        back_populates='passageiros'
    )

    def as_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo': self.tipo,
        }
    
    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)
    

class Carona(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    motorista_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    destino = db.Column(db.String(255), nullable=False)
    horario = db.Column(db.String(255), nullable=False)
    vagas = db.Column(db.Integer, nullable=False)
    cep = db.Column(db.String(8), nullable=False) 
    logradouro = db.Column(db.String(255), nullable=False) 
    bairro = db.Column(db.String(255), nullable=False) 
    localidade = db.Column(db.String(255), nullable=False) 
    uf = db.Column(db.String(2), nullable=False)
    descricao = db.Column(db.String(500), nullable=True)

    passageiros = db.relationship(
        'User',
        secondary=carona_passageiros,
        back_populates='caronas_participando'
    )

    def adicionar_passageiro(self, user):
        if user not in self.passageiros:
            self.passageiros.append(user)
            self.vagas -= 1
            db.session.commit()
            return True
        return False

    def remover_passageiro(self, user):
        if user in self.passageiros:
            self.passageiros.remove(user)
            self.vagas += 1
            db.session.commit()
            return True
        return False

    def as_dict(self):
        return {
            "id": self.id,
            "motorista_id": self.motorista_id,
            "destino": self.destino,
            "horario": self.horario,
            "vagas": self.vagas,
            "cep": self.cep,
            "logradouro": self.logradouro,
            "bairro": self.bairro,
            "localidade": self.localidade,
            "uf": self.uf,
            "descricao": self.descricao,
            "passageiros": [user.as_dict() for user in self.passageiros]
        }