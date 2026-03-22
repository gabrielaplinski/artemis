from flask_cors import CORS
from flask import Flask, jsonify, request
from api import *

app = Flask(__name__, template_folder='../')
app.json.ensure_ascii = False
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

@app.route('/sortear', methods=['GET'])
def sortear():
    plataformas = request.args.getlist('plataforma')    
    return jsonify(sortear_titulo(*plataformas))

@app.route('/filmes_assistidos', methods=['GET'])
def filmes_assistidos_flask():
    plataformas = request.args.getlist('plataforma')    
    return jsonify(listar_assistidos(*plataformas))

@app.route('/filmes_sorteaveis', methods=['GET'])
def filmes_sorteaveis():
    plataformas = request.args.getlist('plataforma')
    return jsonify(listar_sorteaveis(*plataformas))

@app.route('/sugerir', methods=['GET'])
async def sugerir_filmes():
    titulo = request.args.getlist('titulo')
    try:
        resultado = await sugerir_titulos(titulo)
        return jsonify(resultado)
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

@app.route('/filmes/excluir', methods=['DELETE'])
def excluir_filme():
    id = request.args.get('id')
    id_api = request.args.get('id_api')
    return jsonify(excluirTitulo(int(id), id_api))
    
@app.route('/filmes/atualizar', methods=['PUT'])
def atualizar_filmes():
    return jsonify(atualizar_provedores()) 
   
@app.route('/alterar_status', methods=['GET'])
def alterar_status_flask():
    status = request.args.getlist('status')
    id_api = request.args.getlist('id_api')
    return jsonify(alterar_status(id_api, status))
    
@app.route('/add_assistindo', method=['POST'])
def add_assistindo_flask():
    id_api = request.args.getlist('id_api')
    return jsonify(add_assistindo(id_api))

@app.route('/remover_assistindo')
def remover_assistindo_flask():
    return remover_assistindo

@app.route('/assistindo', method=['GET'])
def assistindo_flask():
    return jsonify(assistindo)

if __name__ == '__main__':
    app.run(debug=True)
    