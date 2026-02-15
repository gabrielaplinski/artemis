import json
   
def listarTitulos():
    try:
        arquivo = open("./roletela/backend/filmes.json", "r")
    except:
        arquivo = open("./roletela/backend/filmes.json", "w")
    try:
        dados = json.load(arquivo)
    except:
        dados = []
    arquivo.close()
    return dados  

def adicionarTitulo(titulo, plataforma):
    dados = listarTitulos()
    dados.append({
        "id": len(dados) + 1,
        "titulo": titulo,
        "plataforma": plataforma
    })
    arquivo = open("./roletela/backend/filmes.json", "w")
    json.dump(dados, arquivo)
    arquivo.close()
    return "Filme cadastrado com sucesso!"

def sortearTitulo():
    import random
    dados = listarTitulos()
    filme_sorteado = random.choice(dados)    
    return filme_sorteado