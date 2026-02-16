import requests

def buscar_plataformas_disponiveis(titulo):
    plataformas = [
        "Netflix",
        "Crunchyroll",
        "Disney Plus",
        "Globoplay",
        "HBO Max",
        "Apple TV",
        "Amazon Prime Video"
    ]

    url = 'https://api.themoviedb.org/3/search/multi'

    headers = {
        "accept": 'application/json',
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZDU4N2YxNjY3ZDViZDIzNjkyMDk1MjQ2NWE4OWQyZCIsIm5iZiI6MTc3MDk1NDQwOC44OTIsInN1YiI6IjY5OGU5ZWE4MjVjOGE0YThjYmI2ODk5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.SRmYAq05TPExKlLEzQut7hOuGAE2JFO_TOjW5RfvIpE"
    }
    
    response = requests.get(url, headers=headers, params={"query": titulo, "region": "BR"})
    results = response.json()['results']
    for r in results:
        if r['media_type'] == 'tv':
            url = 'https://api.themoviedb.org/3/tv/{tv_id}/watch/providers'.format(tv_id=r['id'])
            response = requests.get(url, headers=headers)
            if 'BR' in response.json()['results']:
                providers = response.json()['results']['BR']['flatrate']
                for provider in providers:
                    if provider['provider_name'] in plataformas:
                        print(provider['provider_name'])
                        try:
                            print(r['original_title'])
                        except:
                            print(r['original_name'])
        if r['media_type'] == 'movie':
            url = 'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers'.format(movie_id=r['id'])
            response = requests.get(url, headers=headers)
            if 'BR' in response.json()['results']:
                providers = response.json()['results']['BR']['flatrate']
                for provider in providers:
                    if provider['provider_name'] in plataformas:
                        print(provider['provider_name'])
                        try:
                            print(r['original_title'])
                        except:
                            print(r['original_name'])
                            
buscar_plataformas_disponiveis("office")