import requests
from functions import listarTitulos

url = 'https://api.themoviedb.org/3/search/multi'

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
    
    response = requests.get(url, headers=headers, params={"query": titulo, "region": "BR"})
    results_titulo = response.json()['results']
    for r in results_titulo:
        id_api = r['id']
        if r['media_type'] == 'tv' or r['media_type'] == 'movie':
            url = 'https://api.themoviedb.org/3/{media}/{tv_id}/watch/providers'.format(media=r['media_type'],tv_id=id_api)
            response = requests.get(url, headers=headers)
            result_providers = response.json()['results']
            if 'name' in r:
                nome = r['name']
            elif 'title' in r:
                nome = r['title']  
            elif 'original_title' in r:
                nome = r['original_title']
            elif 'original_name' in r:
                nome = r['original_name']
            else:
                nome = ''
            if 'BR' in result_providers:                 
                if 'flatrate' in result_providers['BR']:   
                    providers = result_providers['BR']['flatrate']
                else:
                    providers = []
                if 'rent' in result_providers['BR']:
                    providers_rent = [provider['provider_name'] for provider in result_providers['BR']['rent']]
                else:
                    providers_rent = ''
                if 'buy' in result_providers['BR']:
                    providers_buy = [provider['provider_name'] for provider in result_providers['BR']['buy']]
                else:
                    providers_buy = ''
                    
                plataforma = []
                if providers:
                    for provider in providers:
                        if provider['provider_name'] in plataformas:
                            plataforma.append(provider['provider_name']) 
                if plataforma == []:
                    plataforma = ''
                teste = {"id": r['id'], "media": r['media_type'], "titulo": f'{titulo} ({nome})', "plataforma": plataforma, "aluguel/compra": {"aluguel": providers_rent, "compra": providers_buy}}    
                sugestoes.append(teste)
    return sugestoes

def detalhes_titulo(id_api, media_type):
    url = 'https://api.themoviedb.org/3/{media}/{tv_id}'.format(media=media_type,tv_id=id_api)
    response = requests.get(url, headers=headers)
    return response.json()

print(detalhes_titulo('568091', 'movie'))

'''for filme in listarTitulos():
    try:
        print(buscar_plataformas_disponiveis(filme["titulo"]), '\n')
    except:
        print(f'{filme["titulo"]} não encontrado na API.\n')'''