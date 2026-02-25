from flask import json
import requests
import asyncio
import aiohttp

headers = {
    "accept": 'application/json',
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZDU4N2YxNjY3ZDViZDIzNjkyMDk1MjQ2NWE4OWQyZCIsIm5iZiI6MTc3MDk1NDQwOC44OTIsInN1YiI6IjY5OGU5ZWE4MjVjOGE0YThjYmI2ODk5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.SRmYAq05TPExKlLEzQut7hOuGAE2JFO_TOjW5RfvIpE"
}
plataformas = [
        "Netflix",
        "Crunchyroll",
        "Disney",
        "Globoplay",
        "HBO",
        "Apple",
        "Amazon"
    ]

# funções com a API TMBD

async def search_multi_TMBD(session, titulo):
    url = 'https://api.themoviedb.org/3/search/multi'
    params = {"query": titulo, "region": "BR", 'language': 'pt-BR'}
    try:
        async with session.get(url,headers=headers,params=params, timeout=10) as response:
            response.raise_for_status()
            return await response.json()
    except Exception as e:
        return f'Erro {e}'

async def search_providers_TMBD(session, id_api, media):
    url = 'https://api.themoviedb.org/3/{media}/{tv_id}/watch/providers'.format(media=media,tv_id=id_api)
    try:
        async with session.get(url,headers=headers, timeout=10) as response:
            response.raise_for_status()
            return await response.json()
    except Exception as e:
        return f'Erro {e}'

def buscar_img(result):
    img = result['poster_path']  
    if img:
        img = 'https://image.tmdb.org/t/p/w500' + img
    else:
        img = ''
    
    return img

def buscar_providers(result_providers):
    if 'flatrate' in result_providers['BR']:   
        providers = result_providers['BR']['flatrate']
    else:
        providers = []
    if 'rent' in result_providers['BR']:
        providers_rent = [provider['provider_name'] for provider in result_providers['BR']['rent']]
    else:
        providers_rent = []
    if 'buy' in result_providers['BR']:
        providers_buy = [provider['provider_name'] for provider in result_providers['BR']['buy']]
    else:
        providers_buy = [] 
            
    plataforma = []
    if providers:
        for provider in providers:
            provider = provider['provider_name'].split(' ')[0]
            if provider in plataformas:
                if provider not in plataforma:
                    plataforma.append(provider) 
                    
    return plataforma, providers_rent, providers_buy

async def sugerir_titulos(titulo):
    sugestoes = []    
    async with aiohttp.ClientSession() as session:
        tasks = [
            search_multi_TMBD(session, titulo)
        ]
        results_titulo = await asyncio.gather(*tasks)
        results_titulo = results_titulo[0].get('results')
        tasks = [
            search_providers_TMBD(session, r['id'], r['media_type']) for r in results_titulo
        ]
        result_providers = await asyncio.gather(*tasks)
        for r in range(0,len(results_titulo)+1):
            try:
                if 'BR' in result_providers[r]['results']:
                    id_api = results_titulo[r]['id']
                    media = results_titulo[r]['media_type']
                    title = results_titulo[r]['title'] if media == 'movie' else results_titulo[r]['name']
                    providers = buscar_providers(result_providers[r]['results'])
                    plataforma = providers[0]
                    providers_rent = providers[1]
                    providers_buy = providers[2]
                    img = buscar_img(results_titulo[r])
                    sugestao = {
                                "id_api": id_api,
                                "media": media,
                                'title': title,
                                "plataforma": plataforma,
                                "aluguel/compra": {"aluguel": providers_rent,
                                                    "compra": providers_buy},
                                "img": img}
                    sugestoes.append(sugestao)
            except:
                continue
    return sugestoes

def detalhes_titulo(id_api, media_type, title, plataforma=[], providers_rent=[], providers_buy=[], img=''):
    url_detail = 'https://api.themoviedb.org/3/{media}/{tv_id}'.format(media=media_type,tv_id=id_api)
    response = requests.get(url_detail, headers=headers, params={'language': 'pt-BR'})
    r = response.json()
    data = r['release_date'] if media_type == 'movie' else r['first_air_date']
    generos = []
    
    for g in r['genres']:
        generos.append(g['name'])
        
    retorno = {
        "id_api": id_api,
        "media": media_type,
        'title': title,
        'overview': r['overview'],
        'release_date': '/'.join(data.split('-')[::-1]),
        'vote_average': r['vote_average'],
        'origin_country': r['origin_country'], 
        'genres': generos, 
        'img': img,
        'plataforma': plataforma, 
        'aluguel/compra': {"aluguel": providers_rent,
                           "compra": providers_buy}}
    return retorno

def escolher_titulo(titulo):
    opcao = 0
    detalhes = []
    for c, v in enumerate(asyncio.run(sugerir_titulos(titulo))):
        arg = []
        for k, val in v.items():
            arg.append(val)
        detalhes.append(arg)
    for i in detalhes:
        print(detalhes.index(i)+1, ':', i, end='\n\n')
    while opcao < 1 or opcao > c+1:
        opcao = int(input('Digite o número do título desejado: '))
    return detalhes[opcao-1]

def atualizar_provedores():
    dados = listarTitulos()
    dados_backup = listarTitulos()
    for filme in dados:
        att_provedores(filme)
    if dados == dados_backup:
        return 'Nenhuma alteração necessária.'
    with open("./roletela/backend/filmes.json", "w", encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False)
    return 'Provedores atualizados.'

def att_provedores(filme):
    url = 'https://api.themoviedb.org/3/{media}/{tv_id}/watch/providers'.format(media=filme['media'],tv_id=filme['id_api'])
    response = requests.get(url, headers=headers)
    try:
        result_providers = response.json()['results']
    except:
        result_providers = {}
    if 'BR' in result_providers:                    
        providers = buscar_providers(result_providers)
        plataforma = providers[0]
        providers_rent = providers[1]
        providers_buy = providers[2]
        filme['plataforma'] = plataforma
        filme['aluguel/compra'] = {"aluguel": providers_rent,
                                    "compra": providers_buy}

# funções da lógica do site
   
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
    att_provedores(filme_sorteado)
    return filme_sorteado['title'], filme_sorteado['plataforma']

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
# função usada pra atualizar a lista de filmes, não é necessária para o funcionamento do programa, mas pode ser útil para adicionar novos títulos sugeridos
'''for t in listarTitulos():
    print(t['title'], '-', t['plataforma'])
    print('----------------------------------')
    titulo_selecionado = escolher_titulo(t['title'])
    print(completarTitulo(detalhes_titulo(titulo_selecionado[0], titulo_selecionado[1], titulo_selecionado[2], titulo_selecionado[3], titulo_selecionado[4]['aluguel'], titulo_selecionado[4]['compra'], titulo_selecionado[5])))'''
    
# titulos não encontrados ou à verificar: inuyasha, tokyo show    
'''
{"id": 46, "title": "Kaze ga tsuyoku fuiteiru", "plataforma": "X", "id_api": "api_1046"}
{"id": 61, "title": "91 days", "plataforma": "X", "id_api": "api_1061"}
inuyasha
tokyo ghoul
'''


'''titulo_selecionado = escolher_titulo('inuyasha')
print(adicionarTitulo(detalhes_titulo(titulo_selecionado[0], titulo_selecionado[1], titulo_selecionado[2], titulo_selecionado[3], titulo_selecionado[4]['aluguel'], titulo_selecionado[4]['compra'], titulo_selecionado[5])))'''
