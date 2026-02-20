from flask import json
import requests
from functions import adicionarTitulo, listarTitulos
headers = {
    "accept": 'application/json',
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZDU4N2YxNjY3ZDViZDIzNjkyMDk1MjQ2NWE4OWQyZCIsIm5iZiI6MTc3MDk1NDQwOC44OTIsInN1YiI6IjY5OGU5ZWE4MjVjOGE0YThjYmI2ODk5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.SRmYAq05TPExKlLEzQut7hOuGAE2JFO_TOjW5RfvIpE"
}

def sugerir_titulos(titulo):
    plataformas = [
        "Netflix",
        "Crunchyroll",
        "Disney",
        "Globoplay",
        "HBO",
        "Apple",
        "Amazon"
    ]
    sugestoes = []
    
    url = 'https://api.themoviedb.org/3/search/multi'
    response = requests.get(url, headers=headers, params={"query": titulo, "region": "BR", 'language': 'pt-BR'})
    response.encoding = 'utf-8'
    results_titulo = response.json()['results']
    
    i = 0
    for r in results_titulo[:8]:
        if r['media_type'] == 'tv' or r['media_type'] == 'movie':
            url = 'https://api.themoviedb.org/3/{media}/{tv_id}/watch/providers'.format(media=r['media_type'],tv_id=r['id'])
            response = requests.get(url, headers=headers)
            try:
                result_providers = response.json()['results']
            except:
                result_providers = {}
            
            if 'BR' in result_providers:
                i += 1
                id_api = r['id']
                media = r['media_type']
                title = r['title'] if media == 'movie' else r['name']
                        
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
                
                img = r['poster_path']
                
                if img:
                    img = 'https://image.tmdb.org/t/p/w500' + img
                else:
                    img = ''

                sugestao = { 
                            "id_api": id_api,
                            "media": media,
                            'title': title,
                            "plataforma": plataforma,
                            "aluguel/compra": {"aluguel": providers_rent,
                                                "compra": providers_buy},
                            "img": img}    
                sugestoes.append(sugestao)
        if i == 5:
            break  
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
    for c, v in enumerate(sugerir_titulos(titulo)):
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
    plataformas = [
        "Netflix",
        "Crunchyroll",
        "Disney",
        "Globoplay",
        "HBO",
        "Apple",
        "Amazon"
    ]
    
    dados = listarTitulos()
    dados_backup = listarTitulos()
    
    for filme in dados:
        print(filme['title'], filme['id_api'], filme['media'])
        print('----------------------------------')
        print(filme['plataforma'])
        print(filme['aluguel/compra'])
        print('----------------------------------')
        url = 'https://api.themoviedb.org/3/{media}/{tv_id}/watch/providers'.format(media=filme['media'],tv_id=filme['id_api'])
        response = requests.get(url, headers=headers)
        try:
            result_providers = response.json()['results']
        except:
            result_providers = {}
            print('Nenhum resultado encontrado para o título:', filme['title'])
        
        if 'BR' in result_providers:                    
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
            print(plataforma)
            print(providers_rent)
            print(providers_buy)
            print('----------------------------------')
            filme['plataforma'] = plataforma
            filme['aluguel/compra'] = {"aluguel": providers_rent,
                                        "compra": providers_buy}
    if dados == dados_backup:
        return 'Nenhuma alteração necessária.'
    with open("./roletela/backend/filmes.json", "w", encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False)
    return 'Provedores atualizados.'

print(atualizar_provedores())

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