import json
   
def listarTitulos(*plataformas):
    try:
        arquivo = open("./roletela/backend/filmes.json", "r", encoding='utf-8')
    except:
        arquivo = open("./roletela/backend/filmes.json", "w", encoding='utf-8')
        arquivo.close()
    try:
        arquivo = open("./roletela/backend/filmes.json", "r", encoding='utf-8')
        dados = json.load(arquivo)
    except:
        dados = []
    arquivo.close()
    if plataformas:
        dados = filtrarTitulos(dados, *plataformas)
    return dados
    
' not in [filme["id_api"] for filme in dados]'

def adicionarTitulo(dict):
    dados = listarTitulos()
    if dados:
        if dict['id_api']:
            dados.append({
                "id": len(dados) + 1,
                "id_api": dict['id_api'],
                "media": dict['media'],
                'title': dict['title'],
                'overview': dict['overview'],
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
    else:
        return 'Nenhum filme encontrado para as plataformas selecionadas.'

def sortearTitulo(*plataformas):
    import random
    dados = listarTitulos()
    if plataformas:
        dados = filtrarTitulos(dados, *plataformas)
    if not dados:
        return 'Nenhum filme encontrado para as plataformas selecionadas.'
    filme_sorteado = random.choice(dados)    
    return filme_sorteado

def filtrarTitulos(dados, *plataformas):
    filmes_filtrados = []
    for plataforma in list(plataformas):
        for filme in dados:
            if plataforma in filme["plataforma"]:
                if filme not in filmes_filtrados:
                    filmes_filtrados += [filme]
    return filmes_filtrados