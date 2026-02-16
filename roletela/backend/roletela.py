from flask_cors import CORS
from flask import Flask, jsonify, render_template, request
from functions import *

app = Flask(__name__, template_folder='../')
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

@app.route('/sortear', methods=['GET'])
def sortear():
    plataformas = request.args.getlist('plataforma')    
    return jsonify(sortearTitulo(*plataformas))

@app.route('/filmes', methods=['GET'])
def filmes():
    return jsonify(listarTitulos())

@app.route('/adicionar', methods=['POST'])
def adicionar_filme():
    dados = request.get_json()
    titulo = dados.get('titulo')
    plataforma = dados.get('plataforma')
    return jsonify(adicionarTitulo(titulo, plataforma))

if __name__ == '__main__':
    app.run(debug=True)
