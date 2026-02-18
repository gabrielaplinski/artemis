from flask_cors import CORS
from flask import Flask, jsonify, request
from functions import *
from api import sugerir_titulos

app = Flask(__name__, template_folder='../')
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

@app.route('/sortear', methods=['GET'])
def sortear():
    plataformas = request.args.getlist('plataforma')    
    return jsonify(sortearTitulo(*plataformas))

@app.route('/filmes', methods=['GET'])
def filmes():
    plataformas = request.args.getlist('plataforma')    
    return jsonify(listarTitulos(*plataformas))

@app.route('/adicionar', methods=['POST'])
def adicionar_filme():
    dados = request.get_json()
    titulo = dados.get('titulo')
    plataforma = dados.get('plataforma')
    return jsonify(adicionarTitulo(titulo, plataforma))

'''@app.route('/sugerir', methods=['GET'])
def sugerir_filmes():
    titulo = request.args.getlist('titulo')
    return jsonify(sugerir_titulos(titulo))'''

@app.route('/sugerir', methods=['POST'])
def sugerir_filmes():
    dados = request.get_json()
    titulo = dados.get('titulo')
    return jsonify(sugerir_titulos(titulo))

if __name__ == '__main__':
    app.run(debug=True)
