from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Isso permite CORS para todas as rotas e todas as origens

@app.route('/carona', methods=['GET', 'OPTIONS'])
def carona():
    return jsonify({'message': 'Dados da carona'}), 200

if __name__ == '__main__':
    app.run()