from flask import Flask, jsonify, render_template, request
from functions import *

app = Flask(__name__, template_folder='../')

@app.route('/sortear', methods=['GET'])
def sorteio():
    return jsonify(sortearTitulo())

@app.route('/filmes', methods=['GET'])
def filmes():
    return jsonify(listarTitulos())

@app.route('/filmes', methods=['POST'])
def cadastrar_filme():
    dados = request.get_json()
    titulo = dados.get('titulo')
    plataforma = dados.get('plataforma')
    return jsonify(adicionarTitulo(titulo, plataforma))

if __name__ == '__main__':
    app.run(debug=True)
