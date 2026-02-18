import json
   
def listarTitulos(*plataformas):
    try:
        arquivo = open("./roletela/backend/filmes.json", "r")
    except:
        arquivo = open("./roletela/backend/filmes.json", "w")
    try:
        dados = json.load(arquivo)
    except:
        dados = []
    arquivo.close()
    if plataformas:
        dados = filtrarTitulos(*plataformas)
    if not dados:
        return 'Nenhum filme encontrado para as plataformas selecionadas.'
    return dados

def adicionarTitulo(dict):
    dados = listarTitulos()
    if dict['id_api'].capitalize() not in [filme["id_api"] for filme in dados]:
        dados.append({
            "id": len(dados) + 1,
            "id_api": dict['id_api'],
            "media": dict['media_type'],
            'overview': dict['overview'],
            'title': dict['title'],
            'release_date': dict['release_date'],
            'vote_average': dict['vote_average'],
            'origin_country': dict['origin_country'], 
            'genres': dict['genres'], 
            'img': dict['img'],
            'plataforma': dict['plataforma'], 
            'aluguel/compra': {"aluguel": dict['providers_rent'],
                            "compra": dict['providers_buy']}})
        with open("./roletela/backend/filmes.json", "w", encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False)
        return 'Filme adicionado.'
    else:
        return 'Filme já cadastrado.'

def sortearTitulo(*plataformas):
    import random
    dados = listarTitulos()
    if plataformas:
        dados = filtrarTitulos(*plataformas)
    if not dados:
        return 'Nenhum filme encontrado para as plataformas selecionadas.'
    filme_sorteado = random.choice(dados)    
    return filme_sorteado

def filtrarTitulos(*plataformas):
    dados = listarTitulos()
    filmes_filtrados = []
    for plataforma in list(plataformas):
        for filme in dados:
            if plataforma in filme["plataforma"]:
                if filme not in filmes_filtrados:
                    filmes_filtrados += [filme]
    return filmes_filtrados