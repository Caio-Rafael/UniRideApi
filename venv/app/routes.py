from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Carona
from werkzeug.security import check_password_hash, generate_password_hash

# Criando o blueprint
routes = Blueprint('routes', __name__)

# Listar usuários
@routes.route('/users', methods=['GET'])
def get_all_user():
    users = User.query.all()
    return jsonify([user.as_dict() for user in users])

# Adicionar usuários
@routes.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        data['senha'] = generate_password_hash(data['senha'])
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.as_dict()), 201
    except Exception as e:
        db.session.rollback() 
        return jsonify({"error": str(e)}), 400

# Deletar usuários por id
@routes.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return '', 204

# Adicionar carona
@routes.route('/carona', methods=['POST'])
def create_carona():
    data = request.get_json()
    new_carona = Carona(**data)
    db.session.add(new_carona)
    db.session.commit()
    return jsonify(new_carona.as_dict()), 201

# Listar caronas
@routes.route('/carona', methods=['GET'])
def get_all_carona():
    caronas = Carona.query.all()
    return jsonify([carona.as_dict() for carona in caronas])

# Atualizar carona por id
@routes.route('/carona/<int:id>', methods=['PUT'])
def update_carona(id):
    carona = Carona.query.get(id)
    if not carona:
        return jsonify({"error": "Carona not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(carona, key, value)
    db.session.commit()
    return jsonify(carona.as_dict())

# deletar carona por id
@routes.route('/carona/<int:carona_id>', methods=['DELETE'])
def delete_carona(carona_id):
    carona = Carona.query.get(carona_id)

    if not carona:
        return jsonify({"error": "Carona não encontrada"}), 404

    db.session.delete(carona)
    db.session.commit()
    return jsonify({"message": "Carona excluída com sucesso"}), 204

# Login de usuário
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios!"}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        print(f"Usuário encontrado: {user.email}")
        if check_password_hash(user.senha, senha):
            print("Senha correta!") 
            return jsonify({
                'email': user.email,
                'tipo': user.tipo, 
                'id': user.id,     
            }), 200
        else:
            print("Senha incorreta!") 
    else:
        print("Usuário não encontrado!")  
    
    return jsonify({"message": "Email ou senha inválidos!"}), 401

#Buscar CEP com API ViaCEP
@routes.route('/buscar-endereco', methods=['GET'])
def buscar_endereco():
    cep = request.args.get('cep')
    if not cep:
        return jsonify({"error": "CEP não informado"}), 400
    
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        endereco = response.json()
        
        if "erro" in endereco:
            return jsonify({"error": "CEP inválido"}), 404
        
        return jsonify(endereco)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500