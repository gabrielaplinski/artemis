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
    if dict['id_api'] not in [filme["id_api"] for filme in dados]:
        dados.append({
            "id": len(dados) + 1,
            "id_api": dict['id_api'],
            "media": dict['media'],
            'overview': dict['overview'],
            'title': dict['title'],
            'release_date': dict['release_date'],
            'vote_average': dict['vote_average'],
            'origin_country': dict['origin_country'], 
            'genres': dict['genres'], 
            'img': dict['img'],
            'plataforma': dict['plataforma'], 
            'aluguel/compra': {"aluguel": dict['aluguel/compra']['aluguel'],
                            "compra": dict['aluguel/compra']['compra']}})
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

'''dict_Fratura = {'id_api': 568091, 'media': 'movie', 'overview': "Driving cross-country, Ray and his wife and daughter stop at a highway rest area where his daughter falls and breaks her arm. After a frantic rush to the hospital and a clash with the check-in nurse, Ray is finally able to get her to a doctor. While the wife and daughter go downstairs for an MRI, Ray, exhausted, passes out in a chair in the lobby. Upon waking up, they have no record or knowledge of Ray's family ever being checked in.", 'title': 'Fratura', 'release_date': '22/09/2019', 'vote_average': 6.75, 'origin_country': ['US'], 'genres': ['Thriller', 'Drama'], 'img': 'https://image.tmdb.org/t/p/w500/vsvmurub7aShF1PIFJS2l2D5ArS.jpg', 'plataforma': ['Netflix'], 'aluguel/compra': {'aluguel': ['Amazon Prime Video'], 'compra': ['Amazon Prime Video']}}

print(adicionarTitulo(dict_Fratura))'''