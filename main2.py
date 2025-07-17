from flask import Flask, jsonify, request
from bd import Carros

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def home():
    return 'API FUNCIONANDO!'

@app.route('/carros', methods=['GET'])
def get_carros():
    return jsonify(Carros)

@app.route('/carros', methods=['POST'])
def createCarro():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    carro = request.get_json()
    Carros.append(carro)
    return jsonify(carro), 201

if __name__ == '__main__':
    app.run()

