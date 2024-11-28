from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo': self.tipo,
            #'senha': self.senha,
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

    def as_dict(self):
        return {
            "id": self.id,
            "motorista_id": self.motorista_id,
            "destino": self.destino,
            "horario": self.horario,
            "vagas": self.vagas
        }