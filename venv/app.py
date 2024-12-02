from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/carona', methods=['GET', 'OPTIONS'])
def carona():
    return jsonify({'message': 'Dados da carona'}), 200

if __name__ == '__main__':
    app.run()