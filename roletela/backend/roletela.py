from flask_cors import CORS
from flask import Flask, jsonify, request
from functions import *
from api import sugerir_titulos, detalhes_titulo

app = Flask(__name__, template_folder='../')
app.config['JSON_AS_ASCII'] = False
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

@app.route('/sortear', methods=['GET'])
def sortear():
    plataformas = request.args.getlist('plataforma')    
    return jsonify(sortearTitulo(*plataformas))

@app.route('/filmes', methods=['GET'])
def filmes():
    plataformas = request.args.getlist('plataforma')    
    return jsonify(listarTitulos(*plataformas))

@app.route('/sugerir', methods=['GET'])
def sugerir_filmes():
    titulo = request.args.getlist('titulo')
    try:
        resultado = jsonify(sugerir_titulos(titulo))
        return resultado
    except:
        return jsonify('Nenhum resultado encontrado para o título sugerido.')

@app.route('/sugerir/adicionar', methods=['POST'])
def adicionar_filme():
    dados = request.get_json()
    
    id_api = dados.get('id_api')
    media = dados.get('media')
    title = dados.get('title')
    plataforma = dados.get('plataforma')
    providers_rent = dados.get('providers_rent')
    providers_buy = dados.get('providers_buy')
    img = dados.get('img')
    dados = detalhes_titulo(id_api, media, title, plataforma, providers_rent, providers_buy, img)
    
    return jsonify(adicionarTitulo(dados))

if __name__ == '__main__':
    app.run(debug=True)
    