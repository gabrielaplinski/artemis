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

def adicionarTitulo(dict):
    dados = listarTitulos()
    if dados:
        if dict['id_api'] not in [filme["id_api"] for filme in dados]:
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

def excluirTitulo(id, id_api):
    dados = listarTitulos()
    for filme in dados:
        if filme['id'] == id and filme['id_api'] == id_api:
            dados.remove(filme)
            with open("./roletela/backend/filmes.json", "w", encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False)
            return 'Filme excluído.'
        return 'Informações de id incorretas.'
    return 'Filme não encontrado.'

# função usada pra atualizar a lista de filmes, não é necessária para o funcionamento do programa, mas pode ser útil para adicionar novos títulos sugeridos
'''
def completarTitulo(dict):
    dados = listarTitulos()
    novos_dados = []
    try:
        arquivo = open("./roletela/backend/novos_filmes.json", "r", encoding='utf-8')
    except:
        arquivo = open("./roletela/backend/novos_filmes.json", "w", encoding='utf-8')
        arquivo.close()
    try:
        arquivo = open("./roletela/backend/novos_filmes.json", "r", encoding='utf-8')
        novos_dados = json.load(arquivo)
    except:
        novos_dados = []
    arquivo.close()
    
    if dados:
        if dict['id_api'] not in [filme["id_api"] for filme in novos_dados]:
            novos_dados.append({
                "id": len(novos_dados) + 1,
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
            with open("./roletela/backend/novos_filmes.json", "w", encoding='utf-8') as arquivo:
                json.dump(novos_dados, arquivo, ensure_ascii=False)
            return 'Filme adicionado.'
        else:
            return 'Filme já cadastrado.'
    else:
        return 'Nenhum filme encontrado para as plataformas selecionadas.'
'''