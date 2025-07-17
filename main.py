from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Pegando a URL do banco do Railway (a DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # ou DATABASE_PUBLIC_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Carro(db.Model):
    __tablename__ = 'carros'

    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)

# Criação das tabelas (apenas uma vez)
with app.app_context():
    db.create_all()

# Criar um carro (POST)
@app.route('/carros', methods=['POST'])
def criar_carro():
    dados = request.get_json()
    novo_carro = Carro(modelo=dados['modelo'], ano=dados['ano'])
    db.session.add(novo_carro)
    db.session.commit()
    return jsonify({'id': novo_carro.id, 'modelo': novo_carro.modelo, 'ano': novo_carro.ano}), 201

# Listar todos os carros (GET)
@app.route('/carros', methods=['GET'])
def listar_carros():
    carros = Carro.query.all()
    return jsonify([{'id': c.id, 'modelo': c.modelo, 'ano': c.ano} for c in carros])

# Obter carro por ID (GET)
@app.route('/carros/<int:id>', methods=['GET'])
def obter_carro(id):
    carro = Carro.query.get_or_404(id)
    return jsonify({'id': carro.id, 'modelo': carro.modelo, 'ano': carro.ano})

# Atualizar carro (PUT)
@app.route('/carros/<int:id>', methods=['PUT'])
def atualizar_carro(id):
    carro = Carro.query.get_or_404(id)
    dados = request.get_json()
    carro.modelo = dados['modelo']
    carro.ano = dados['ano']
    db.session.commit()
    return jsonify({'id': carro.id, 'modelo': carro.modelo, 'ano': carro.ano})

# Deletar carro (DELETE)
@app.route('/carros/<int:id>', methods=['DELETE'])
def deletar_carro(id):
    carro = Carro.query.get_or_404(id)
    db.session.delete(carro)
    db.session.commit()
    return jsonify({'mensagem': 'Carro deletado com sucesso'})

