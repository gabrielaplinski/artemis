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

def adicionarTitulo(titulo, plataforma="X"):
    dados = listarTitulos()
    if titulo.capitalize() not in [filme["titulo"] for filme in dados]:
        dados.append({
            "id": len(dados) + 1,
            "titulo": titulo.capitalize(),
            "plataforma": plataforma.capitalize()
        })
        arquivo = open("./roletela/backend/filmes.json", "w")
        json.dump(dados, arquivo)
        arquivo.close()
        return 'Filme adicionado.'
    else:
        return 'Filme já cadastrado.'

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
    if not dados:
        return 'Nenhum filme encontrado para as plataformas selecionadas.'
    filme_sorteado = random.choice(dados)    
    return filme_sorteado

print(adicionarTitulo("fatura"))