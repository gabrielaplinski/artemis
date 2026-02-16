import requests

url = 'https://api.themoviedb.org/3/search/multi'

headers = {
    "accept": 'application/json',
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZDU4N2YxNjY3ZDViZDIzNjkyMDk1MjQ2NWE4OWQyZCIsIm5iZiI6MTc3MDk1NDQwOC44OTIsInN1YiI6IjY5OGU5ZWE4MjVjOGE0YThjYmI2ODk5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.SRmYAq05TPExKlLEzQut7hOuGAE2JFO_TOjW5RfvIpE"
}

response = requests.get(url, headers=headers, params={"query": "fratura", "region": "BR"})

results = response.json()['results']

for r in results:
    try:
        print(r['original_title'])

    except:
        print(r['original_name'])
    url = 'https://api.themoviedb.org/3/watch/providers/movie/' + str(r['id'])
    response = requests.get(url, headers=headers, params={"region": "BR"})
    print(response.json())