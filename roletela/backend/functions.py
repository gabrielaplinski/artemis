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
    if titulo not in [filme["titulo"] for filme in dados]:
        dados.append({
            "id": len(dados) + 1,
            "titulo": titulo.capitalize(),
            "plataforma": plataforma.capitalize()
        })
        arquivo = open("./roletela/backend/filmes.json", "w")
        json.dump(dados, arquivo)
        arquivo.close()
        return True
    else:
        return False

def sortearTitulo(*plataformas):
    import random
    dados = listarTitulos()
    if plataformas:
        filmes_filtrados = []
        for plataforma in list(plataformas):
            for filme in dados:
                if plataforma in filme["plataforma"]:
                    if filme not in filmes_filtrados:
                        filmes_filtrados += [filme]
        dados = filmes_filtrados
    filme_sorteado = random.choice(dados)    
    return filme_sorteado