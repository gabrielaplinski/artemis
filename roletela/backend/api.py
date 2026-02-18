import requests
from functions import listarTitulos
headers = {
    "accept": 'application/json',
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZDU4N2YxNjY3ZDViZDIzNjkyMDk1MjQ2NWE4OWQyZCIsIm5iZiI6MTc3MDk1NDQwOC44OTIsInN1YiI6IjY5OGU5ZWE4MjVjOGE0YThjYmI2ODk5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.SRmYAq05TPExKlLEzQut7hOuGAE2JFO_TOjW5RfvIpE"
}

def sugerir_titulos(titulo):
    plataformas = [
        "Netflix",
        "Crunchyroll",
        "Disney Plus",
        "Globoplay",
        "HBO Max",
        "Apple TV",
        "Amazon Prime Video"
    ]
    sugestoes = []
    
    url = 'https://api.themoviedb.org/3/search/multi'
    response = requests.get(url, headers=headers, params={"query": titulo, "region": "BR", 'language': 'pt-BR'})
    results_titulo = response.json()['results']
    
    i = 0
    for r in results_titulo[:8]:
        if r['media_type'] == 'tv' or r['media_type'] == 'movie':
            url = 'https://api.themoviedb.org/3/{media}/{tv_id}/watch/providers'.format(media=r['media_type'],tv_id=r['id'])
            response = requests.get(url, headers=headers)
            result_providers = response.json()['results']
            
            if 'BR' in result_providers:
                i += 1
                id_api = r['id']
                media_type = r['media_type']
                title = r['title'] if media_type == 'movie' else r['name']
                        
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
                        if provider['provider_name'] in plataformas:
                            plataforma.append(provider['provider_name']) 
                
                img = r['poster_path']
                
                if img:
                    img = 'https://image.tmdb.org/t/p/w500' + img
                else:
                    img = ''

                sugestao = { 
                            "id_api": id_api,
                            "media": media_type,
                            'title': title,
                            "plataforma": plataforma,
                            "aluguel/compra": {"aluguel": providers_rent,
                                                "compra": providers_buy},
                            "img": img}    
                sugestoes.append(sugestao)
        if i == 4:
            break  
    return sugestoes

def detalhes_titulo(id_api, media_type, title, plataforma, providers_rent, providers_buy, img):
    url_detail = 'https://api.themoviedb.org/3/{media}/{tv_id}'.format(media=media_type,tv_id=id_api)
    response = requests.get(url_detail, headers=headers)
    r = response.json()
    data = r['release_date'] if media_type == 'movie' else r['first_air_date']
    generos = []
    
    for g in r['genres']:
        generos.append(g['name'])
        
    retorno = {
        "id_api": id_api,
        "media": media_type,
        'overview': r['overview'],
        'title': title,
        'release_date': '/'.join(data.split('-')[::-1]),
        'vote_average': r['vote_average'],
        'origin_country': r['origin_country'], 
        'genres': generos, 
        'img': img,
        'plataforma': plataforma, 
        'aluguel/compra': {"aluguel": providers_rent,
                           "compra": providers_buy}}
    return retorno

'''print(detalhes_titulo(568091, 'movie', "Fratura", ["Netflix"], ['Amazon Prime Video'], ['Amazon Prime Video'], 'https://image.tmdb.org/t/p/w500/vsvmurub7aShF1PIFJS2l2D5ArS.jpg'))'''

'''print(sugerir_titulos("Fratura"))'''