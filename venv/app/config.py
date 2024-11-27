import os

class Config:
    # Configuração do banco de dados SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "caronas.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False